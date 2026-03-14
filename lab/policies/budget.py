from __future__ import annotations

from collections import OrderedDict
from dataclasses import dataclass


@dataclass(frozen=True)
class RetryBudget:
    """Deterministic retry budget used to cap retry storms."""

    max_attempts: int

    def allows(self, attempt: int) -> bool:
        return attempt <= self.max_attempts


class CookieRegistry:
    """Deterministic server-side cookie registry with optional FIFO budget enforcement."""

    def __init__(self, *, max_entries: int) -> None:
        if max_entries < 0:
            raise ValueError("max_entries must be >= 0")
        self.max_entries = max_entries
        self._entries: "OrderedDict[str, set[str]]" = OrderedDict()
        self.evicted_count = 0

    def insert(self, *, cookie: str, registrations: set[str], enforce_budget: bool) -> None:
        # Update-in-place for existing cookie; no growth.
        if cookie in self._entries:
            self._entries[cookie] = registrations
            return

        if enforce_budget:
            if self.max_entries == 0:
                self.evicted_count += 1
                return

            while len(self._entries) >= self.max_entries:
                self._entries.popitem(last=False)
                self.evicted_count += 1

        self._entries[cookie] = registrations

    def count(self) -> int:
        return len(self._entries)

    def cookies(self) -> list[str]:
        return list(self._entries.keys())

