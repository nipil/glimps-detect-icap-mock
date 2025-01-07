# glimps detect mock

## How to use

    docker-compose down --rmi local

    docker-compose up

    docker exec -it glimps-detect-mock-client-1 bash

        c-icap-client -i detect -p 1344 -v -f /samples/legit-nocache.json
        c-icap-client -i detect -p 1344 -v -f /samples/cached-legit.json

        c-icap-client -i detect -p 1344 -v -f /samples/malware-nocache.json
        c-icap-client -i detect -p 1344 -v -f /samples/cached-malware.json

        c-icap-client -i detect -p 1344 -v -f /samples/too-long.json
        c-icap-client -i detect -p 1344 -v -f /samples/quota-exceeded.json

        c-icap-client -i detect -p 1344 -v -f /samples/bypass-denied.json

        c-icap-client -i detect -p 1344 -v -f /samples/internal-error.json
        c-icap-client -i detect -p 1344 -v -f /samples/invalid-file.json
        c-icap-client -i detect -p 1344 -v -f /samples/invalid-token.json
        c-icap-client -i detect -p 1344 -v -f /samples/not-found.json

See `detect-mock\README.md` for expected output.

## TODO

Tester avec le client c-icap debian 11 bullseye

Et pour guider l'intégration dans nos applications internes :

- développer un POC java en CLI
- développer un POC php en CLI

Ou simplement spécifier aux TMA :

- d'installer le package debian  `c-icap`
- de développer un worker applicatif qui lance la cli `c-icap-client` et analyse son retour
