## Day 32 — QoS Controlled Testing

Today I continued ROS2 QoS testing.

### Main QoS ideas

* Reliability: how message delivery is handled.
* Durability: whether late subscribers receive earlier retained messages.
* History: which messages are stored.
* Depth: how many messages `KEEP_LAST` stores.

The publisher offers QoS, and the subscriber requests QoS. They do not always need to be identical, but the publisher must satisfy the subscriber’s request.

### Reliability test

```text
BEST_EFFORT publisher
RELIABLE subscriber
→ incompatible
→ no messages received
```

A `RELIABLE` publisher can satisfy a `BEST_EFFORT` subscriber, but not the opposite.

### Durability test

```text
VOLATILE publisher
TRANSIENT_LOCAL subscriber
→ incompatible
```

A `TRANSIENT_LOCAL` publisher can satisfy a `VOLATILE` subscriber.

I published one message using a `TRANSIENT_LOCAL` publisher and started the subscriber afterward.

The `TRANSIENT_LOCAL` subscriber received the old message, while the `VOLATILE` subscriber stayed blank.

This proved that durability controls late-subscriber message behaviour.

### History and depth test

I created:

```text
qos_depth_test_publisher
qos_depth_test_subscriber
```

Both used:

```text
RELIABLE
KEEP_LAST
depth = 5
VOLATILE
```

The publisher sent about 100 messages per second. The subscriber processed about one message per second.

Received values jumped like:

```text
20924
21025
21125
21225
```

This showed genuine queue pressure and that many old intermediate messages were skipped.

For robot sensors, recent information is more useful than processing hundreds of old readings because people and obstacles continuously move.

The exact five internal queue positions were configured in code but were not directly displayed.
