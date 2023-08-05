# -*- coding: utf-8 -*-

import uuid
import time
import datetime
from warnings import warn
from functools import wraps

from requests import Session

try:
    from urllib import quote
except ImportError:
    from urllib.parse import quote

DIALECT = 'python'

DEFAULT_API_VERSION = 1

DEFAULT_BUILD_TITLE = 'Launch at {}'.format(
    datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S'),
)

DEFAULT_BUILD_NAME = str(hash(str(uuid.uuid4()) + str(time.time())))


class RemoteApiError(UserWarning):
    pass


def will_expected(status_code):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            try:
                resp = f(*args, **kwargs)
            except BaseException as error:
                warn(
                    '{}'.format(
                        error.__class__.__name__,
                        getattr(
                            error, 'message',
                            u' '.join(
                                str(i) for i in getattr(error, 'args', []) if not isinstance(i, int)
                            )
                        ),
                    ),
                    RemoteApiError,
                )
                return None

            if resp is not None and resp.status_code != status_code:
                message = u'Aggregate analytic error. From URL {} got response {}'.format(
                    resp.url, resp.content,
                )
                warn(message, RemoteApiError)
            return resp

        return wrapped

    return wrapper


def true_by_status(success_status_code):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            try:
                resp = f(*args, **kwargs)
            except BaseException as error:
                warn(
                    '{}'.format(
                        error.__class__.__name__,
                        getattr(
                            error, 'message',
                            u' '.join(
                                str(i) for i in getattr(error, 'args', []) if not isinstance(i, int)
                            )
                        ),
                    ),
                    RemoteApiError,
                )
                return False

            if resp.status_code == success_status_code:
                return True
            return False

        return wrapped

    return wrapper


class Seisma(Session):

    def __init__(self,
                 base_url,
                 job_name,
                 job_title,
                 build_title,
                 build_name=None,
                 api_version=None,
                 build_metadata=None,
                 build_name_preffix=None):
        self.base_url = base_url
        self.api_version = api_version or DEFAULT_API_VERSION

        self.api_url = '{}/api/v{}'.format(self.base_url, self.api_version)

        self.build_title = build_title or DEFAULT_BUILD_TITLE
        self.build_name = quote(build_name or DEFAULT_BUILD_NAME)

        if build_name_preffix:
            self.build_name = build_name_preffix + self.build_name

        self.job_name = quote(job_name)
        self.job_title = job_title

        self.build_metadata = build_metadata

        super(Seisma, self).__init__()

        self.headers['Content-Type'] = 'application/json'

    @will_expected(201)
    def create_job(self, description=None):
        url = '{}{}'.format(
            self.api_url,
            '/jobs/{}'.format(self.job_name),
        )
        json = {
            'title': self.job_title,
        }
        if description:
            json['description'] = description

        return self.post(url, json=json)

    @true_by_status(200)
    def job_exists(self):
        url = '{}{}'.format(
            self.api_url,
            '/jobs/{}'.format(self.job_name),
        )

        return self.get(url)

    @will_expected(201)
    def start_build(self):
        url = '{}{}'.format(
            self.api_url,
            '/jobs/{}/builds/{}/start'.format(
                self.job_name, self.build_name,
            ),
        )

        json = {
            'title': self.build_title,
        }

        if isinstance(self.build_metadata, dict):
            json['metadata'] = self.build_metadata

        return self.post(url, json=json)

    @will_expected(200)
    def stop_build(self,
                   runtime,
                   was_success,
                   tests_count,
                   success_count,
                   fail_count,
                   error_count):
        url = '{}{}'.format(
            self.api_url,
            '/jobs/{}/builds/{}/stop'.format(
                self.job_name, self.build_name,
            ),
        )
        json = {
            'runtime': runtime,
            'was_success': was_success,
            'tests_count': tests_count,
            'success_count': success_count,
            'fail_count': fail_count,
            'error_count': error_count,
        }

        return self.put(url, json=json)

    @true_by_status(200)
    def case_exists_on_job(self, name):
        url = '{}{}'.format(
            self.api_url,
            '/jobs/{}/cases/{}'.format(
                self.job_name, quote(name),
            ),
        )

        return self.get(url)

    @will_expected(201)
    def add_case_to_job(self, name, description=None):
        url = '{}{}'.format(
            self.api_url,
            '/jobs/{}/cases/{}'.format(
                self.job_name, quote(name),
            ),
        )
        json = {}

        if description:
            json['description'] = description

        return self.post(url, json=json)

    @will_expected(200)
    def update_case_in_job(self, name, description):
        url = '{}{}'.format(
            self.api_url,
            '/jobs/{}/cases/{}'.format(
                self.job_name, quote(name),
            ),
        )
        json = {
            'description': description,
        }

        return self.put(url, json=json)

    @will_expected(201)
    def add_case_result(self, name, status, runtime, reason=None, metadata=None):
        url = '{}{}'.format(
            self.api_url,
            '/jobs/{}/builds/{}/cases/{}'.format(
                self.job_name, self.build_name, quote(name),
            ),
        )

        json = {
            'status': status,
            'runtime': runtime,
            'dialect': DIALECT,
        }

        if reason:
            json['reason'] = reason

        if metadata:
            json['metadata'] = metadata

        return self.post(url, json=json)
