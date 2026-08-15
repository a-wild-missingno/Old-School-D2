# Experiment: Sunrise external-server baseline

Date:
Researcher:
Status: planned

## Question

When the supported Sunrise external-server mode is enabled, which transport connections and datagrams does the historical client attempt to send to the isolated lab listener?

## Safety pre-check

- [ ] Client isolation from WAN was verified immediately before launch.
- [ ] Lab gateway IPv4 and IPv6 forwarding are disabled.
- [ ] No NAT, proxy, or route can provide WAN access to client traffic.
- [ ] Capture is running on the physical lab LAN interface.
- [ ] DNS logging is running, even though Sunrise may redirect relevant resolver calls locally.
- [ ] The client is stopped before configuration is changed.
- [ ] The external target is a lab-owned listener, not a production endpoint.

## Configuration record

Record sanitized values only. Do not commit private addresses, hostnames, paths, identifiers, or credentials.

- Sunrise upstream revision or release:
- Working fork revision:
- `client.external_server.enabled`:
- Lab listener role and exposed ports:
- Capture file identifier or sanitized summary:

## Expected behavior

The external-server setting redirects guarded client egress to one configured lab host before it reaches the network. Captured packets therefore identify the lab listener rather than the original remote service. The observation goal is transport sequencing and request shape, not contact with external infrastructure.

## Observation

- First observed connection or datagram:
- Transport and destination port:
- Retry interval or timeout behavior:
- TLS, framing, or payload metadata:
- Client-visible result:

## Evidence

Link only to sanitized summaries, decoded metadata, source paths, or non-sensitive hashes. Do not commit raw PCAP files by default.

## Hypothesis


## Test

Use a minimal fail-closed listener first. Document any response separately before sending it.

## Result


## Confidence

Confirmed | High | Medium | Low

## Follow-up
