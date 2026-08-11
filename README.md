# Old-School-D2

Old-School-D2 is an experimental research project to understand how historical Destiny 2 clients interacted with their online service infrastructure, with the long-term hope of documenting and eventually building clean-room replacement services for offline or preservation-focused PvE experiences.

The immediate goal is not to make the game work. The first milestone is a safe, reproducible network-isolation and observation environment.

## Current milestone: isolated network discovery

Before any protocol emulation work begins, the client machine must be isolated from Bungie and the public Internet while still allowing a controlled lab machine to observe the client's attempted network traffic.

The intended topology is:

```text
Historical Destiny client
        |
        v
Lab gateway + DNS logger
        |
        X no forwarding / no NAT / no WAN access for client traffic
```

The lab gateway acts as the client's configured gateway and DNS server. This lets us observe packets whose original destinations are remote addresses, including both DNS-discovered services and hard-coded IP destinations, without forwarding those packets to the real services.

## Safety principles

- Do not allow the historical client to contact Bungie infrastructure.
- Do not forward, NAT, proxy, or tunnel client traffic to the public Internet.
- Do not blindly wildcard DNS.
- Do not forward Destiny/Bungie-related DNS queries upstream unless explicitly reviewed and approved.
- Do not make router changes without first documenting the router, proposed change, and rollback plan.
- Do not implement speculative server behavior before baseline captures are complete.
- Prefer reversible, local, documented changes.
- Keep observed facts separate from hypotheses.

## DNS discovery strategy

Initially, DNS is used for discovery only.

The DNS logger should record:

- timestamp
- requesting client
- query sequence
- hostname
- query type
- response behavior

Unknown names may safely fail resolution during early discovery. Once specific services are identified and selected for emulation, individual hostnames can be mapped to the lab gateway. Mappings should be narrow, reviewed, and documented.

## Packet capture strategy

The lab gateway should capture all traffic originating from the isolated client while preserving original destination information.

Captures should support analysis of:

- destination IPs
- destination ports
- protocols
- connection order
- retry intervals
- TCP resets
- TLS negotiation attempts
- DNS activity
- persistent versus short-lived connections
- UDP flows
- packet sizes
- timing relationships

Raw captures may contain sensitive local-network information and should be reviewed before publication.

## Research workflow

### Phase 1: Network discovery

Launch the historical client only after isolation has been experimentally verified. Capture a complete startup attempt and build an endpoint inventory including:

- hostname, if DNS-based
- resolved IP, if applicable
- hard-coded IP, if suspected
- protocol and port
- TCP or UDP
- order during startup
- retry behavior
- whether failure blocks further startup
- whether the connection appears optional
- observable TLS metadata
- likely purpose
- confidence level

### Phase 2: Static client analysis

Analyze client files for network and service architecture references, such as:

- hostnames and URLs
- IP literals and ports
- protocol names
- serialization formats
- message identifiers
- service names
- error messages
- authentication and session state-machine hints
- matchmaking, activity, world, or destination terminology
- configuration files and manifests
- TLS or HTTP client usage
- socket and DNS resolution code

The goal is understanding expected interfaces, not bypassing protections or contacting real services.

### Phase 3: Controlled fake services

Create small local listeners for identified endpoints. Begin with the smallest possible behavior:

1. accept a connection
2. record the first bytes or message
3. optionally return a controlled failure or minimal response
4. observe how the client reacts

Every experiment should document:

- client state before experiment
- endpoint
- request bytes or structure
- response supplied
- resulting client behavior
- logs or packet evidence
- hypothesis
- confidence

### Phase 4: Selective DNS substitution

Map only identified hostnames that are intentionally being intercepted. Avoid wildcard DNS and unrelated names.

### Phase 5: Narrow transparent interception

If the client uses hard-coded IPs, cached addresses, or non-DNS discovery, use narrowly scoped interception rules only for specific destinations and ports. Do not forward intercepted connections to real remote destinations.

### Phase 6: Protocol documentation

For each identified protocol, maintain independent documentation covering:

- transport
- framing
- byte order
- compression
- serialization
- message IDs
- request fields
- response fields
- state transitions
- unknown fields
- observed examples
- confidence level

Observed facts and hypotheses should be clearly separated.

### Phase 7: Clean-room replacement services

Implement independently written services from the protocol documentation. Do not copy Bungie code, assets, or proprietary data.

### Phase 8: Minimal boot milestone

The first meaningful milestone should be modest, such as the client advancing farther than before after contacting controlled replacement infrastructure. Larger gameplay goals should wait until the protocol surface is understood.

## Repository rules

This repository is public. Do not commit:

- Destiny binaries
- Bungie assets
- extracted cinematics
- extracted audio
- textures or models
- copyrighted configuration dumps where redistribution would be inappropriate
- encryption or signing keys
- credentials or account tokens
- raw packet captures containing sensitive local-network data
- machine-specific LAN details such as private IP addresses, hostnames, MAC addresses, or router details

Generated technical metadata should be reviewed before committing.

## Documentation structure

Planned organization:

```text
docs/
  network/              Network lab design, verification, and capture notes
  protocols/            Protocol notes and independent specifications
  experiments/          Experiment logs with evidence and confidence levels
  client-analysis/      Static-analysis notes and references
tools/
  capture/              Capture and summary helpers
  dns/                  DNS logging and selective mapping tools
  protocol-analysis/    Parsers, decoders, and analysis utilities
server/
  gateway/              Local gateway/listener components
  auth/                 Clean-room auth/session experiments
  profile/              Profile-related experiments
  world/                World/activity experiments
```

## Status

Preparation is in progress. The current work is limited to network-isolation planning, DNS logging, packet-capture tooling, and reproducible documentation. Destiny client startup capture should not begin until isolation tests have passed.
