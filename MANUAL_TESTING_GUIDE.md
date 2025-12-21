# MDSA Framework - Complete Manual Testing Guide
## Phase 3 & Phase 4 Features

This guide will help you test and experience all the features implemented in Phase 3 (Authentication & Rate Limiting) and Phase 4 (Async Support) end-to-end.

---

## Prerequisites

1. **Install Dependencies** (if not already done):
```bash
cd "j:\ME CSE\Sem III\Research Paper\MDSA Orcherstartion Framework\MDSA\version_1"
pip install flask-login flask-limiter
```

2. **Initial Model Download** (first-time only, ~5.4GB):
The Phi-2 model will download automatically on first use.
This takes 5-10 minutes depending on your internet speed.

---

## Part 1: Authentication & Rate Limiting Testing

### 1.1 Start the Dashboard

```bash
python -m mdsa.ui.dashboard
```

You should see:
```
========================================================================
MDSA Dashboard Server
========================================================================
Version: 1.0.0
URL: http://127.0.0.1:5000

Pages:
  • Welcome: http://127.0.0.1:5000/welcome
  • Monitor: http://127.0.0.1:5000/monitor
  • API:     http://127.0.0.1:5000/api/metrics

Press Ctrl+C to stop
========================================================================
```

### 1.2 Test Login Page

**Step 1: Access Dashboard**
- Open browser: http://127.0.0.1:5000
- You should be **automatically redirected** to: http://127.0.0.1:5000/login

**Expected**: Beautiful gradient login page with:
- MDSA Dashboard header with purple gradient
- Version badge
- Username field
- Password field
- "Remember me" checkbox
- Sign In button

**Step 2: Test Invalid Login**
- Username: `admin`
- Password: `wrong_password`
- Click "Sign In"

**Expected**:
- ❌ Red error message: "Invalid username or password."
- Still on login page
- No access to dashboard

**Step 3: Test Valid Login**
- Username: `admin_mdsa`
- Password: `mdsa@admin123`
- Check "Remember me" ✓
- Click "Sign In"

**Expected**:
- ✅ Green success message: "Login successful!"
- Redirect to: http://127.0.0.1:5000/welcome
- Navigation bar shows: 👤 admin_mdsa [Logout]

### 1.3 Test Protected Routes

**While Logged In:**

**Test Welcome Page:**
- Visit: http://127.0.0.1:5000/welcome
- **Expected**: Full access to welcome page showing:
  - Framework features grid
  - Quick start code examples
  - System information
  - User menu with "👤 admin_mdsa" and "Logout" button

**Test Monitor Page:**
- Visit: http://127.0.0.1:5000/monitor
- **Expected**: Full access to monitoring dashboard showing:
  - System overview cards
  - Request statistics
  - Performance metrics
  - Loaded models table
  - User menu visible

**Test API Endpoints:**
- Visit: http://127.0.0.1:5000/api/metrics
- **Expected**: JSON response with framework metrics

### 1.4 Test Session Persistence

**Test 1: Session Persists**
- Keep browser open
- Navigate to: http://127.0.0.1:5000/welcome
- Navigate to: http://127.0.0.1:5000/monitor
- **Expected**: No re-login required, stays logged in

**Test 2: Remember Me**
- Close browser completely
- Reopen browser
- Visit: http://127.0.0.1:5000
- **Expected**: Still logged in (if "Remember me" was checked)

### 1.5 Test Logout

**Step 1: Click Logout**
- Click "Logout" button in navigation

**Expected**:
- ℹ️ Blue info message: "You have been logged out."
- Redirect to: http://127.0.0.1:5000/login

**Step 2: Verify Logout**
- Try accessing: http://127.0.0.1:5000/welcome
- **Expected**: Redirect to login page
- Message: "Please log in to access the dashboard."

### 1.6 Test Rate Limiting

**Test API Rate Limits (PowerShell/Bash):**

**Test 1: Health Endpoint (60/min limit)**
```powershell
# PowerShell
1..65 | ForEach-Object {
    $response = Invoke-WebRequest -Uri "http://127.0.0.1:5000/api/health" -UseBasicParsing
    Write-Host "$_ : $($response.StatusCode)"
}
```

**Expected**:
- Requests 1-60: Status 200 (Success)
- Requests 61+: Status 429 (Too Many Requests)

**Test 2: Metrics Endpoint (30/min limit)**
```powershell
# Login first to get session cookie, then:
1..35 | ForEach-Object {
    Write-Host "Request $_"
    try {
        Invoke-WebRequest -Uri "http://127.0.0.1:5000/api/metrics" -UseBasicParsing
    } catch {
        Write-Host "Error: $_"
    }
}
```

**Expected**:
- Requests 1-30: Status 200 (Success) with JSON
- Requests 31+: Status 429 (Too Many Requests)

**Test 3: Wait for Reset**
- Wait 1 minute
- Try again: http://127.0.0.1:5000/api/health
- **Expected**: Status 200 (limit reset)

---

## Part 2: Async Support Testing

### 2.1 Interactive Python Testing

```bash
python
```

```python
import asyncio
from mdsa import ModelManager, DomainExecutor
from mdsa.domains.config import get_predefined_domain
from mdsa.async_ import AsyncExecutor, AsyncManager

# Create components
model_manager = ModelManager(max_models=2)
domain_executor = DomainExecutor(model_manager)
async_executor = AsyncExecutor(domain_executor, max_workers=5)

# Get domain config
support_config = get_predefined_domain('support')

# Test 1: Single Async Query
async def test_single():
    result = await async_executor.execute_async(
        query="What time is it?",
        domain_config=support_config
    )
    print(f"Status: {result['status']}")
    print(f"Response: {result.get('response', 'N/A')}")
    print(f"Latency: {result['latency_ms']:.1f}ms")

asyncio.run(test_single())
```

**Expected Output:**
```
Status: success
Response: [Current time and date]
Latency: 1500-3000ms (first run, model loading)
```

**Test 2: Concurrent Queries**
```python
async def test_concurrent():
    queries = [
        "What time is it?",
        "Calculate 25 + 37",
        "What is AI?",
    ]
    configs = [support_config] * 3

    results = await async_executor.execute_multiple(
        queries=queries,
        domain_configs=configs
    )

    for i, result in enumerate(results):
        print(f"\nQuery {i+1}: {queries[i]}")
        print(f"  Status: {result['status']}")
        print(f"  Latency: {result['latency_ms']:.1f}ms")

asyncio.run(test_concurrent())
```

**Expected Output:**
```
Query 1: What time is it?
  Status: success
  Latency: 850ms

Query 2: Calculate 25 + 37
  Status: success
  Latency: 920ms

Query 3: What is AI?
  Status: success
  Latency: 1100ms
```

**Test 3: Batch Processing with AsyncManager**
```python
async def test_batch():
    manager = AsyncManager(
        async_executor=async_executor,
        max_concurrent=3,
        enable_stats=True
    )

    queries = [
        "What time is it?",
        "Calculate 50 + 75",
        "Convert 100 celsius to fahrenheit",
        "What is Python?",
        "How many words are in this sentence?",
    ]

    configs = [support_config] * len(queries)

    results = await manager.execute_batch(
        queries=queries,
        domain_configs=configs
    )

    # Show results
    success_count = sum(1 for r in results if r and r['status'] == 'success')
    print(f"\nSuccess: {success_count}/{len(queries)}")

    # Show statistics
    stats = manager.get_stats()
    print(f"\nStatistics:")
    print(f"  Total queries: {stats['total_queries']}")
    print(f"  Success rate: {stats['success_rate']:.1f}%")
    print(f"  Avg latency: {stats['avg_latency_ms']:.1f}ms")
    print(f"  Concurrent peak: {stats['concurrent_peak']}")

    # Cleanup
    await manager.shutdown()

asyncio.run(test_batch())
```

**Expected Output:**
```
Success: 5/5

Statistics:
  Total queries: 5
  Success rate: 100.0%
  Avg latency: 950.2ms
  Concurrent peak: 3
```

### 2.2 Performance Comparison

```python
import time

async def compare_performance():
    queries = ["What time is it?", "Calculate 10 + 20", "What is AI?"]
    config = support_config

    # Synchronous execution
    print("Synchronous execution...")
    sync_start = time.time()
    for query in queries:
        result = domain_executor.execute(
            query=query,
            domain_config=config
        )
    sync_time = (time.time() - sync_start) * 1000

    # Asynchronous execution
    print("Asynchronous execution...")
    async_start = time.time()
    configs = [config] * len(queries)
    results = await async_executor.execute_multiple(
        queries=queries,
        domain_configs=configs
    )
    async_time = (time.time() - async_start) * 1000

    print(f"\nSynchronous time: {sync_time:.1f}ms")
    print(f"Asynchronous time: {async_time:.1f}ms")
    print(f"Speedup: {sync_time / async_time:.2f}x")

asyncio.run(compare_performance())
```

**Expected Output:**
```
Synchronous execution...
Asynchronous execution...

Synchronous time: 4500ms  (3 queries × ~1500ms each)
Asynchronous time: 1800ms (3 queries in parallel)
Speedup: 2.5x
```

---

## Part 3: End-to-End Integration Testing

### 3.1 Complete Workflow Test

**Scenario**: Test authentication, monitoring, and async queries together

**Step 1: Start Dashboard**
```bash
python -m mdsa.ui.dashboard
```

**Step 2: Login**
- Browser: http://127.0.0.1:5000
- Login with: admin_mdsa / mdsa@admin123

**Step 3: Monitor Initial State**
- Visit: http://127.0.0.1:5000/monitor
- Note current metrics:
  - Total requests: 0
  - Loaded models: 0

**Step 4: Execute Async Queries (Python)**
```python
# In separate Python terminal
import asyncio
from mdsa import ModelManager, DomainExecutor
from mdsa.domains.config import get_predefined_domain
from mdsa.async_ import AsyncExecutor

model_manager = ModelManager(max_models=2)
domain_executor = DomainExecutor(model_manager)
async_executor = AsyncExecutor(domain_executor)

async def run_queries():
    config = get_predefined_domain('support')
    queries = ["Query 1", "Query 2", "Query 3", "Query 4", "Query 5"]
    configs = [config] * len(queries)

    results = await async_executor.execute_multiple(
        queries=queries,
        domain_configs=configs
    )

    success = sum(1 for r in results if r['status'] == 'success')
    print(f"Completed: {success}/{len(queries)}")

asyncio.run(run_queries())
```

**Step 5: Refresh Dashboard**
- Browser: Refresh http://127.0.0.1:5000/monitor
- **Expected**: Updated metrics showing:
  - Total requests: 5
  - Loaded models: 1 (microsoft/phi-2)
  - Performance metrics updated

**Step 6: Test API Rate Limit**
- Rapidly access: http://127.0.0.1:5000/api/metrics
- After 30 requests in 1 minute, you should get:
  - Status 429: Too Many Requests

**Step 7: Logout**
- Click "Logout"
- Try accessing: http://127.0.0.1:5000/monitor
- **Expected**: Redirect to login (access denied)

---

## Part 4: Feature Verification Checklist

### ✅ Phase 3: Authentication & Rate Limiting

**Authentication:**
- [ ] Login page displays correctly
- [ ] Invalid credentials rejected
- [ ] Valid login successful (admin_mdsa / mdsa@admin123)
- [ ] User menu shows logged-in user (👤 admin_mdsa)
- [ ] Logout button visible and functional
- [ ] Protected routes require login
- [ ] Session persists across navigation
- [ ] Remember me checkbox works
- [ ] Logout clears session

**Rate Limiting:**
- [ ] /api/health: 60 requests/minute limit enforced
- [ ] /api/metrics: 30 requests/minute limit enforced
- [ ] 429 status returned when limit exceeded
- [ ] Limits reset after 1 minute
- [ ] Global limits (200/day, 50/hour) work

**UI Elements:**
- [ ] Login template has gradient design
- [ ] Flash messages display correctly
- [ ] Navigation shows user info
- [ ] Logout button styled properly
- [ ] Mobile responsive design

### ✅ Phase 4: Async Support

**AsyncExecutor:**
- [ ] execute_async() works for single query
- [ ] execute_multiple() handles concurrent queries
- [ ] execute_with_retry() retries on failure
- [ ] Timeout handling works (30s default)
- [ ] ThreadPoolExecutor created with max_workers
- [ ] Context manager support (__aenter__, __aexit__)

**AsyncManager:**
- [ ] execute_batch() processes multiple queries
- [ ] Semaphore limits concurrent execution
- [ ] Statistics tracking works (ExecutionStats)
- [ ] execute_with_fallback() tries alternative domains
- [ ] execute_parallel_domains() runs cross-domain queries
- [ ] Progress callback support
- [ ] Graceful shutdown

**Performance:**
- [ ] Async faster than sync for multiple queries
- [ ] Concurrent execution verified
- [ ] Resource pooling effective
- [ ] No race conditions or deadlocks

---

## Troubleshooting

### Issue 1: "ModuleNotFoundError: No module named 'flask_login'"
**Solution:**
```bash
pip install flask-login flask-limiter
```

### Issue 2: Login always fails
**Solution:** Check default credentials:
- Username: `admin_mdsa` (not just "admin")
- Password: `mdsa@admin123`

### Issue 3: "429 Too Many Requests" immediately
**Solution:** Wait 1 minute for rate limit to reset, or restart dashboard.

### Issue 4: Async queries timeout
**Solution:** First-time model download takes 5-10 minutes. After model is cached:
- Increase timeout: `timeout=60.0`
- Or wait for model to fully download

### Issue 5: Model downloading is slow
**Solution:** First-time Phi-2 download is ~5.4GB. Subsequent runs use cached model.

### Issue 6: "Can't find users.json"
**Solution:** File is auto-created in `mdsa/ui/users.json`. Ensure write permissions.

---

## Performance Expectations

### Initial Run (First Time):
- Model download: 5-10 minutes
- First query: 30-60 seconds (model loading)
- Subsequent queries: 1-3 seconds each

### After Model Cached:
- Model loading: 2-5 seconds
- Query execution: 0.5-2 seconds
- Async speedup: 2-3x for 3+ concurrent queries

### Rate Limits:
- Health API: 60 requests/minute
- Metrics API: 30 requests/minute (with auth)
- Global: 200 requests/day, 50 requests/hour

---

## Next Steps After Testing

Once you've verified all features:

**Phase 5: Comprehensive Test Suite**
- Pytest configuration
- Unit tests (80%+ coverage)
- Integration tests
- CI/CD setup

**Phase 6: UI Redesign**
- Modern dashboard with D3.js
- Real-time charts and graphs
- Interactive visualizations

**Phase 7: Documentation**
- Complete FRAMEWORK_REFERENCE.md
- API documentation
- Architecture diagrams

---

## Support & Feedback

If you encounter any issues:
1. Check this troubleshooting section
2. Review error messages in console
3. Check logs in terminal
4. Verify all dependencies installed

**Enjoy testing the MDSA Framework!** 🚀
