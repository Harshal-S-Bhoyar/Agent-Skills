# @loop Edge Case Strategies

Progressive edge case tiers — adapt to your task type.

---

## Universal Tiers

| Tier | Iters | Focus |
|------|-------|-------|
| Foundation | 1-2 | Happy path. Does it work at all? |
| Boundaries | 3-5 | Empty, null, max length, special chars, duplicates |
| Stress | 6-10 | Volume, concurrency, timeouts, memory pressure |
| Adversarial | 11-15 | Injection, overflow, race conditions, auth edge cases |
| Exotic | 16-20 | Platform quirks, timezone, locale, crash recovery |

---

## By Task Type

### Testing a Feature
- **1-2**: Valid inputs, expected outputs, basic success
- **3-5**: Empty/null, unicode/emoji, boundary values, whitespace-only
- **6-10**: Rapid calls, concurrent access, large payloads, slow network
- **11-15**: SQL injection, XSS, path traversal, expired auth, double-submit
- **16-20**: Timezone DST, locale decimal formats, network disconnect mid-op

### Building a Feature
- **1-2**: Core logic with test data, correct output shape
- **3-5**: Error handling, loading/empty states, permission checks
- **6-10**: Realistic data volume, no N+1 queries, resource cleanup
- **11-15**: Injection safety, CSRF/XSS, rate limiting, dependency failure
- **16-20**: Offline/reconnect, migration compat, accessibility

### Fixing a Bug
- **1-2**: Reproduce exact bug, verify fix resolves it
- **3-5**: Variations of trigger, regression check, old+new data
- **6-10**: Bug under load, no perf regression, concurrent triggers
- **11-15**: Alternative code paths to same bug, similar bugs in related code
- **16-20**: Cross-platform, survives restart, forward-compatible

### Optimizing Performance
- **1-2**: Measure baseline with realistic data, identify actual bottleneck
- **3-5**: Empty/min/max dataset, cold vs warm cache
- **6-10**: Sustained load (memory leaks?), concurrent requests, GC pressure
- **11-15**: Pathological inputs, cache-busting, degraded dependencies
- **16-20**: Cross-region latency, different hardware, JIT cold/hot paths

---

## Edge Case Generation Heuristics

When you run out of predefined cases, use these:

1. **Invert assumptions**: What if the opposite were true?
2. **Boundary ±1**: Test at limit, limit-1, limit+1
3. **Empty/null/missing**: What if the input is absent entirely?
4. **Type confusion**: Wrong type — string instead of number?
5. **Timing**: Out of order? Delay? Simultaneous?
6. **Scale**: 0 items? 1 item? 1 million?
7. **State**: Partially initialized? Mid-migration? Post-crash?
8. **Dependencies**: External service down, slow, or returning garbage?
9. **Identity**: Wrong user, expired token, different tenant?
10. **Composition**: Two valid operations that conflict when combined?
