Unbounded rendezvous DISCOVER cookies enable remote memory exhaustion

Atlas mapping:
- failure pattern: `atlas/FP_005_unbounded_pagination_cookie_state_amplification.md`
- lab reproduction: `lab/failure_modes/FM_005_unbounded_pagination_state/`
- guardrail: `guardrails/GR_005_bounded_pagination_state.md`
- canonical postmortem: `postmortems/PM_005_unbounded_pagination_state.md`

### Summary
The rendezvous server stores pagination cookies without bounds.
An unauthenticated peer can repeatedly issue `DISCOVER` requests and force unbounded memory growth.

This incident is now maintainer-confirmed via GitHub advisory [`GHSA-v5hw-cv9c-rpg7`](https://github.com/libp2p/rust-libp2p/security/advisories/GHSA-v5hw-cv9c-rpg7)
and [`CVE-2026-35457`](https://github.com/advisories/GHSA-v5hw-cv9c-rpg7) (published April 4, 2026).

### Details

Pagination state is stored in:

```rs
HashMap<Cookie, HashSet<RegistrationId>>
```

On `Message::Discover`:

```
remote peer
→ DISCOVER
→ handle_request
→ registrations.get(...)
→ new cookie generated
→ cookie inserted into Registrations::cookies
```

There is **no upper bound or eviction policy**, so repeated DISCOVER requests grow this map indefinitely.


### PoC
A deterministic reproduction now lives in
`lab/failure_modes/FM_005_unbounded_pagination_state/`.
Use `tests/test_repro_fm005.py` for the failing baseline and
`tests/test_prevent_fm005.py` for the containment proof.

### Impact

**Remote state amplification leading to memory exhaustion.**


Properties:

- network reachable
- no authentication required
- low attack complexity
- protocol-compliant traffic

Impacts rendezvous nodes exposed to untrusted peers.
---

### Possible Fixes

1. **Global cap + eviction**

Bound cookie storage (`MAX_COOKIES_TRACKED`) with FIFO/expiry aware eviction.  
Tradeoff: attacker can churn cookies and evict legitimate pagination state.

2. **Stateless cookies**

Encode pagination state in authenticated cookies instead of storing server-side state.  
Tradeoff: more complex implementation.

3. **Rate limiting / per-peer quotas**

Limit cookie creation per peer.  
Tradeoff: requires peer tracking.

### External confirmation

- Maintainer advisory: `GHSA-v5hw-cv9c-rpg7`
- CVE: `CVE-2026-35457`
- Published: April 4, 2026

### References

- GitHub advisory: <https://github.com/libp2p/rust-libp2p/security/advisories/GHSA-v5hw-cv9c-rpg7>

status: confirmed by maintainers; mapped to FP_005 / FM_005 / GR_005 / PM_005
