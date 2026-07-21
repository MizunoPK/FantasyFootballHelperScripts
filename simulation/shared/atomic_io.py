"""
Atomic JSON Write

Cross-simulation primitive: write a dict as JSON to a path atomically via a
temp-file -> os.replace rename, so a crash or I/O error mid-write can never leave
the destination truncated or half-written. On any OSError/PermissionError the
orphaned .tmp is removed and the failure is re-raised as FileOperationError.

Consolidates the tmp->rename logic that was duplicated in
simulation/win_rate/config_promoter.py (_atomic_write_json) and
simulation/win_rate/SweepResultsManager.py (_save). Each caller passes its own
error_message so its exact FileOperationError wording is preserved.

Author: Kai Mizuno
"""

import json
from pathlib import Path
from typing import Optional

from utils.error_handler import FileOperationError


def atomic_write_json(data: dict, path: Path, error_message: Optional[str] = None) -> None:
    """Write `data` as JSON to `path` atomically via tmp file -> rename.

    Writes to a `.tmp` sibling with indent=2 (utf-8), then replaces it over
    `path`. json.dump defaults to ensure_ascii=True, so the written bytes are
    pure ASCII and identical regardless of the file encoding. On any
    OSError/PermissionError the orphaned .tmp is removed before re-raising.

    Args:
        data: JSON-serializable payload to write.
        path: Destination file path.
        error_message: Caller-specific prefix for the raised FileOperationError
            (the underlying exception is appended as ": {e}"). Falls back to a
            generic message when None.

    Raises:
        FileOperationError: On any OSError/PermissionError during the write.
    """
    tmp_path = path.with_suffix(".tmp")
    try:
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        tmp_path.replace(path)
    except (PermissionError, OSError) as e:
        tmp_path.unlink(missing_ok=True)
        raise FileOperationError(
            f"{error_message or f'Failed to write JSON to {path}'}: {e}"
        ) from e
