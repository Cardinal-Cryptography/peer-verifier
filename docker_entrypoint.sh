#!/usr/bin/env bash
set -euo pipefail

signer --message "$PEER_ID" --p2p-secret-path "$P2P_SECRET_PATH"

echo "Done!"
