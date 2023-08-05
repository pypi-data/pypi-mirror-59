# Copyright (C) 2015-2019  The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

import datetime
import hashlib
import logging
import os
import psycopg2
import requests
import traceback
import uuid

from abc import ABCMeta, abstractmethod
from retrying import retry
from typing import Any, Dict, Iterable, Mapping, Optional, Tuple, Union

from swh.core import config
from swh.storage import get_storage, HashCollision
from swh.loader.core.converters import content_for_storage


def retry_loading(error):
    """Retry policy when the database raises an integrity error"""
    exception_classes = [
        # raised when two parallel insertions insert the same data.
        psycopg2.IntegrityError,
        HashCollision,
        # raised when uWSGI restarts and hungs up on the worker.
        requests.exceptions.ConnectionError,
    ]

    if not any(isinstance(error, exc) for exc in exception_classes):
        return False

    logger = logging.getLogger('swh.loader')

    error_name = error.__module__ + '.' + error.__class__.__name__
    logger.warning('Retry loading a batch', exc_info=False, extra={
        'swh_type': 'storage_retry',
        'swh_exception_type': error_name,
        'swh_exception': traceback.format_exception(
            error.__class__,
            error,
            error.__traceback__,
        ),
    })

    return True


class BufferedLoader(config.SWHConfig, metaclass=ABCMeta):
    """Mixin base class for loader.

    To use this class, you must:

    - inherit from this class
    - and implement the @abstractmethod methods:

      - :func:`prepare`: First step executed by the loader to prepare some
        state needed by the `func`:load method.

      - :func:`get_origin`: Retrieve the origin that is currently being loaded.

      - :func:`fetch_data`: Fetch the data is actually the method to implement
        to compute data to inject in swh (through the store_data method)

      - :func:`store_data`: Store data fetched.

      - :func:`visit_status`: Explicit status of the visit ('partial' or
        'full')

      - :func:`load_status`: Explicit status of the loading, for use by the
        scheduler (eventful/uneventful/temporary failure/permanent failure).

      - :func:`cleanup`: Last step executed by the loader.

    The entry point for the resulting loader is :func:`load`.

    You can take a look at some example classes:

    - :class:`BaseSvnLoader`

    """
    CONFIG_BASE_FILENAME = None  # type: Optional[str]

    DEFAULT_CONFIG = {
        'storage': ('dict', {
            'cls': 'remote',
            'args': {
                'url': 'http://localhost:5002/',
            }
        }),

        'max_content_size': ('int', 100 * 1024 * 1024),
        'save_data': ('bool', False),
        'save_data_path': ('str', ''),

    }  # type: Dict[str, Tuple[str, Any]]

    ADDITIONAL_CONFIG = {}  # type: Dict[str, Tuple[str, Any]]

    def __init__(self, logging_class: Optional[str] = None,
                 config: Dict[str, Any] = {}):
        if config:
            self.config = config
        else:
            self.config = self.parse_config_file(
                additional_configs=[self.ADDITIONAL_CONFIG])

        self.storage = get_storage(**self.config['storage'])

        if logging_class is None:
            logging_class = '%s.%s' % (self.__class__.__module__,
                                       self.__class__.__name__)
        self.log = logging.getLogger(logging_class)

        _log = logging.getLogger('requests.packages.urllib3.connectionpool')
        _log.setLevel(logging.WARN)

        self.counters = {
            'contents': 0,
            'directories': 0,
            'revisions': 0,
            'releases': 0,
        }
        self.max_content_size = self.config['max_content_size']

        # possibly overridden in self.prepare method
        self.visit_date: Optional[Union[str, datetime.datetime]] = None

        self.origin: Dict[str, Any] = {}

        if not hasattr(self, 'visit_type'):
            self.visit_type: Optional[str] = None

        self.origin_metadata: Dict[str, Any] = {}

        # Make sure the config is sane
        save_data = self.config.get('save_data')
        if save_data:
            path = self.config['save_data_path']
            os.stat(path)
            if not os.access(path, os.R_OK | os.W_OK):
                raise PermissionError("Permission denied: %r" % path)

    def save_data(self) -> None:
        """Save the data associated to the current load"""
        raise NotImplementedError

    def get_save_data_path(self) -> str:
        """The path to which we archive the loader's raw data"""
        if not hasattr(self, '__save_data_path'):
            year = str(self.visit_date.year)  # type: ignore

            url = self.origin['url'].encode('utf-8')
            origin_url_hash = hashlib.sha1(url).hexdigest()

            path = '%s/sha1:%s/%s/%s' % (
                self.config['save_data_path'],
                origin_url_hash[0:2],
                origin_url_hash,
                year,
            )

            os.makedirs(path, exist_ok=True)
            self.__save_data_path = path

        return self.__save_data_path

    @retry(retry_on_exception=retry_loading, stop_max_attempt_number=3)
    def send_origin(self, origin: Dict[str, Any]) -> None:
        log_id = str(uuid.uuid4())
        self.log.debug('Creating origin for %s' % origin['url'],
                       extra={
                           'swh_type': 'storage_send_start',
                           'swh_content_type': 'origin',
                           'swh_num': 1,
                           'swh_id': log_id
                       })
        self.storage.origin_add_one(origin)
        self.log.debug('Done creating origin for %s' % origin['url'],
                       extra={
                           'swh_type': 'storage_send_end',
                           'swh_content_type': 'origin',
                           'swh_num': 1,
                           'swh_id': log_id
                       })

    @retry(retry_on_exception=retry_loading, stop_max_attempt_number=3)
    def send_origin_visit(self, visit_date: Union[str, datetime.datetime],
                          visit_type: str) -> Dict[str, Any]:
        log_id = str(uuid.uuid4())
        self.log.debug(
            'Creating origin_visit for origin %s at time %s' % (
                self.origin['url'], visit_date),
            extra={
                'swh_type': 'storage_send_start',
                'swh_content_type': 'origin_visit',
                'swh_num': 1,
                'swh_id': log_id
            })
        origin_visit = self.storage.origin_visit_add(
            self.origin['url'], visit_date, visit_type)
        self.log.debug(
            'Done Creating %s origin_visit for origin %s at time %s' % (
                visit_type, self.origin['url'], visit_date),
            extra={
                'swh_type': 'storage_send_end',
                'swh_content_type': 'origin_visit',
                'swh_num': 1,
                'swh_id': log_id
            })

        return origin_visit

    @retry(retry_on_exception=retry_loading, stop_max_attempt_number=3)
    def send_tool(self, tool: Dict[str, Any]) -> None:
        log_id = str(uuid.uuid4())
        self.log.debug(
            'Creating tool with name %s version %s configuration %s' % (
                 tool['name'], tool['version'], tool['configuration']),
            extra={
                'swh_type': 'storage_send_start',
                'swh_content_type': 'tool',
                'swh_num': 1,
                'swh_id': log_id
            })

        tools = self.storage.tool_add([tool])
        tool_id = tools[0]['id']

        self.log.debug(
            'Done creating tool with name %s version %s and configuration %s' % (  # noqa
                 tool['name'], tool['version'], tool['configuration']),
            extra={
                'swh_type': 'storage_send_end',
                'swh_content_type': 'tool',
                'swh_num': 1,
                'swh_id': log_id
            })
        return tool_id

    @retry(retry_on_exception=retry_loading, stop_max_attempt_number=3)
    def send_provider(self, provider: Dict[str, Any]) -> None:
        log_id = str(uuid.uuid4())
        self.log.debug(
            'Creating metadata_provider with name %s type %s url %s' % (
                provider['provider_name'], provider['provider_type'],
                provider['provider_url']),
            extra={
                'swh_type': 'storage_send_start',
                'swh_content_type': 'metadata_provider',
                'swh_num': 1,
                'swh_id': log_id
            })
        # FIXME: align metadata_provider_add with indexer_configuration_add
        _provider = self.storage.metadata_provider_get_by(provider)
        if _provider and 'id' in _provider:
            provider_id = _provider['id']
        else:
            provider_id = self.storage.metadata_provider_add(
                provider['provider_name'],
                provider['provider_type'],
                provider['provider_url'],
                provider['metadata'])

        self.log.debug(
            'Done creating metadata_provider with name %s type %s url %s' % (
                provider['provider_name'], provider['provider_type'],
                provider['provider_url']),
            extra={
                'swh_type': 'storage_send_end',
                'swh_content_type': 'metadata_provider',
                'swh_num': 1,
                'swh_id': log_id
            })
        return provider_id

    @retry(retry_on_exception=retry_loading, stop_max_attempt_number=3)
    def send_origin_metadata(self, visit_date, provider_id,
                             tool_id, metadata):
        log_id = str(uuid.uuid4())
        self.log.debug(
            'Creating origin_metadata for origin %s at time %s with provider_id %s and tool_id %s' % (  # noqa
                self.origin['url'], visit_date, provider_id, tool_id),
            extra={
                'swh_type': 'storage_send_start',
                'swh_content_type': 'origin_metadata',
                'swh_num': 1,
                'swh_id': log_id
            })

        self.storage.origin_metadata_add(
            self.origin['url'], visit_date, provider_id, tool_id, metadata)
        self.log.debug(
            'Done Creating origin_metadata for origin %s at time %s with provider %s and tool %s' % (  # noqa
                self.origin['url'], visit_date, provider_id, tool_id),
            extra={
                'swh_type': 'storage_send_end',
                'swh_content_type': 'origin_metadata',
                'swh_num': 1,
                'swh_id': log_id
            })

    @retry(retry_on_exception=retry_loading, stop_max_attempt_number=3)
    def update_origin_visit(self, status: str) -> None:
        log_id = str(uuid.uuid4())
        self.log.debug(
            'Updating origin_visit for origin %s with status %s' % (
                self.origin['url'], status),
            extra={
                'swh_type': 'storage_send_start',
                'swh_content_type': 'origin_visit',
                'swh_num': 1,
                'swh_id': log_id
            })
        self.storage.origin_visit_update(
            self.origin['url'], self.visit, status)
        self.log.debug(
            'Done updating origin_visit for origin %s with status %s' % (
                self.origin['url'], status),
            extra={
                'swh_type': 'storage_send_end',
                'swh_content_type': 'origin_visit',
                'swh_num': 1,
                'swh_id': log_id
            })

    @retry(retry_on_exception=retry_loading, stop_max_attempt_number=3)
    def send_contents(self, contents: Iterable[Mapping[str, Any]]) -> None:
        """Actually send properly formatted contents to the database.

        """
        contents = list(contents)
        num_contents = len(contents)
        if num_contents > 0:
            log_id = str(uuid.uuid4())
            self.log.debug("Sending %d contents" % num_contents,
                           extra={
                               'swh_type': 'storage_send_start',
                               'swh_content_type': 'content',
                               'swh_num': num_contents,
                               'swh_id': log_id,
                           })
            # FIXME: deal with this in model at some point
            result = self.storage.content_add([
                content_for_storage(
                    c, max_content_size=self.max_content_size,
                    origin_url=self.origin['url'])
                for c in contents
            ])
            self.counters['contents'] += result.get('content:add', 0)
            self.log.debug("Done sending %d contents" % num_contents,
                           extra={
                               'swh_type': 'storage_send_end',
                               'swh_content_type': 'content',
                               'swh_num': num_contents,
                               'swh_id': log_id,
                           })

    @retry(retry_on_exception=retry_loading, stop_max_attempt_number=3)
    def send_directories(self,
                         directories: Iterable[Mapping[str, Any]]) -> None:
        """Actually send properly formatted directories to the database.

        """
        directories = list(directories)
        num_directories = len(directories)
        if num_directories > 0:
            log_id = str(uuid.uuid4())
            self.log.debug("Sending %d directories" % num_directories,
                           extra={
                               'swh_type': 'storage_send_start',
                               'swh_content_type': 'directory',
                               'swh_num': num_directories,
                               'swh_id': log_id,
                           })
            result = self.storage.directory_add(directories)
            self.counters['directories'] += result.get('directory:add', 0)
            self.log.debug("Done sending %d directories" % num_directories,
                           extra={
                               'swh_type': 'storage_send_end',
                               'swh_content_type': 'directory',
                               'swh_num': num_directories,
                               'swh_id': log_id,
                           })

    @retry(retry_on_exception=retry_loading, stop_max_attempt_number=3)
    def send_revisions(self, revisions: Iterable[Mapping[str, Any]]) -> None:
        """Actually send properly formatted revisions to the database.

        """
        revisions = list(revisions)
        num_revisions = len(revisions)
        if num_revisions > 0:
            log_id = str(uuid.uuid4())
            self.log.debug("Sending %d revisions" % num_revisions,
                           extra={
                               'swh_type': 'storage_send_start',
                               'swh_content_type': 'revision',
                               'swh_num': num_revisions,
                               'swh_id': log_id,
                           })
            result = self.storage.revision_add(revisions)
            self.counters['revisions'] += result.get('revision:add', 0)
            self.log.debug("Done sending %d revisions" % num_revisions,
                           extra={
                               'swh_type': 'storage_send_end',
                               'swh_content_type': 'revision',
                               'swh_num': num_revisions,
                               'swh_id': log_id,
                           })

    @retry(retry_on_exception=retry_loading, stop_max_attempt_number=3)
    def send_releases(self, releases: Iterable[Mapping[str, Any]]) -> None:
        """Actually send properly formatted releases to the database.

        """
        releases = list(releases)
        num_releases = len(releases)
        if num_releases > 0:
            log_id = str(uuid.uuid4())
            self.log.debug("Sending %d releases" % num_releases,
                           extra={
                               'swh_type': 'storage_send_start',
                               'swh_content_type': 'release',
                               'swh_num': num_releases,
                               'swh_id': log_id,
                           })
            result = self.storage.release_add(releases)
            self.counters['releases'] += result.get('release:add', 0)
            self.log.debug("Done sending %d releases" % num_releases,
                           extra={
                               'swh_type': 'storage_send_end',
                               'swh_content_type': 'release',
                               'swh_num': num_releases,
                               'swh_id': log_id,
                           })

    @retry(retry_on_exception=retry_loading, stop_max_attempt_number=3)
    def send_snapshot(self, snapshot: Mapping[str, Any]) -> None:
        self.flush()  # to ensure the snapshot targets existing objects
        self.storage.snapshot_add([snapshot])
        self.storage.origin_visit_update(
            self.origin['url'], self.visit, snapshot=snapshot['id'])

    def flush(self) -> None:
        """Flush any potential dangling data not sent to swh-storage.

        Bypass the maybe_load_* methods which awaits threshold reached
        signal. We actually want to store those as we are done
        loading.

        """
        if hasattr(self.storage, 'flush'):
            self.storage.flush()

    def prepare_metadata(self) -> None:
        """First step for origin_metadata insertion, resolving the
        provider_id and the tool_id by fetching data from the storage
        or creating tool and provider on the fly if the data isn't available

        """
        origin_metadata = self.origin_metadata

        tool = origin_metadata['tool']
        try:
            tool_id = self.send_tool(tool)
            self.origin_metadata['tool']['tool_id'] = tool_id
        except Exception:
            self.log.exception('Problem when storing new tool')
            raise

        provider = origin_metadata['provider']
        try:
            provider_id = self.send_provider(provider)
            self.origin_metadata['provider']['provider_id'] = provider_id
        except Exception:
            self.log.exception('Problem when storing new provider')
            raise

    @abstractmethod
    def cleanup(self) -> None:
        """Last step executed by the loader.

        """
        pass

    @abstractmethod
    def prepare_origin_visit(self, *args, **kwargs) -> None:
        """First step executed by the loader to prepare origin and visit
           references. Set/update self.origin, and
           optionally self.origin_url, self.visit_date.

        """
        pass

    def _store_origin_visit(self) -> None:
        """Store origin and visit references. Sets the self.origin_visit and
           self.visit references.

        """
        origin = self.origin.copy()
        self.send_origin(origin)

        if not self.visit_date:  # now as default visit_date if not provided
            self.visit_date = datetime.datetime.now(tz=datetime.timezone.utc)
        self.origin_visit = self.send_origin_visit(
            self.visit_date, self.visit_type)
        self.visit = self.origin_visit['visit']

    @abstractmethod
    def prepare(self, *args, **kwargs) -> None:
        """Second step executed by the loader to prepare some state needed by
           the loader.

        """
        pass

    def get_origin(self) -> Dict[str, Any]:
        """Get the origin that is currently being loaded.
        self.origin should be set in :func:`prepare_origin`

        Returns:
          dict: an origin ready to be sent to storage by
          :func:`origin_add_one`.
        """
        return self.origin

    @abstractmethod
    def fetch_data(self) -> bool:
        """Fetch the data from the source the loader is currently loading
           (ex: git/hg/svn/... repository).

        Returns:
            a value that is interpreted as a boolean. If True, fetch_data needs
            to be called again to complete loading.

        """
        pass

    @abstractmethod
    def store_data(self):
        """Store fetched data in the database.

        Should call the :func:`maybe_load_xyz` methods, which handle the
        bundles sent to storage, rather than send directly.
        """
        pass

    def store_metadata(self) -> None:
        """Store fetched metadata in the database.

        For more information, see implementation in :class:`DepositLoader`.
        """
        pass

    def load_status(self) -> Dict[str, str]:
        """Detailed loading status.

        Defaults to logging an eventful load.

        Returns: a dictionary that is eventually passed back as the task's
          result to the scheduler, allowing tuning of the task recurrence
          mechanism.
        """
        return {
            'status': 'eventful',
        }

    def post_load(self, success: bool = True) -> None:
        """Permit the loader to do some additional actions according to status
        after the loading is done. The flag success indicates the
        loading's status.

        Defaults to doing nothing.

        This is up to the implementer of this method to make sure this
        does not break.

        Args:
            success (bool): the success status of the loading

        """
        pass

    def visit_status(self) -> str:
        """Detailed visit status.

        Defaults to logging a full visit.
        """
        return 'full'

    def pre_cleanup(self) -> None:
        """As a first step, will try and check for dangling data to cleanup.
        This should do its best to avoid raising issues.

        """
        pass

    def load(self, *args, **kwargs) -> Dict[str, str]:
        r"""Loading logic for the loader to follow:

        - 1. Call :meth:`prepare_origin_visit` to prepare the
             origin and visit we will associate loading data to
        - 2. Store the actual ``origin_visit`` to storage
        - 3. Call :meth:`prepare` to prepare any eventual state
        - 4. Call :meth:`get_origin` to get the origin we work with and store

        - while True:

          - 5. Call :meth:`fetch_data` to fetch the data to store
          - 6. Call :meth:`store_data` to store the data

        - 7. Call :meth:`cleanup` to clean up any eventual state put in place
             in :meth:`prepare` method.

        """
        try:
            self.pre_cleanup()
        except Exception:
            msg = 'Cleaning up dangling data failed! Continue loading.'
            self.log.warning(msg)

        self.prepare_origin_visit(*args, **kwargs)
        self._store_origin_visit()

        try:
            self.prepare(*args, **kwargs)

            while True:
                more_data_to_fetch = self.fetch_data()
                self.store_data()
                if not more_data_to_fetch:
                    break

            self.store_metadata()
            self.update_origin_visit(status=self.visit_status())
            self.post_load()
        except Exception:
            self.log.exception('Loading failure, updating to `partial` status',
                               extra={
                                   'swh_task_args': args,
                                   'swh_task_kwargs': kwargs,
                               })
            self.update_origin_visit(status='partial')
            self.post_load(success=False)
            return {'status': 'failed'}
        finally:
            self.flush()
            self.cleanup()

        return self.load_status()


class UnbufferedLoader(BufferedLoader):
    """This base class is a pattern for unbuffered loaders.

    UnbufferedLoader loaders are able to load all the data in one go. For
    example, the loader defined in swh-loader-git
    :class:`BulkUpdater`.

    For other loaders (stateful one, (e.g :class:`SWHSvnLoader`),
    inherit directly from :class:`BufferedLoader`.

    """
    ADDITIONAL_CONFIG = {}  # type: Dict[str, Tuple[str, Any]]

    def cleanup(self) -> None:
        """Clean up an eventual state installed for computations."""
        pass

    def has_contents(self) -> bool:
        """Checks whether we need to load contents"""
        return True

    def get_contents(self) -> Iterable[Dict[str, Any]]:
        """Get the contents that need to be loaded"""
        raise NotImplementedError

    def has_directories(self) -> bool:
        """Checks whether we need to load directories"""
        return True

    def get_directories(self) -> Iterable[Dict[str, Any]]:
        """Get the directories that need to be loaded"""
        raise NotImplementedError

    def has_revisions(self) -> bool:
        """Checks whether we need to load revisions"""
        return True

    def get_revisions(self) -> Iterable[Dict[str, Any]]:
        """Get the revisions that need to be loaded"""
        raise NotImplementedError

    def has_releases(self) -> bool:
        """Checks whether we need to load releases"""
        return True

    def get_releases(self) -> Iterable[Dict[str, Any]]:
        """Get the releases that need to be loaded"""
        raise NotImplementedError

    def get_snapshot(self) -> Dict[str, Any]:
        """Get the snapshot that needs to be loaded"""
        raise NotImplementedError

    def eventful(self) -> bool:
        """Whether the load was eventful"""
        raise NotImplementedError

    def store_data(self) -> None:
        if self.config['save_data']:
            self.save_data()

        if self.has_contents():
            self.send_contents(self.get_contents())
        if self.has_directories():
            self.send_directories(self.get_directories())
        if self.has_revisions():
            self.send_revisions(self.get_revisions())
        if self.has_releases():
            self.send_releases(self.get_releases())
        self.send_snapshot(self.get_snapshot())
        self.flush()
