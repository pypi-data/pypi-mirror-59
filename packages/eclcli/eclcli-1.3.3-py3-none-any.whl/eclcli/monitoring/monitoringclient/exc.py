#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import json
import sys


class BaseException(Exception):
    """An error occurred."""
    def __init__(self, message=None):
        self.message = message

    def __str__(self):
        return self.message or self.__class__.__doc__


class CommandError(BaseException):
    """Invalid usage of CLI."""


class InvalidEndpoint(BaseException):
    """The provided endpoint is invalid."""


class CommunicationError(BaseException):
    """Unable to communicate with server."""


class HTTPException(BaseException):
    """Base exception for all HTTP-derived exceptions."""
    code = 'N/A'

    def __init__(self, details=None):
        self.details = details

    def __str__(self):
        try:
            data = json.loads(self.details)
            message = data.get("error_message", {}).get("faultstring")
            if message:
                return "%s (HTTP %s) ERROR %s" % (
                    self.__class__.__name__, self.code, message)
        except (ValueError, TypeError, AttributeError):
            pass
        return "%s (HTTP %s)" % (self.__class__.__name__, self.code)


class HTTPMultipleChoices(HTTPException):
    code = 300

    def __str__(self):
        self.details = ("Requested version of OpenStack Images API is not"
                        "available.")
        return "%s (HTTP %s) %s" % (self.__class__.__name__, self.code,
                                    self.details)


class HTTPBadRequest(HTTPException):
    code = 400


class HTTPUnauthorized(HTTPException):
    code = 401


class HTTPForbidden(HTTPException):
    code = 403


class HTTPNotFound(HTTPException):
    code = 404


class HTTPMethodNotAllowed(HTTPException):
    code = 405


class HTTPConflict(HTTPException):
    code = 409


class HTTPOverLimit(HTTPException):
    code = 413


class HTTPInternalServerError(HTTPException):
    code = 500


class HTTPNotImplemented(HTTPException):
    code = 501


class HTTPBadGateway(HTTPException):
    code = 502


class HTTPServiceUnavailable(HTTPException):
    code = 503


# NOTE(bcwaldon): Build a mapping of HTTP codes to corresponding exception
# classes
_code_map = {}
for obj_name in dir(sys.modules[__name__]):
    if obj_name.startswith('HTTP'):
        obj = getattr(sys.modules[__name__], obj_name)
        _code_map[obj.code] = obj


def from_response(response, details=None):
    """Return an instance of an HTTPException based on httplib response."""
    cls = _code_map.get(response.status_code, HTTPException)
    return cls(details)
