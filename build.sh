#!/bin/bash

FAIL=0
echo "Starting buildings..."

docker buildx build \
  --tag akeb/calibre-telegram-bot:latest \
  --platform linux/amd64,linux/arm64 \
  . && \
  docker push akeb/calibre-telegram-bot:latest

for job in `jobs -p`
do
   wait $job || let "FAIL+=1"
done

if [ "$FAIL" == "0" ];
then
    echo "All jobs completed!"
else
    echo "Jobs FAILED: ($FAIL)"
fi
