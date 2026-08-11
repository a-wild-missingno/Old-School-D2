# Isolation plan

This document describes the generic network-isolation design for the lab. It intentionally omits machine-specific hostnames, private IP addresses, MAC addresses, router details, and other local-environment identifiers because the repository is public.

## Objective

The historical client must be prevented from reaching Bungie or the public Internet while a lab gateway receives and records the traffic the client attempts to send.

The lab gateway is configured as the client's default gateway and DNS server. The lab gateway must not forward or NAT client traffic to WAN.

## Required checks before client launch

1. Confirm the lab gateway's active LAN interface, subnet, gateway, and DNS settings from the live machine.
2. Confirm IP forwarding is disabled for IPv4 and IPv6.
3. Confirm no NAT or masquerade rules can forward client traffic.
4. Confirm no VPN, Docker bridge, virtualization bridge, tunnel, or other interface can accidentally route the client.
5. Confirm the client can reach the lab gateway.
6. Confirm the client cannot establish HTTPS sessions to public hosts.
7. Confirm the client cannot use arbitrary public DNS resolvers.
8. Confirm same-subnet LAN access is blocked except where explicitly allowed.
9. Confirm the lab gateway itself still has Internet access for research and package installation.
10. Start packet capture before launching the historical client.

## DNS posture

Initial DNS should be discovery-only. Unknown names should fail closed. Do not wildcard all names. Add selective mappings only after the endpoint and experiment goal are documented.

## Capture posture

Capture client traffic on the real LAN interface where practical, not only on a synthetic aggregate interface. Preserve original destination IPs and ports. Keep raw captures out of the public repository unless carefully sanitized and reviewed.

## Router changes

Do not make router changes as part of the default workflow. If router enforcement becomes necessary, document the router identity, the exact proposed rule, expected effect, and rollback before making changes.
