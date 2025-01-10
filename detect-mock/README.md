# glimps detect api mock app

## How to use

### Compose

Use image as is and application autostarts

### Development

Open in dev container, then :

- run the mocked API for glimps-detect in a terminal :

        python3 -m flask --app mock --debug run --host 0.0.0.0

- unit-testing
    - open another terminal
    - run the "test" queries of the next sections below


- integration-testing
    - run `icap-detect` in another terminal :

          /srv/icap-detect -verbose -timeout=3s --token=00000000-00000000-00000000-00000000-00000000 --host http://127.0.0.1:5000

    - run the following commands in another terminal :

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

## Usage and log examples of `icap-detect`

Sample usage :

    -bypass-cache=false: disable detect result cache (degrade performances)
    -certificate="": TLS certificate path for ICAP
    -host="": GLIMPS Malware Detect host like https://gmalware.domain.tld
    -insecure=false: disable HTTPS certificate checks
    -key="": TLS key path for ICAP
    -syndetect=false: use syndetect API
    -tag="": additionnal tag associated with analyses
    -timeout=5m0s: timeout associated with analyses
    -token="": GLIMPS Malware detect authorization token
    -verbose=false: print information strings

Sample logging (in verbose mode)

    configuration: {
    "host": "http://127.0.0.1:5000",
    "insecure": false,
    "verbose": true,
    "bypass_cache": false,
    "syndetect": false,
    "tags": [
    "ICAP"
    ],
    "timeout": 3000000000,
    "tls_cert_path": "",
    "tls_key_path": ""
    }
    {"level":"info","msg":"ready to handle icap requests","time":"2025-01-10T14:24:45Z"}
    {"level":"error","msg":"Get \"http://127.0.0.1:5000/api/lite/v2/search/d914176fd50bd7f565700006a31aa97b79d3ad17cee20c8e5ff2061d5cb74817\": dial tcp 127.0.0.1:5000: connect: connection refused","time":"2025-01-10T14:24:50Z"}
    {"level":"info","msg":"file dcf16cf0-a516-4a17-995d-4d65666c0312 is not a malware: false (0)","time":"2025-01-10T14:25:16Z"}
    {"level":"info","msg":"malware DETECTED for uuid a8274f0e-9771-49ad-a322-37c9b92f0546 (0)","time":"2025-01-10T14:27:55Z"}
    {"level":"error","msg":"could not analyze file 7c6279cd418e79327e31c2fa49d1f44e39200d61ced0ddb2d661bc5a34070c40, error: 500 INTERNAL SERVER ERROR","time":"2025-01-10T14:28:01Z"}
    {"level":"error","msg":"could not analyze file fcd8410b0acf6a8bb7fd6771a0e32ce28f89946cfdcecc2fa5a77dd3ce8870fc, error: 400 BAD REQUEST","time":"2025-01-10T14:28:07Z"}
    {"level":"error","msg":"could not analyze file 39f035accc6015d4748a9000370dfd8a23d1e6561256c8a8279c442f244e2cd6, error: 401 UNAUTHORIZED","time":"2025-01-10T14:28:14Z"}
    {"level":"error","msg":"could not analyze file 20778bed9d178c07aee3490c2181796895d179b929e764fc489513f2adf31320, error: 404 NOT FOUND","time":"2025-01-10T14:28:18Z"}
    {"level":"error","msg":"could not analyze file a9e1991428cce150cbf7d37181a72eed30f959f35e587a4c2ed8495eb8d15026, error: 429 TOO MANY REQUESTS","time":"2025-01-10T14:28:22Z"}
    {"level":"error","msg":"could not analyze file a6b3af66c98e61bf2d7929af559defece09c8d83d67df6f92c0390f2070e8185, error: timeout","time":"2025-01-10T14:28:30Z"}
    {"level":"error","msg":"could not analyze file 284bcf42014a1b1d6dcab2691d489bf76e27a8343f6a7823b343102e228220dc, error: 403 FORBIDDEN","time":"2025-01-10T14:28:59Z"}
