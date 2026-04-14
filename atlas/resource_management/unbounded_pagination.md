# [FM-005] Unbounded Pagination State Amplification
**Pattern:** Resource Management

**The Failure**
An unauthenticated user can crash a server by simply requesting the first page of a search result thousands of times. If the server stores "pagination cursors" in memory for every request, it will eventually run out of RAM (OOM).

**Mechanism**
"State Amplification". The cost to the attacker is a tiny HTTP request. The cost to the server is a durable memory allocation (the cursor). Without a global limit or TTL on these cursors, the memory usage grows monotonically with the request rate.

**Reproduction**
```python
# Attacker sends many requests
for _ in range(1000000):
    # Each request forces the server to create and store a cursor
    requests.get("/api/items?page=1")

# Server Memory:
# [Cursor1, Cursor2, ..., Cursor1000000] -> OOM!
```
Full reproduction: `lab/resource_management/unbounded_pagination/`

**Remediation**
1. **Stateless Cursors**: Encode the state (like the last ID seen) into an encrypted/signed token sent to the client (JWT-style).
2. **Bounded Registry**: If state must be server-side, use a fixed-size LRU cache with a global memory limit and strict TTL.
