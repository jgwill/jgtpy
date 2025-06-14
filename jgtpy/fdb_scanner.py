import JGTCDS as cds
from concurrent.futures import ThreadPoolExecutor


def scan_fdb(instruments, timeframes, quiet=False, workers=5):
    """Scan FDB signals for given instruments and timeframes concurrently."""

    def _scan(inst, tf):
        try:
            signal = cds.checkFDB(inst, tf)
        except Exception as exc:  # pragma: no cover - defensive
            if not quiet:
                print(f"Error scanning {inst}_{tf}: {exc}")
            signal = False
        return {"instrument": inst, "timeframe": tf, "fdb": signal}

    results = []
    with ThreadPoolExecutor(max_workers=workers) as exe:
        futures = [exe.submit(_scan, inst, tf) for inst in instruments for tf in timeframes]
        for fut in futures:
            results.append(fut.result())

    return results
