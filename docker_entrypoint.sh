#!/usr/bin/env bash
set -eo pipefail

if [[ -z $MESSAGE ]]
then
    signer --p2p-secret-path "$P2P_SECRET_PATH"
else
    signer --message "$MESSAGE" --p2p-secret-path "$P2P_SECRET_PATH"
fi

echo "Done!"
