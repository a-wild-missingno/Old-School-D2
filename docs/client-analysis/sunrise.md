# Sunrise integration notes

## Scope

Sunrise is the current client-side starting point for this project. These notes are derived from a source review of the public Sunrise repository and describe the behavior relevant to isolated-lab experiments. They are not a specification of the original Destiny 2 online services.

Upstream project: [stanuwu/Sunrise](https://github.com/stanuwu/Sunrise)

Working fork: [a-wild-missingno/Sunrise](https://github.com/a-wild-missingno/Sunrise)

## Why it matters for network capture

Sunrise supports two distinct operating modes that must not be conflated when interpreting captures.

### Default offline mode

The default `client.external_server.enabled` setting is `false`. In this mode Sunrise uses local handling and loopback redirection for relevant resolver, socket, HTTP, and discovery paths. This means that a packet capture on the lab gateway can correctly contain no game-originated LAN traffic even while the client is functioning.

A lack of game traffic in this mode is therefore an expected result, not evidence that gateway capture is broken.

### External-server mode

Sunrise exposes a configuration switch named `client.external_server`. When enabled, the client directs the guarded network paths to one configured numeric IPv4 host. It also rewrites game HTTP URLs to that host and delegates UDP discovery to the external target instead of answering it locally.

This is the preferred first path for a controlled transport experiment because it does not require changing the game executable or the Sunrise source. The experiment target must be a researcher-controlled listener inside the isolated lab.

## Interpretation limits

External-server mode redirects destinations before packets leave the client. As a result:

- A gateway capture can reveal connection ordering, ports, TCP or UDP behavior, payload framing, retries, and timing.
- The captured destination is the configured lab listener, not the original remote service address.
- Original host or URL information, where available, belongs in client-side logs or static-analysis notes rather than being inferred from the redirected packet destination.
- The mode relaxes client TLS peer checks for rewritten external requests. Treat it as a lab-only setting and never point it at an unreviewed or production endpoint.

## Settings ownership

The repository contains a default settings document under `Sunrise/resources/default_settings.json`. At runtime Sunrise creates and reads a writable `settings.json` in its own artifact directory. The runtime copy is experiment configuration, not a reason to patch or fork the client for initial external-server tests.

Do not commit local settings files when they include machine paths, private addresses, tokens, or experiment-specific identifiers. Commit only sanitized examples or documentation.

## Recommended first experiment

1. Verify the client isolation controls and start packet capture.
2. Stop the client.
3. Record the exact Sunrise revision and the sanitized external-server configuration in an experiment file.
4. Enable external-server mode with a researcher-controlled lab listener.
5. Restart the client and record connection attempts, request order, retry behavior, and any local logs.
6. Keep the listener fail-closed until the first request shape is documented.

See [the experiment template](../experiments/sunrise-external-server.md).

## Source credit and boundaries

Sunrise is an independent upstream project. Preserve its attribution, license, notices, and project rules in any downstream work. Old-School-D2 documentation should describe observed behavior in original words and should not import Sunrise source code, Destiny assets, binaries, or private captures.
