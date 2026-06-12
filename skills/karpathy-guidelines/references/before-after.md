# Before / After Examples

Real-world style diffs showing the Karpathy Guidelines applied correctly. Use these to calibrate what "right" looks like.

Each example shows: the task, the LLM's first (bad) instinct, and the correct minimal response.

---

## Example 1: Bug Fix with Scope Discipline

**Task:** "The `format_price` function adds an extra decimal place sometimes. Fix it."

### ❌ LLM's bad first instinct
```python
# LLM rewrote the whole module, added type hints everywhere,
# extracted helpers, reformatted docstrings, and fixed the bug

from decimal import Decimal, ROUND_HALF_UP
from typing import Union

def format_price(
    amount: Union[int, float, Decimal],
    currency: str = "USD",
    locale: str = "en-US"
) -> str:
    """
    Format a monetary amount as a localized currency string.
    
    Args:
        amount: The monetary value to format
        currency: ISO 4217 currency code (default: USD)
        locale: BCP 47 locale string (default: en-US)
    
    Returns:
        Formatted currency string (e.g., "$12.99")
    """
    decimal_amount = Decimal(str(amount)).quantize(
        Decimal("0.01"), rounding=ROUND_HALF_UP
    )
    symbols = {"USD": "$", "EUR": "€", "GBP": "£"}
    symbol = symbols.get(currency, currency)
    return f"{symbol}{decimal_amount}"

def _parse_amount(raw: Union[int, float, str]) -> Decimal:
    """Parse various input types to Decimal."""
    return Decimal(str(raw))
```

### ✅ Correct minimal fix
```python
# Before:
def format_price(amount):
    return f"${amount:.3f}"   # ← was using 3 decimal places

# After:
def format_price(amount):
    return f"${amount:.2f}"   # ← fixed: 2 decimal places for currency
```

**What the good version does:**
- One character changed: `3` → `2`
- Everything else untouched
- No new imports, no type hints, no helpers, no config
- User's style preserved exactly

---

## Example 2: New Feature with Assumption Surfacing

**Task:** "Add rate limiting to the API."

### ❌ LLM's bad first instinct
```python
# LLM silently chose: per-IP, 100 req/min, in-memory, no burst allowance
from collections import defaultdict
import time

_request_counts = defaultdict(list)
RATE_LIMIT = 100  # requests per minute

def check_rate_limit(ip: str) -> bool:
    now = time.time()
    minute_ago = now - 60
    _request_counts[ip] = [t for t in _request_counts[ip] if t > minute_ago]
    
    if len(_request_counts[ip]) >= RATE_LIMIT:
        return False
    
    _request_counts[ip].append(now)
    return True
```

### ✅ Correct: surface assumptions first
```
Before implementing, I need to clarify a few design choices:

1. **Granularity**: Per-IP? Per-user/API key? Per endpoint?
2. **Limit**: What's the threshold? (100 req/min is common for public APIs, but depends on your traffic)
3. **Storage**: In-memory (single instance, resets on restart) or shared (Redis, works across instances)?
4. **Burst allowance**: Strict limit, or token bucket that allows short bursts?
5. **Response**: Return 429 with Retry-After header?

My default assumption: per-IP, 100 req/min, in-memory sliding window, 429 on breach. 
Does that match your needs, or should I adjust?
```

*(Then implement once confirmed)*

---

## Example 3: Refactor with Surgical Precision

**Task:** "Extract the email validation logic from `register_user` into its own function."

### ❌ LLM's bad first instinct
```python
# LLM restructured the whole module, split into separate files,
# added an EmailValidator class with multiple methods,
# switched to a different validation library

class EmailValidator:
    DOMAIN_BLACKLIST = ["tempmail.com", "throwaway.email"]
    
    def validate(self, email: str) -> ValidationResult:
        ...
    
    def _check_format(self, email: str) -> bool:
        ...
    
    def _check_domain(self, email: str) -> bool:
        ...
    
    def _check_mx_record(self, email: str) -> bool:
        ...
```

### ✅ Correct: extract exactly what was asked
```python
# Before:
def register_user(email, password):
    import re
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        raise ValueError("Invalid email")
    # ... rest of registration ...

# After:
def is_valid_email(email: str) -> bool:          # ← extracted exactly this logic
    import re
    return bool(re.match(r"[^@]+@[^@]+\.[^@]+", email))

def register_user(email, password):
    if not is_valid_email(email):                 # ← replaced with extracted function
        raise ValueError("Invalid email")
    # ... rest of registration unchanged ...
```

**What the good version does:**
- Extracts the exact 2 lines that were asked about
- Same regex, same import placement, same error message
- No new abstractions, no new validation logic, no new dependencies
- `register_user` diff: 2 lines changed (the call site)

---

## Example 4: Performance Task with Baseline

**Task:** "The user search is slow — can you make it faster?"

### ❌ LLM's bad first instinct
```python
# LLM added caching, changed the query, added an index,
# switched to async, all without measuring anything first

@lru_cache(maxsize=1000)
async def search_users(query: str) -> list[User]:
    async with db.connection() as conn:
        return await conn.execute(
            "SELECT * FROM users WHERE name ILIKE $1 LIMIT 20",
            f"%{query}%"
        )
```

### ✅ Correct: diagnose before optimizing
```
Before optimizing, let's understand what's actually slow.

Step 1 — Baseline measurement:
Can you run this and share the output?

```python
import time

def search_users_timed(query: str) -> tuple[list, float]:
    start = time.perf_counter()
    results = search_users(query)  # current implementation
    elapsed = time.perf_counter() - start
    return results, elapsed

# Run with a typical query:
results, ms = search_users_timed("john")
print(f"Query took {ms*1000:.1f}ms, returned {len(results)} results")
```

Also helpful: run `EXPLAIN ANALYZE SELECT * FROM users WHERE name ILIKE '%john%'` in your DB console and share the output.

Step 2 — Once we know the bottleneck, I'll implement the minimal fix:
- If it's a missing index → add one index
- If it's N+1 queries → fix the query
- If it's repeated identical lookups → add targeted caching

Guessing without measuring often optimizes the wrong thing.
```

---

## Example 5: Android — Adding a Feature Without God-Object

**Task:** "Add a 'copy to clipboard' button to the notes detail screen."

### ❌ LLM's bad first instinct
```kotlin
// Rewrote NoteDetailFragment with new architecture,
// added ViewModel for clipboard, added analytics, 
// added undo snackbar, added haptic feedback

class NoteDetailViewModel(
    private val clipboardManager: ClipboardManager,
    private val analyticsTracker: AnalyticsTracker,
    private val vibrator: Vibrator
) : ViewModel() {
    
    sealed class UiEvent { ... }
    
    fun onCopyClicked(text: String) {
        clipboardManager.setPrimaryClip(ClipData.newPlainText("note", text))
        analyticsTracker.track("note_copied")
        vibrator.vibrate(VibrationEffect.createOneShot(50, DEFAULT_AMPLITUDE))
        _events.emit(UiEvent.ShowCopiedConfirmation)
    }
}
```

### ✅ Correct: minimum addition to the existing fragment
```kotlin
// In NoteDetailFragment — added only what was asked:

// 1. Add button to layout (note_detail_fragment.xml)
// <Button android:id="@+id/copyButton" android:text="Copy" ... />

// 2. Wire it up in onViewCreated — 3 lines:
binding.copyButton.setOnClickListener {
    val clipboard = getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager
    clipboard.setPrimaryClip(ClipData.newPlainText("note", binding.noteContent.text))
    Toast.makeText(context, "Copied", Toast.LENGTH_SHORT).show()
}
// Everything else in the fragment unchanged.
```

**What the good version does:**
- 3 lines of logic + 1 button in XML
- No new ViewModel, no analytics, no haptics, no architecture change
- Uses the existing binding pattern in the fragment
- States what XML change is needed but doesn't silently expand scope

---

## Reading the Pattern

All "good" examples share the same structure:

1. **Minimum diff** — smallest possible change that satisfies the request
2. **Preserved context** — existing style, imports, patterns kept intact  
3. **No speculation** — nothing added "in case they need it later"
4. **Clear verification** — it's obvious whether it worked or not

The failure mode in every "bad" example is the same: the LLM imagined a larger, more complete, more "professional" version of the task and built that instead of what was asked.