# In-process character-signin probe result

Status: COMPLETE — unique target, zero direct rel32 callers, black screen unchanged

Windows CI run 32578816582 built the source probe successfully. The dedicated external-trace DLL deployed with SHA-256 `4664163200278bcb214307c7fe12126fc5f5ac5f9ecde9aacf88db5a71c130d2`. The user pressed Enter once and again observed the persistent black screen without a visible error.

The once-only in-process event was:

```text
ev=external_trace stage=character_signin_image matches=1 direct_callers=0
```

Thus Sunrise's own executable image uniquely contains the handler target, resolving the external-reader mismatch. It has no direct `E8 rel32` callers in the bounded scan; this does not exclude indirect/vtable/tail-call paths. The client still completed SignOn, ContentConfig, authenticated BAP, repeated no-reply service 29, and keepalives without service 10.

Cleanup completed: Destiny, listeners, and capture stopped; forwarding disabled and public HTTPS blocked; protected external-validation hashes unchanged. No new causal mechanism is established.
