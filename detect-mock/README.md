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

## Testing with `c-icap-client`

Usage :

    c-icap-client [-V ] [-VV ] [-i icap_servername] [-p port] [-s service] [-tls ] [-tls-method tls_method] [-tls-no-verify ] [-f filename] [-o filename] [-method method] [-req url] [-resp url] [-d level] [-noreshdr ] [-nopreview ] [-no204 ] [-206 ] [-x xheader] [-hx xheader] [-rhx xheader] [-w preview] [-v ]
    
    -V                      : Print version and exits
    -VV                     : Print version and build informations and exits
    -i icap_servername              : The icap server name
    -p port         : The server port
    -s service              : The service name
    -tls                    : Use TLS
    -tls-method tls_method          : Use TLS method
    -tls-no-verify                  : Disable server certificate verify
    -f filename             : Send this file to the icap server.
    Default is to send an options request
    -o filename             : Save output to this file.
    Default is to send to stdout
    -method method          : Use 'method' as method of the request modification
    -req url                : Send a request modification instead of response modification
    -resp url               : Send a responce modification request with request url the 'url'
    -d level                : debug level info to stdout
    -noreshdr                       : Do not send reshdr headers
    -nopreview                      : Do not send preview data
    -no204                  : Do not allow204 outside preview
    -206                    : Support allow206
    -x xheader              : Include xheader in icap request headers
    -hx xheader             : Include xheader in http request headers
    -rhx xheader            : Include xheader in http response headers
    -w preview              : Sets the maximum preview data size
    -v                      : Print response headers

Try to provide additionnal data (and use maximum debug) :

    c-icap-client -i 127.0.0.1 -p 1344 -v -f samples/malware-nocache.json -d 10 \
        -x "x1: foo" -x "x2: bar" -rhx "rhx1: aze" -rhx "rhx2: qsd" -s toto

    OK done with options!
    ICAP server:127.0.0.1, ip:127.0.0.1, port:1344

    Preview:-1 keepalive:0,allow204:0
    OK allocating request going to send request
    Allocate a new entity of type 1
    Allocate a new entity of type 3
    Going to add 6 response headers
    Add resp header: HTTP/1.0 200 OK
    Add resp header: Date: Fri Jan 10 17:28:24 2025
    Add resp header: Last-Modified: Fri Jan 10 17:28:24 2025
    Add resp header: Content-Length: 22
    Add resp header: rhx1: aze
    Add resp header: rhx2: qsd
    Response was with status:200 
    Get entity from trash....
    Get entity from trash....
    OK reading headers, going to read body

    ICAP HEADERS:
            ICAP/1.0 200 OK
            Connection: close
            Date: Fri, 10 Jan 2025 17:28:24 GMT
            Istag: "WEBFILTER"
            Service: GMalware-detect-0.2.4
            Encapsulated: res-hdr=0, res-body=26

    RESPMOD HEADERS:
            HTTP/1.1 403 Forbidden

    Done

Seen headers and payload in mock api :

    Headers {"Host": "127.0.0.1:5000", "User-Agent": "Go-http-client/1.1", "X-Auth-Token": "00000000-00000000-00000000-00000000-00000000", "Accept-Encoding": "gzip"}
    Form {"tags": "ICAP"}

Use `tcpdump` to check what goes on the wire :

- service (`toto`) is ignored on icap-detect side
- icap headers (`-x`) are not forwarded to api, nor logged in `icap-detect`
- request headers (`-hx`) are not forwarded to api (that is OK, as we work in RESPmod !), nor logged in `icap-detect`
- response headers (`-rhx`) are not forwarded to api (even if we work in RESPmod), nor logged in `icap-detect`

Example network capture :

    OPTIONS icap://127.0.0.1/toto ICAP/1.0
    Host: 127.0.0.1
    User-Agent: C-ICAP-Client-Library/0.5.10
    x1: foo
    x2: bar
    Encapsulated: null-body=0


    ICAP/1.0 200 OK
    Allow: 204
    Connection: close
    Date: Fri, 10 Jan 2025 17:28:24 GMT
    Istag: "WEBFILTER"
    Methods: RESPMOD, REQMOD
    Service: GMalware-detect-0.2.4
    Transfer-Preview: *
    Encapsulated: null-body=0


    RESPMOD icap://127.0.0.1/toto ICAP/1.0
    Host: 127.0.0.1
    User-Agent: C-ICAP-Client-Library/0.5.10
    Allow: 204
    x1: foo
    x2: bar
    Encapsulated: res-hdr=0, res-body=134

    HTTP/1.0 200 OK
    Date: Fri Jan 10 17:28:24 2025
    Last-Modified: Fri Jan 10 17:28:24 2025
    Content-Length: 22
    rhx1: aze
    rhx2: qsd

    16
    {
    "malware": true
    }

    0


    ICAP/1.0 200 OK
    Connection: close
    Date: Fri, 10 Jan 2025 17:28:24 GMT
    Istag: "WEBFILTER"
    Service: GMalware-detect-0.2.4
    Encapsulated: res-hdr=0, res-body=26

    HTTP/1.1 403 Forbidden

    0

## Suggestions for `icap-detect`

### Client-provided token

**Proposal** : dynamically forward provided `X-Auth-Token` ICAP header (provided by `-x`) token to Detect API

Bundling an `icap-detect` instance in each platform to tune instance parameters "per-platform" is easy and efficient
when using containers, as deployment, configuration and upgrade is convenient, and lightweight.

When using VMs, bundling the binary or creating a dedicated VM in each platform, just to be able to be able to
tune the parameters of the running `icap-detect` "per-platform" is inefficient (dedicated VM) or makes upgrading
`icap-detect` instances troublesome (when bundling in application VM).

This proposal would allow differentiating client token (quotas/policy/processing...), while allowing for a
centralized `icap-detect` instance, making maintenance and deployment of the `icap-detect` server easier.

### Client-provided tags

**Proposal** : dynamically forward tags present in `X-Additionnal-Tags` response header (provided by `-rhx`)

This would allow for clients to submit additionnal (_non-authoritative_) metadata to Detect API submissions.

### Logging of client-provided information

**Proposal** : log information about the ICAP client

- authoritative client IP from TCP connection source
- _non-autoritative_ `X-Additionnal-Tags` response header
- _non-autoritative_ `X-Forwarded-For` response header

This would allow attributing scan results to sources through `icap-detect` logs.

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
