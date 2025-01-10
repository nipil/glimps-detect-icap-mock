import hashlib
import json
import time
from dataclasses import dataclass
from uuid import UUID, uuid4

from flask import Flask, request
from werkzeug.exceptions import NotFound

app = Flask(__name__)

BASE_PATH = '/api/lite/v2'

VALID_TOKEN = '00000000-00000000-00000000-00000000-00000000'

TOKEN_HEADER = 'X-Auth-Token'


def response_bad_request(e):
    return {
        "status": False,
        "error": e,
    }, 400


def response_invalid_filetype():
    return {
        "status": False,
        "error": "invalid filetype",
        "details": [
            {
                "file": "invalid filetype"
            }
        ]
    }, 400


def response_invalid_token():
    return {
        "status": False,
        "error": "unauthorized"
    }, 401


def response_bypass_denied():
    return {
        "status": False,
        "error": "bypass-cache denied"
    }, 403


def response_not_found():
    return {
        "status": False,
        "error": "not found"
    }, 404


def response_quota_exceeded():
    return {
        "status": False,
        "error": "quota exceeded, try again in 24h"
    }, 429


def response_internal_error():
    return {
        "status": False,
        "error": "internal server error"
    }, 500


@dataclass
class Expectation:
    invalid_file: bool = False
    invalid_token: bool = False
    bypass_denied: bool = False
    not_found: bool = False
    quota_exceeded: bool = False
    internal_error: bool = False
    malware: bool = False
    cache_result: bool = False
    wait_seconds: int = 0
    data: str = None

    def __post_init__(self):
        if self.data is None:
            self.data = ''

    def early_response(self, *, bypass_requested):
        if bypass_requested and self.bypass_denied:
            return response_bypass_denied()
        if self.invalid_file:
            return response_invalid_filetype()
        if self.invalid_token:
            return response_invalid_token()
        if self.not_found:
            return response_not_found()
        if self.quota_exceeded:
            return response_quota_exceeded()
        if self.internal_error:
            return response_internal_error()
        return None

    @staticmethod
    def from_bytes(data: bytes = None):
        try:
            expectation = data.decode()
        except UnicodeDecodeError:
            return Expectation()
        try:
            expectation = json.loads(expectation)
        except ValueError:
            return Expectation()
        try:
            expectation = Expectation(**expectation)
        except TypeError:
            return Expectation()
        return expectation


@dataclass
class Submission:
    sha256: str
    identifier: UUID
    expectation: Expectation
    timestamp: int
    done: bool = False
    is_malware: bool = False

    def to_result(self):
        return {
            "status": True,
            "uuid": str(self.identifier),
            "sha256": self.sha256,
            "sha1": "",
            "md5": "",
            "ssdeep": "",
            "is_malware": self.is_malware,
            "score": 0,
            "done": self.done,
            "timestamp": self.timestamp,
            "filetype": "",
            "size": 0,
            "file_count": 0,
            "duration": 0
        }


def sha256sum(data: bytes):
    m = hashlib.sha256()
    m.update(data)
    return m.hexdigest().lower()


SUBMISSIONS_BY_SHA256: dict[str, Submission] = {}

SUBMISSIONS_BY_UUID: dict[UUID, Submission] = {}


@dataclass
class Token:
    token: str = None

    def is_valid(self):
        try:
            return self.token == VALID_TOKEN
        except TypeError:
            return False

    @staticmethod
    def from_request():
        token = request.headers.get(TOKEN_HEADER, None)
        return Token(token=token)


@app.route(f"/{BASE_PATH}/search/<sha256>")
def search_sha(sha256: str):
    # validate token anyway
    if not Token.from_request().is_valid():
        return response_invalid_token()
    # get file hash
    sha256 = sha256.lower()
    # check cache miss
    if sha256 not in SUBMISSIONS_BY_SHA256:
        return response_not_found()
    # cache hit
    submission = SUBMISSIONS_BY_SHA256[sha256]
    return submission.to_result(), 200


@app.route(f"/{BASE_PATH}/submit", methods=['POST'])
def submit():
    # validate token anyway
    if not Token.from_request().is_valid():
        return response_invalid_token()
    # get file content
    try:
        file = request.files['file']
    except KeyError:
        return response_bad_request('Un champs "file" pour le fichier est nécessaire')
    data = file.read()
    # try to build an expectation from the uploaded file content
    expectation = Expectation.from_bytes(data)
    # handle cache bypass flag
    bypass_requested = str(request.values.get("bypass-cache", 'false')) == "true"
    early_response = expectation.early_response(bypass_requested=bypass_requested)
    if early_response is not None:
        return early_response
    # simulate an actual submission
    identifier = uuid4()
    sha256 = sha256sum(data)
    timestamp = int(time.time())
    print(f'submission: {identifier=} {sha256=} {timestamp=}')
    submission = Submission(identifier=identifier, sha256=sha256, expectation=expectation, timestamp=timestamp)
    SUBMISSIONS_BY_UUID[identifier] = submission
    if expectation.cache_result:
        SUBMISSIONS_BY_SHA256[sha256] = submission
    return {
        'status': True,
        'uuid': str(identifier).lower(),
        'error': ''
    }, 200


@app.route(f"/{BASE_PATH}/results/<identifier>")
def result_uuid(identifier: str):
    # validate token anyway
    if not Token.from_request().is_valid():
        return response_invalid_token()
    # get identifier
    identifier = identifier.lower()
    identifier = UUID(f'urn:uuid:{identifier}')
    if identifier not in SUBMISSIONS_BY_UUID:
        return response_not_found()
    submission = SUBMISSIONS_BY_UUID[identifier]
    # prepare result from current state
    result = submission.to_result()
    # mock processing duration based on expectation
    if not submission.done and int(time.time()) >= submission.timestamp + submission.expectation.wait_seconds:
        submission.done = True
        submission.is_malware = submission.expectation.malware
    # return in progress result
    return result, 200


def not_yet_implemented():
    # validate token anyway
    if not Token.from_request().is_valid():
        return response_invalid_token()
    return response_internal_error()


@app.route(f"/{BASE_PATH}/status")
def status():
    # TODO: implement if needed
    return not_yet_implemented()


@app.route(f"/{BASE_PATH}/results")
def results():
    # TODO: implement if needed
    return not_yet_implemented()


@app.route(f"/{BASE_PATH}/results/<uuid>/full")
def result_uuid_full():
    # TODO: implement if needed
    return not_yet_implemented()


@app.route(f"/{BASE_PATH}/search/<uuid>/<sha256>/service/<service>")
def result_uuid_sha256_service(uuid: UUID, sha256: str, service: str):
    # TODO: implement if needed
    return not_yet_implemented()
