# glimps detect api mock app

## How to use

### Compose

Use image as is and application autostarts

### Development

Open in dev container, then :

- run the mocked API for glimps-detect in a terminal :


    python3 -m flask --app mock --debug run --host 0.0.0.0

- in another terminal, run the "test" queries of the next sections below for unit-testing

- run `icap-detect` in another terminal :


    /srv/icap-detect -verbose -timeout=3s --token=00000000-00000000-00000000-00000000-00000000 --host http://127.0.0.1:5000

- and run the following commands in another terminal :

Safe files :

    c-icap-client -i 127.0.0.1 -p 1344 -v -f samples/legit-nocache.json
    c-icap-client -i 127.0.0.1 -p 1344 -v -f samples/cached-legit.json

        ICAP server:127.0.0.1, ip:127.0.0.1, port:1344

        No modification needed (Allow 204 response)

        ICAP HEADERS:
                ICAP/1.0 204 No Modifications
                Connection: close
                Date: Tue, 07 Jan 2025 14:26:33 GMT
                Istag: "WEBFILTER"
                Service: GMalware-detect-0.2.1
                Encapsulated: res-hdr=0, res-body=19

Malware :

    c-icap-client -i 127.0.0.1 -p 1344 -v -f samples/malware-nocache.json
    c-icap-client -i 127.0.0.1 -p 1344 -v -f samples/cached-malware.json

        ICAP server:127.0.0.1, ip:127.0.0.1, port:1344

        ICAP HEADERS:
                ICAP/1.0 200 OK
                Connection: close
                Date: Tue, 07 Jan 2025 14:26:57 GMT
                Istag: "WEBFILTER"
                Service: GMalware-detect-0.2.1
                Encapsulated: res-hdr=0, res-body=26

        RESPMOD HEADERS:
                HTTP/1.1 403 Forbidden

Mocking Glimps Detect api errors :

    c-icap-client -i 127.0.0.1 -p 1344 -v -f samples/internal-error.json

        ICAP server:127.0.0.1, ip:127.0.0.1, port:1344

        ICAP HEADERS:
                ICAP/1.0 502 Bad Gateway
                Connection: close
                Date: Tue, 07 Jan 2025 14:23:58 GMT
                Istag: "WEBFILTER"
                Service: GMalware-detect-0.2.1
                Encapsulated: res-hdr=0, res-body=38

        RESPMOD HEADERS:
                HTTP/1.1 500 Internal Server Error

    c-icap-client -i 127.0.0.1 -p 1344 -v -f samples/invalid-file.json

        ICAP server:127.0.0.1, ip:127.0.0.1, port:1344

        ICAP HEADERS:
                ICAP/1.0 502 Bad Gateway
                Connection: close
                Date: Tue, 07 Jan 2025 14:24:13 GMT
                Istag: "WEBFILTER"
                Service: GMalware-detect-0.2.1
                Encapsulated: res-hdr=0, res-body=28

        RESPMOD HEADERS:
                HTTP/1.1 400 Bad Request

    c-icap-client -i 127.0.0.1 -p 1344 -v -f samples/invalid-token.json

        ICAP server:127.0.0.1, ip:127.0.0.1, port:1344

        ICAP HEADERS:
                ICAP/1.0 502 Bad Gateway
                Connection: close
                Date: Tue, 07 Jan 2025 14:24:50 GMT
                Istag: "WEBFILTER"
                Service: GMalware-detect-0.2.1
                Encapsulated: res-hdr=0, res-body=29

        RESPMOD HEADERS:
                HTTP/1.1 401 Unauthorized

    c-icap-client -i 127.0.0.1 -p 1344 -v -f samples/not-found.json

        ICAP server:127.0.0.1, ip:127.0.0.1, port:1344

        ICAP HEADERS:
                ICAP/1.0 502 Bad Gateway
                Connection: close
                Date: Tue, 07 Jan 2025 14:25:04 GMT
                Istag: "WEBFILTER"
                Service: GMalware-detect-0.2.1
                Encapsulated: res-hdr=0, res-body=26

        RESPMOD HEADERS:
                HTTP/1.1 404 Not Found

    c-icap-client -i 127.0.0.1 -p 1344 -v -f samples/quota-exceeded.json

        ICAP server:127.0.0.1, ip:127.0.0.1, port:1344

        ICAP HEADERS:
                ICAP/1.0 502 Bad Gateway
                Connection: close
                Date: Tue, 07 Jan 2025 14:25:21 GMT
                Istag: "WEBFILTER"
                Service: GMalware-detect-0.2.1
                Encapsulated: res-hdr=0, res-body=34

        RESPMOD HEADERS:
                HTTP/1.1 429 Too Many Requests

    c-icap-client -i 127.0.0.1 -p 1344 -v -f samples/too-long.json

        ICAP server:127.0.0.1, ip:127.0.0.1, port:1344

        ICAP HEADERS:
                ICAP/1.0 408 Request Timeout
                Connection: close
                Date: Tue, 07 Jan 2025 14:22:34 GMT
                Istag: "WEBFILTER"
                Service: GMalware-detect-0.2.1
                Encapsulated: res-hdr=0, res-body=32

        RESPMOD HEADERS:
                HTTP/1.1 408 Request Timeout

- restart icap-detect adding `-bypass-cache=true` to the arguments

    c-icap-client -i 127.0.0.1 -p 1344 -v -f samples/bypass-denied.json

        ICAP server:127.0.0.1, ip:127.0.0.1, port:1344

        ICAP HEADERS:
                ICAP/1.0 502 Bad Gateway
                Connection: close
                Date: Tue, 07 Jan 2025 14:23:29 GMT
                Istag: "WEBFILTER"
                Service: GMalware-detect-0.2.1
                Encapsulated: res-hdr=0, res-body=26

        RESPMOD HEADERS:
                HTTP/1.1 403 Forbidden

## Test mocked `icap-detect` normal workflow

Check for cache miss :

    curl --fail-with-body --request GET -H "X-Auth-Token: 00000000-00000000-00000000-00000000-00000000" localhost:5000/api/lite/v2/search/non_existing_sha256
    {
    "error": "not found",
    "status": false
    }
    curl: (22) The requested URL returned error: 404

Submits file :

    curl --fail-with-body --request POST -H "X-Auth-Token: 00000000-00000000-00000000-00000000-00000000" --form "file=@samples/cached-legit.json" localhost:5000/api/lite/v2/submit
    {
    "error": "",
    "status": true,
    "uuid": "afc918f3-0ed8-433d-84ff-c806fed2c777"
    }

Checks for result until done :

    curl --fail-with-body --request GET -H "X-Auth-Token: 00000000-00000000-00000000-00000000-00000000" localhost:5000/api/lite/v2/results/afc918f3-0ed8-433d-84ff-c806fed2c777
    {
    "done": false,
    "duration": 0,
    "file_count": 0,
    "filetype": "",
    "is_malware": false,
    "md5": "",
    "score": 0,
    "sha1": "",
    "sha256": "a711400fb202d34d3214a7e996f8957171e87239be3f76ef54d5ea46f26e4a3b",
    "size": 0,
    "ssdeep": "",
    "status": true,
    "timestamp": 1736245591,
    "uuid": "afc918f3-0ed8-433d-84ff-c806fed2c777"
    }

    curl --fail-with-body --request GET -H "X-Auth-Token: 00000000-00000000-00000000-00000000-00000000" localhost:5000/api/lite/v2/search/a711400fb202d34d3214a7e996f8957171e87239be3f76ef54d5ea46f26e4a3b
    {
    "done": true,
    "duration": 0,
    "file_count": 0,
    "filetype": "",
    "is_malware": false,
    "md5": "",
    "score": 0,
    "sha1": "",
    "sha256": "a711400fb202d34d3214a7e996f8957171e87239be3f76ef54d5ea46f26e4a3b",
    "size": 0,
    "ssdeep": "",
    "status": true,
    "timestamp": 1736245591,
    "uuid": "afc918f3-0ed8-433d-84ff-c806fed2c777"
    }

# Test mocked failures

Quota exceeded :

    curl --fail-with-body --request POST -H "X-Auth-Token: 00000000-00000000-00000000-00000000-00000000" --form "file=@samples/quota-exceeded.json" localhost:5000/api/lite/v2/submit
    {
    "error": "quota exceeded, try again in 24h",
    "status": false
    }
    curl: (22) The requested URL returned error: 429

Not found :

    curl --fail-with-body --request POST -H "X-Auth-Token: 00000000-00000000-00000000-00000000-00000000" --form "file=@samples/not-found.json" localhost:5000/api/lite/v2/submit
    {
    "error": "not found",
    "status": false
    }
    curl: (22) The requested URL returned error: 404

Invalid token :

    curl --fail-with-body --request POST -H "X-Auth-Token: 00000000-00000000-00000000-00000000-00000000" --form "file=@samples/invalid-token.json" localhost:5000/api/lite/v2/submit
    {
    "error": "unauthorized",
    "status": false
    }
    curl: (22) The requested URL returned error: 401

Invalid file :

    curl --fail-with-body --request POST -H "X-Auth-Token: 00000000-00000000-00000000-00000000-00000000" --form "file=@samples/invalid-file.json" localhost:5000/api/lite/v2/submit
    {
    "details": [
        {
        "file": "invalid filetype"
        }
    ],
    "error": "invalid filetype",
    "status": false
    }
    curl: (22) The requested URL returned error: 400

Internal server error :

    curl --fail-with-body --request POST -H "X-Auth-Token: 00000000-00000000-00000000-00000000-00000000" --form "file=@samples/internal-error.json" localhost:5000/api/lite/v2/submit
    {
    "error": "internal server error",
    "status": false
    }
    curl: (22) The requested URL returned error: 500

Cache bypass forbidden :

    curl --fail-with-body --request POST -H "X-Auth-Token: 00000000-00000000-00000000-00000000-00000000" --form "file=@samples/bypass-denied.json" localhost:5000/api/lite/v2/submit?bypass-cache=true
    {
    "error": "bypass-cache denied",
    "status": false
    }
    curl: (22) The requested URL returned error: 403
