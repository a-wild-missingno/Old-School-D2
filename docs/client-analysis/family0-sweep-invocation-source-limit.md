# Family-zero sweep invocation source limit

## Question

Can the authorized Sunrise source identify the predecessor or eligibility condition that invokes the native family-zero sweep in the known-good path but not in the external black-screen path?

## Source result

No. The authorized client source identifies the family-zero sweep only through one unique runtime image signature. The hook attaches its observer to that native target, decodes the target's source-list getter from the target's internal call operand, and then defers to the original native sweep. It contains no source-level caller, scheduler, transition predicate, or state-machine predecessor for that target.

The current-reference branch and every retained external validation lineage have the same family-zero subscription source file. Their file identity is unchanged across the examined upstream baseline, service-29 trace, fresh external trace, and current reference branches. The only reviewed divergence in this area is the later source-list key fallback; it is downstream of the now-confirmed non-invocation of the sweep.

## Evidence boundary

The controlled aggregate observer established that the native sweep did not execute during the bounded external run even though the hook attached. That is runtime evidence of non-invocation, not evidence of why the native caller declined to invoke it. The source supplies no unique predecessor from which to infer the missing condition.

## Conclusion

**COMPLETE / SOURCE LIMIT.** No further source-only change or live probe is justified for this target. Repeating the observer, porting the fallback, or fabricating Queuez/server state would not identify the invocation gate.

The next potentially falsifiable route is separately scoped offline analysis of the locally installed historical executable to recover bounded static callers or control-flow predecessors for the uniquely matched native sweep. That work must remain read-only, derive no proprietary payload/identity data, and receive its own explicit authorization before execution.
