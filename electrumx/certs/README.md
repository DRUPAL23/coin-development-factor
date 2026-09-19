# TLS certificates

Do not commit private keys.

For local testnet, generate a certificate whose hostname matches the Electrum
server name used by your client:

```bash
./electrumx/scripts/generate-testnet-cert.sh electrum-testnet.example.org
```

This creates `server.crt` and `server.key` in this directory.

For production, use a certificate issued by a trusted CA or use the wallet's
documented certificate pinning workflow. Back up the private key securely.
