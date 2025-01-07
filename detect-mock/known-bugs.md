# Bugs possibles

## MINEUR: double cache search en 0.2.2, alors qu'on en a qu'un en 0.2.1

_Question: pourquoi deux cache hit dans la nouvelle version ?_

Requêtes reçues avec icap-detect 0.2.1 :

    127.0.0.1 - - [07/Jan/2025 16:08:50] "GET /api/lite/v2/search/d914176fd50bd7f565700006a31aa97b79d3ad17cee20c8e5ff2061d5cb74817 HTTP/1.1" 404 -
    submission: identifier=UUID('3495f387-5b21-44e3-bb02-5651fad416b2') sha256='d914176fd50bd7f565700006a31aa97b79d3ad17cee20c8e5ff2061d5cb74817' timestamp=1736266130
    127.0.0.1 - - [07/Jan/2025 16:08:50] "POST /api/lite/v2/submit HTTP/1.1" 200 -
    127.0.0.1 - - [07/Jan/2025 16:08:50] "GET /api/lite/v2/results/3495f387-5b21-44e3-bb02-5651fad416b2 HTTP/1.1" 200 -
    127.0.0.1 - - [07/Jan/2025 16:08:50] "GET /api/lite/v2/results/3495f387-5b21-44e3-bb02-5651fad416b2 HTTP/1.1" 200 -

Requêtes reçues avec icap-detect 0.2.2 :

    127.0.0.1 - - [07/Jan/2025 16:05:51] "GET /api/lite/v2/search/d914176fd50bd7f565700006a31aa97b79d3ad17cee20c8e5ff2061d5cb74817 HTTP/1.1" 404 -
    127.0.0.1 - - [07/Jan/2025 16:05:51] "GET /api/lite/v2/search/d914176fd50bd7f565700006a31aa97b79d3ad17cee20c8e5ff2061d5cb74817 HTTP/1.1" 404 -
    submission: identifier=UUID('3a874173-3a3f-4813-b36f-186150a891f9') sha256='d914176fd50bd7f565700006a31aa97b79d3ad17cee20c8e5ff2061d5cb74817' timestamp=1736265951
    127.0.0.1 - - [07/Jan/2025 16:05:51] "POST /api/lite/v2/submit HTTP/1.1" 200 -
    127.0.0.1 - - [07/Jan/2025 16:05:51] "GET /api/lite/v2/results/3a874173-3a3f-4813-b36f-186150a891f9 HTTP/1.1" 200 -
    127.0.0.1 - - [07/Jan/2025 16:05:51] "GET /api/lite/v2/results/3a874173-3a3f-4813-b36f-186150a891f9 HTTP/1.1" 200 -

## MAJEUR: Gestion de la reply /search/hash quand cache miss (404) et réponse json

_Question : est-ce que icap-detect gère bien le retour JSON pour le 404 /search/xxxxx ?_

Voir le commentaire `mock.py`, lignes 186-190

### Cas "nominal" : en retournant du json, avec un body conforme à la spec openapi.

Si la réponse de l'appli de mock api est la suivante pour le cache miss:

    curl --fail-with-body --verbose --request GET -H "X-Auth-Token: 00000000-00000000-00000000-00000000-00000000" localhost:5000/api/lite/v2/search/non_existing_sha256
    Note: Unnecessary use of -X or --request, GET is already inferred.
    *   Trying 127.0.0.1:5000...
    * Connected to localhost (127.0.0.1) port 5000 (#0)
    > GET /api/lite/v2/search/non_existing_sha256 HTTP/1.1
    > Host: localhost:5000
    > User-Agent: curl/7.88.1
    > Accept: */*
    > X-Auth-Token: 00000000-00000000-00000000-00000000-00000000
    > 
    < HTTP/1.1 404 NOT FOUND
    < Server: Werkzeug/2.2.2 Python/3.11.2
    < Date: Tue, 07 Jan 2025 15:55:44 GMT
    < Content-Type: application/json
    < Content-Length: 46
    < Connection: close
    < 
    {
    "error": "not found",
    "status": false
    }
    * Closing connection 0
    curl: (22) The requested URL returned error: 404

Logging de icap-detect quand on le requête :

    c-icap-client -i 127.0.0.1 -p 1344 -v -f samples/legit-nocache.json

    /srv/icap-detect -verbose -timeout=3s --token=00000000-00000000-00000000-00000000-00000000 --host http://127.0.0.1:5000
    ...
    {"level":"error","msg":"err: invalid response from endpoint, 404 NOT FOUND: {\n  \"error\": \"not found\",\n  \"status\": false\n}\n","time":"2025-01-07T16:04:19Z"}

Dans le log de l'appli mock api, je n'ai que le test de cache, et aucun submit derrière alors qu'on a un cache miss

    127.0.0.1 - - [07/Jan/2025 16:04:19] "GET /api/lite/v2/search/d914176fd50bd7f565700006a31aa97b79d3ad17cee20c8e5ff2061d5cb74817 HTTP/1.1" 404 -

### Cas "contournment" : en retournant du html

Si la réponse de l'appli de mock api est la suivante pour le cache miss :

    curl --fail-with-body --verbose --request GET -H "X-Auth-Token: 00000000-00000000-00000000-00000000-00000000" localhost:5000/api/lite/v2/search/non_existing_sha256
    Note: Unnecessary use of -X or --request, GET is already inferred.
    *   Trying 127.0.0.1:5000...
    * Connected to localhost (127.0.0.1) port 5000 (#0)
    > GET /api/lite/v2/search/non_existing_sha256 HTTP/1.1
    > Host: localhost:5000
    > User-Agent: curl/7.88.1
    > Accept: */*
    > X-Auth-Token: 00000000-00000000-00000000-00000000-00000000
    > 
    < HTTP/1.1 404 NOT FOUND
    < Server: Werkzeug/2.2.2 Python/3.11.2
    < Date: Tue, 07 Jan 2025 15:57:12 GMT
    < Content-Type: text/html; charset=utf-8
    < Content-Length: 207
    < Connection: close
    < 
    <!doctype html>
    <html lang=en>
    <title>404 Not Found</title>
    <h1>Not Found</h1>
    <p>The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.</p>
    * Closing connection 0
    curl: (22) The requested URL returned error: 404

Logging de icap-detect (0.2.2) quand on le requête :

    c-icap-client -i 127.0.0.1 -p 1344 -v -f samples/legit-nocache.json

    /srv/icap-detect -verbose -timeout=3s --token=00000000-00000000-00000000-00000000-00000000 --host http://127.0.0.1:5000
    ...
    {"level":"info","msg":"file 3a874173-3a3f-4813-b36f-186150a891f9 is not a malware: false (0)","time":"2025-01-07T16:05:51Z"}

Et j'ai bien une série de requetes dans l'api mock :

    127.0.0.1 - - [07/Jan/2025 16:05:51] "GET /api/lite/v2/search/d914176fd50bd7f565700006a31aa97b79d3ad17cee20c8e5ff2061d5cb74817 HTTP/1.1" 404 -
    127.0.0.1 - - [07/Jan/2025 16:05:51] "GET /api/lite/v2/search/d914176fd50bd7f565700006a31aa97b79d3ad17cee20c8e5ff2061d5cb74817 HTTP/1.1" 404 -
    submission: identifier=UUID('3a874173-3a3f-4813-b36f-186150a891f9') sha256='d914176fd50bd7f565700006a31aa97b79d3ad17cee20c8e5ff2061d5cb74817' timestamp=1736265951
    127.0.0.1 - - [07/Jan/2025 16:05:51] "POST /api/lite/v2/submit HTTP/1.1" 200 -
    127.0.0.1 - - [07/Jan/2025 16:05:51] "GET /api/lite/v2/results/3a874173-3a3f-4813-b36f-186150a891f9 HTTP/1.1" 200 -
    127.0.0.1 - - [07/Jan/2025 16:05:51] "GET /api/lite/v2/results/3a874173-3a3f-4813-b36f-186150a891f9 HTTP/1.1" 200 -
