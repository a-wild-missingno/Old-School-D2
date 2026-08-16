# External post-BAP transition baseline

Fresh isolated controlled client launch window: 2026-08-15T21:46:00Z through 2026-08-15T21:48:00Z.

Redacted transition ledger:

```json
{"event_count":30,"outcome":"post_bap_transition_absent","services":[30,25,121,302,304,302,250],"responses":[31,26,122,303,305,251]}
```

The displayed service lists are unique ordered route types, not raw packet data. The client completed SignOn, content configuration, the documented BAP bootstrap routes, and keepalive handling. It did not issue any later route in this interval. The ledger contains no HTTPS request content, BAP body bytes, tokens, session values, peer addresses, or account/character identifiers.
