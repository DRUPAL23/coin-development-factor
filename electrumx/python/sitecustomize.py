"""Load AceCoin's ElectrumX coin classes into the ElectrumX process."""

try:
    import electrumx.coin.acecoin  # noqa: F401
except Exception as exc:  # pragma: no cover
    # Let ElectrumX produce its normal startup error while retaining the
    # original exception in stderr for diagnosis.
    import sys
    print(f"AceCoin ElectrumX registration failed: {exc}", file=sys.stderr)
