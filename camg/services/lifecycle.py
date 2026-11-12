"""Best-effort cleanup of every owned episode, with failures reported together."""
import logging


def close_all(identifiers, close, exists):
    failures = []
    for identifier in identifiers:
        try:
            close(identifier)
        except KeyError as exc:
            # An idle reaper may close an episode after the shutdown snapshot.
            if exists(identifier):
                failures.append((identifier, exc))
                logging.exception("Episode %s failed to close", identifier)
        except Exception as exc:
            failures.append((identifier, exc))
            logging.exception("Episode %s failed to close", identifier)
    if failures:
        raise RuntimeError(f"Could not close {len(failures)} owned episodes; inspect service logs") from failures[0][1]
