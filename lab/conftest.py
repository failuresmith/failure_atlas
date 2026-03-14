import json
from typing import Callable, Dict, Any

import pytest


@pytest.fixture
def experiment_log(tmp_path, request) -> Callable[[Dict[str, Any]], Dict[str, Any]]:
    """Shared experiment log helper for deterministic, comparable run records.

    Each test writes JSONL records under its own temporary directory. Tests call
    the returned function with structured data (inputs, observed signals). If a
    test forgets to log anything, a baseline record is emitted automatically so
    every test leaves a comparable artifact.
    """

    log_path = tmp_path / "experiment_log.jsonl"
    counter = {"i": 0}

    def _log(event: Dict[str, Any]) -> Dict[str, Any]:
        counter["i"] += 1
        record = {
            "test": request.node.nodeid,
            "sequence": counter["i"],
        }
        record.update(event)
        with log_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record, sort_keys=True) + "\n")
        return record

    yield _log

    if counter["i"] == 0:
        _log({"note": "auto-baseline"})
