# AceCoin ElectrumX integration

This directory provides the ElectrumX server integration layer for AceCoin.

## Important protocol boundary

ElectrumX is for UTXO-style native blockchains. The current repository is a coin-development framework and does not yet contain a native UTXO chain daemon. The integration therefore implements the Bitcoin-like ElectrumX adapter and deployment contract, while chain-specific consensus values must be supplied by the future AceCoin Core implementation.

The adapter assumes:
- JSON-RPC compatible full node
- non-pruned node
- `txindex=1`
- Bitcoin-style 80-byte block headers
- double-SHA256 block hashes
- Bitcoin-style transaction serialization
- Base58Check P2PKH/P2SH addresses
- 100,000,000 base units per ACE

If AceCoin Core uses different serialization, hashing, address encoding, or consensus rules, the Coin class and deserializer must be changed before production.

## Deployment

1. Build the image from `electrumx/docker/Dockerfile`.
2. Copy `.env.testnet.example` to `.env.testnet` and replace all placeholder RPC credentials and chain values.
3. Place a CA-issued or pinned self-signed certificate in `electrumx/certs/server.crt` and `server.key`.
4. Start with `docker compose --env-file .env.testnet -f electrumx/docker-compose.testnet.yml up -d --build`.
5. Wait for ElectrumX to finish its initial sync before connecting a wallet. ElectrumX intentionally does not accept normal client connections until caught up.

## Required AceCoin Core RPC methods

The daemon must provide the methods ElectrumX's generic daemon/block processor expects, including block retrieval, raw transaction retrieval, chain height, mempool and transaction broadcast. The exact RPC surface is validated during the integration test.

## Security

- Never expose the Core RPC port publicly.
- Expose only TCP/SSL Electrum service ports.
- Prefer SSL on 50002; plaintext TCP is disabled in the default compose file.
- Keep RPC credentials in environment/secrets, never Git.
- Put the database on persistent SSD-backed storage.

See the upstream ElectrumX documentation for environment variables, services, database engines and TLS configuration.
