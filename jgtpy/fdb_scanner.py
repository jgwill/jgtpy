import JGTCDS as cds


def scan_fdb(instruments, timeframes, quiet=False):
    """Scan FDB signals for given instruments and timeframes."""
    results = []
    for inst in instruments:
        for tf in timeframes:
            try:
                has_signal = cds.checkFDB(inst, tf)
            except Exception as exc:
                if not quiet:
                    print(f"Error scanning {inst}_{tf}: {exc}")
                has_signal = False
            results.append({"instrument": inst, "timeframe": tf, "fdb": has_signal})
    return results
