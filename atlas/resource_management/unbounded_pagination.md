[<- Index](../../README.md)
# [FM-005] Unbounded Pagination State Amplification
**Pattern:** Resource Management

**The Failure**
An unauthenticated user can crash a server by simply requesting the first page of a search result thousands of times. If the server stores "pagination cursors" in memory for every request, it will eventually run out of RAM (OOM).

**Mechanism**
"State Amplification". The cost to the attacker is a tiny HTTP request. The cost to the server is a durable memory allocation (the cursor). Without a global limit or TTL on these cursors, the memory usage grows monotonically with the request rate.

**Coding Example**
```python
cursor_registry = {}


def handle_page_request_unsafe(request_id, page_number):
    if page_number == 1:
        cursor_state = build_large_server_side_cursor(request_id)
        cursor_registry[request_id] = cursor_state

    # BUG:
    # no global limit
    # no eviction
    # no expiry


for request_id in many_cheap_requests():
    handle_page_request_unsafe(request_id, page_number=1)

len(cursor_registry)
# grows without bound -> FAILURE:
# tiny requests force durable memory allocation


def handle_page_request_safe(request_id, page_number):
    if page_number == 1:
        cursor_state = build_cursor_state(request_id)
        store_cursor_in_bounded_registry(cursor_state)

    return maybe_return_stateless_cursor_token()
```

**Invariant Violated**
Per-request pagination state must remain globally bounded in memory.

**Remediation**
1. **Stateless Cursors**: Encode the state (like the last ID seen) into an encrypted/signed token sent to the client (JWT-style).
2. **Bounded Registry**: If state must be server-side, use a fixed-size LRU cache with a global memory limit and strict TTL.

**Invariant Restored**
Cursor storage has an explicit upper bound or is moved out of server memory entirely. Cheap client requests can no longer force unbounded durable allocations.

**References**

- [libp2p Advisory](https://github.com/advisories/GHSA-v5hw-cv9c-rpg7)
- [CVE-2026-35457](https://nvd.nist.gov/vuln/detail/CVE-2026-35457)