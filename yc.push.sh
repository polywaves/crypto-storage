#!/bin/bash

REGISTRY_ID="crphroudu03lidop4gfn"
REGISTRY_IMAGE="crypto-storage"
REGISTRY_TAG="latest"

docker build . \
  -t cr.yandex/$REGISTRY_ID/$REGISTRY_IMAGE:$REGISTRY_TAG
docker tag $REGISTRY_IMAGE:$REGISTRY_TAG \
  cr.yandex/$REGISTRY_ID/$REGISTRY_IMAGE:$REGISTRY_TAG
docker push cr.yandex/$REGISTRY_ID/$REGISTRY_IMAGE:$REGISTRY_TAG