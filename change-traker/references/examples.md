---
description: >-
  Real-world examples of `change-traker` logs for TypeScript and Rust codebases.
metadata:
  tags: [examples, typescript, rust]
  source: internal
---

# `change-traker` Real-World Examples

Below are concrete, high-fidelity examples showing how changes in TypeScript and Rust codebases should be logged using this skill.

---

## 💻 TypeScript Example: Bug Fix & Soft-Delete Soft-Crash

```markdown
## 2026-05-25 18:50:00 UTC+05:30 - Fix soft-delete race condition on APIProxy

> [!NOTE]
> **Change Type:** Bug Fix
> **Status:** Complete
> **Target Files:**
> - `src/proxy/apiProxy.ts`
> - `tests/proxy/apiProxy.test.ts`

### 🔍 Context & Objective
* **Why this change?** Intermittent race condition where deleted proxies were queried during initialization because the deleted flag was checked after caching rather than before.
* **What problem is solved?** Resolves `NullReferenceException` in proxy validation router during concurrent active agent handshakes.

### 🛠️ Implementation Summary
- [x] Moved `isDeleted` validation to the beginning of the `getProxyInstance` cache lookup.
- [x] Added unit tests mocking concurrent handshakes with a deleted proxy instance to ensure proper rejection.

### 🔄 Code Differences (Before vs After)

#### 📄 `src/proxy/apiProxy.ts`
```diff
@@ -42,8 +42,12 @@
   public async getProxyInstance(id: string): Promise<ProxyInstance | null> {
-    const cached = this.cache.get(id);
-    if (cached) return cached;
-    
     const instance = await this.db.fetch(id);
+    if (!instance || instance.isDeleted) {
+      this.logger.warn(`Proxy ${id} is deleted or does not exist.`);
+      return null;
+    }
+
+    const cached = this.cache.get(id);
+    if (cached) return cached;
```

#### 📄 `tests/proxy/apiProxy.test.ts`
```diff
@@ -118,3 +118,14 @@
+  it('should return null and warn if proxy is soft-deleted', async () => {
+    const mockDb = { fetch: vi.fn().mockResolvedValue({ id: 'p1', isDeleted: true }) };
+    const proxy = new ApiProxy(mockDb as any);
+    const result = await proxy.getProxyInstance('p1');
+    expect(result).toBeNull();
+  });
```
---
```

---

## 🦀 Rust Example: Refactor & Thread-Safe Logging Cache

```markdown
## 2026-05-25 19:15:30 UTC+05:30 - Refactor PII cache utilizing Arc<RwLock> for thread safety

> [!WARNING]
> **Change Type:** Refactor
> **Status:** Partial (Integration tests still pending validation under load)
> **Target Files:**
> - `src/shield/cache.rs`

### 🔍 Context & Objective
* **Why this change?** Transitioning the single-threaded PII redaction cache to a multi-threaded safe cache using `std::sync::RwLock` instead of a raw `RefCell`.
* **What problem is solved?** Eliminates thread starvation and `RefCell` borrowing panics when scaling concurrent network requests beyond the 100ms latency budget.

### 🛠️ Implementation Summary
- [x] Replaced `RefCell<HashMap<String, String>>` with `Arc<RwLock<HashMap<String, String>>>`.
- [x] Implemented proper `.read()` and `.write()` lock handling with descriptive error messages in case of poisoning.

### 🔄 Code Differences (Before vs After)

#### 📄 `src/shield/cache.rs`
```diff
@@ -10,9 +10,12 @@
 pub struct PiiCache {
-    store: RefCell<HashMap<String, String>>,
+    store: Arc<RwLock<HashMap<String, String>>>,
 }

 impl PiiCache {
     pub fn get(&self, key: &str) -> Option<String> {
-        self.store.borrow().get(key).cloned()
+        self.store
+            .read()
+            .expect("PII cache lock poisoned on read")
+            .get(key)
+            .cloned()
     }
```
---
```
```
