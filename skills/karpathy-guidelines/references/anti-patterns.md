# Anti-Patterns Reference

Concrete examples of the most common LLM coding mistakes, with before/after fixes. Organized by the rule they violate.

---

## Over-Engineering
*Violates Rule 2 — Simplicity First*

### AP-01: Unnecessary Abstraction Layers

**Task:** "Add a function that returns the user's full name."

❌ **Bad — LLM over-engineers it:**
```python
from abc import ABC, abstractmethod
from typing import Protocol

class NameStrategy(Protocol):
    def format(self, first: str, last: str) -> str: ...

class FullNameStrategy:
    def format(self, first: str, last: str) -> str:
        return f"{first} {last}"

class NameFormatter(ABC):
    def __init__(self, strategy: NameStrategy):
        self._strategy = strategy
    
    @abstractmethod
    def get_name(self, user: dict) -> str: ...

class UserNameFormatter(NameFormatter):
    def get_name(self, user: dict) -> str:
        return self._strategy.format(user["first_name"], user["last_name"])

# Usage
formatter = UserNameFormatter(FullNameStrategy())
name = formatter.get_name(user)
```

✅ **Good — minimum code that solves the problem:**
```python
def get_full_name(user: dict) -> str:
    return f"{user['first_name']} {user['last_name']}"
```

**What went wrong:** The LLM anticipated "future flexibility" for different name formats. There was no such requirement. One function. Done.

---

### AP-02: Gratuitous Configuration

**Task:** "Write a function to send a welcome email."

❌ **Bad:**
```python
class EmailConfig:
    def __init__(
        self,
        subject_prefix: str = "[Welcome]",
        greeting_style: str = "formal",  # "formal" | "casual" | "custom"
        include_signature: bool = True,
        retry_on_failure: bool = True,
        max_retries: int = 3,
        retry_delay_seconds: float = 1.0,
        template_engine: str = "jinja2",  # "jinja2" | "mako" | "none"
        log_level: str = "INFO",
    ):
        ...

def send_welcome_email(user: User, config: EmailConfig = EmailConfig()) -> bool:
    ...
```

✅ **Good:**
```python
def send_welcome_email(user: User) -> None:
    subject = "Welcome to the platform"
    body = f"Hi {user.first_name}, welcome aboard!"
    send_email(to=user.email, subject=subject, body=body)
```

**What went wrong:** The task had one use case. Configuration parameters are debt — each one needs documentation, testing, and future maintenance. Add them when a real requirement demands them.

---

### AP-03: Premature Interface Extraction

**Task:** "Write a function to read a config file."

❌ **Bad:**
```python
class ConfigReader(ABC):
    @abstractmethod
    def read(self, path: str) -> dict: ...

class JSONConfigReader(ConfigReader):
    def read(self, path: str) -> dict:
        with open(path) as f:
            return json.load(f)

class YAMLConfigReader(ConfigReader):  # Not needed yet
    def read(self, path: str) -> dict:
        with open(path) as f:
            return yaml.safe_load(f)

class ConfigReaderFactory:  # Definitely not needed
    @staticmethod
    def create(format: str) -> ConfigReader:
        return {"json": JSONConfigReader, "yaml": YAMLConfigReader}[format]()
```

✅ **Good:**
```python
def read_config(path: str) -> dict:
    with open(path) as f:
        return json.load(f)
```

**Rule:** Create an abstraction when you have 2+ concrete implementations **right now**. "We might support YAML later" is speculation.

---

## Scope Creep
*Violates Rule 3 — Surgical Changes*

### AP-04: Silent Refactoring

**Task:** "Fix the off-by-one error in `calculate_discount`."

❌ **Bad — LLM "improves" the whole file:**
```python
# LLM rewrites the entire function, renames variables,
# adds type hints throughout, reformats docstring,
# extracts a helper method, AND fixes the bug
def calculate_discount(price: float, rate: float) -> float:
    """
    Calculate the discounted price.
    
    Args:
        price: Original price in dollars
        rate: Discount rate between 0 and 1
        
    Returns:
        Discounted price
    """
    validated_rate = max(0.0, min(1.0, rate))  # new
    discount_amount = _compute_discount_amount(price, validated_rate)  # new helper
    return price - discount_amount
```

✅ **Good — one surgical fix:**
```python
# Before: return items[0:n-1]  ← off by one
# After:
return items[0:n]
```

**What went wrong:** The user asked for a bug fix. Anything beyond fixing that bug is unsolicited — it makes the diff noisy, risks introducing new bugs, and violates the user's trust that you'll do what was asked.

---

### AP-05: Unsolicited Style Modernization

**Task:** "Add a `created_at` field to the User model."

❌ **Bad:**
```python
# LLM migrates from old-style class to dataclass, adds __slots__,
# converts all string annotations to proper types, etc.
@dataclass
class User:
    id: int
    email: str
    name: str
    created_at: datetime = field(default_factory=datetime.utcnow)
    
    def __post_init__(self):
        self.email = self.email.lower()
```

✅ **Good — touch only what's needed:**
```python
class User:
    def __init__(self, id, email, name):
        self.id = id
        self.email = email
        self.name = name
        self.created_at = datetime.utcnow()  # ← only this line added
```

**Rule:** Match the existing style exactly, even if you'd write it differently. One changed line for one requested feature.

---

### AP-06: Orphan Accumulation

**Task:** "Switch from `requests` to `httpx` for the API calls."

❌ **Bad — leaves the old import:**
```python
import requests  # ← orphaned, your change made this unused
import httpx

def fetch_user(user_id: int) -> dict:
    response = httpx.get(f"/users/{user_id}")
    return response.json()
```

✅ **Good — remove the orphan you created:**
```python
import httpx  # requests removed because your change made it unused

def fetch_user(user_id: int) -> dict:
    response = httpx.get(f"/users/{user_id}")
    return response.json()
```

**Rule:** If YOUR change made something unused, remove it. If it was already dead code before your change, leave it (or mention it separately).

---

## Silent Assumptions
*Violates Rule 1 — Think Before Coding*

### AP-07: Picking an Interpretation Without Saying So

**Task:** "Add caching to the product lookup."

❌ **Bad — LLM silently picks an approach:**
```python
# LLM chose: in-memory LRU cache, 5 min TTL, no invalidation
from functools import lru_cache

@lru_cache(maxsize=128)
def get_product(product_id: int) -> dict:
    return db.query("SELECT * FROM products WHERE id = ?", product_id)
```

✅ **Good — surface the ambiguity first:**
```
Before I implement caching, I need to clarify a few things:

1. **Scope**: In-process (lru_cache) or shared across instances (Redis/Memcached)?
2. **TTL**: How long should cached data be valid? Products change infrequently, but prices might change more often.
3. **Invalidation**: When a product is updated, should the cache be immediately invalidated?
4. **Size**: Is memory usage a concern, or can we cache aggressively?

My default assumption would be in-process LRU with a 5-minute TTL — is that appropriate?
```

**Rule:** State your assumptions. If the question has multiple valid answers, surface them. Don't guess silently.

---

### AP-08: Inventing Requirements

**Task:** "Parse the user's date of birth from the form input."

❌ **Bad — LLM adds unasked-for validation:**
```python
def parse_dob(raw: str) -> date:
    parsed = datetime.strptime(raw, "%Y-%m-%d").date()
    
    today = date.today()
    if parsed > today:
        raise ValueError("Date of birth cannot be in the future")
    if (today - parsed).days > 365 * 150:
        raise ValueError("Date of birth seems unrealistically old")
    if parsed.year < 1900:
        raise ValueError("Date of birth before 1900 not supported")
    
    return parsed
```

✅ **Good — parse what was asked, nothing more:**
```python
def parse_dob(raw: str) -> date:
    return datetime.strptime(raw, "%Y-%m-%d").date()
```

**Note:** If you think validation is important, mention it: "I've implemented basic parsing. Would you like me to add range validation?" Let the user decide.

---

## Unverifiable Output
*Violates Rule 4 — Goal-Driven Execution*

### AP-09: No Verification Path

**Task:** "Fix the race condition in the job queue."

❌ **Bad — change with no way to verify:**
```python
# Added a lock — this should fix it
with self._lock:
    if job_id not in self._processing:
        self._processing.add(job_id)
        return True
return False
```
*(Submits with no test, no reproduction case, no explanation of why this fixes it)*

✅ **Good — verify first, fix second:**
```
Plan:
1. Write a test that reliably reproduces the race condition → verify: test fails consistently
2. Apply the minimal fix → verify: test now passes
3. Run full test suite → verify: no regressions

Here's the reproduction test first:

def test_no_duplicate_job_processing():
    queue = JobQueue()
    results = []
    
    def try_acquire():
        results.append(queue.try_acquire(job_id="job-1"))
    
    threads = [Thread(target=try_acquire) for _ in range(10)]
    [t.start() for t in threads]
    [t.join() for t in threads]
    
    # Only one thread should have acquired the job
    assert results.count(True) == 1

[Test currently fails — confirming the race condition exists. Now applying fix...]
```

---

### AP-10: Vague Success Criteria

**Task:** "Optimize the database queries."

❌ **Bad — no baseline, no target, no measure:**
```python
# Added index and rewrote the JOIN — should be faster now
```

✅ **Good — define what "faster" means before touching anything:**
```
Before optimizing, let me establish success criteria:

Baseline: I'll run EXPLAIN ANALYZE on the current queries and record:
- Current p50 latency: ?ms
- Current p99 latency: ?ms
- Current query plan (index scans vs seq scans)

Target: What improvement are you aiming for? 2×? Sub-100ms? 
Or is there a specific query that's causing problems in production?

Without a baseline measurement and a target, we can't know if the optimization worked.
```

---

## Android / Mobile Specific
*Common patterns for Android development*

### AP-11: God Fragment / God ViewModel

**Task:** "Add location permission handling to the map screen."

❌ **Bad — stuffs all logic into one class:**
```kotlin
class MapFragment : Fragment() {
    // 500 lines: permission logic, location updates, 
    // map rendering, API calls, error handling, analytics...
    
    fun requestLocationPermission() { ... }
    fun onPermissionResult() { ... }
    fun startLocationUpdates() { ... }
    fun fetchNearbyPoints() { ... }
    fun renderMap() { ... }
    fun trackMapView() { ... }
}
```

✅ **Good — surgical addition to the right place:**
```kotlin
// Only added what was asked: permission handling
// Everything else in MapFragment unchanged

class MapFragment : Fragment() {
    // ... existing code unchanged ...
    
    // ← New: permission launcher (added in onCreate area)
    private val locationPermissionLauncher = registerForActivityResult(
        ActivityResultContracts.RequestPermission()
    ) { granted ->
        if (granted) startLocationUpdates() else showPermissionDeniedMessage()
    }
    
    // ← New: call this from the existing button click
    private fun requestLocationIfNeeded() {
        if (hasLocationPermission()) startLocationUpdates()
        else locationPermissionLauncher.launch(Manifest.permission.ACCESS_FINE_LOCATION)
    }
}
```

---

## How to Use This File

When about to write code, quickly scan the relevant section:
- About to add a feature? Check **AP-01 through AP-03** (over-engineering)
- Editing existing code? Check **AP-04 through AP-06** (scope creep)
- Requirement is ambiguous? Check **AP-07 through AP-08** (silent assumptions)
- Hard to tell if it works? Check **AP-09 through AP-10** (unverifiable output)