# Application-Agnostic Monitoring Integration Guide

## ✅ What Was Created

### 1. **MonitoringService** - Universal Metrics Collection
**File:** [mdsa/monitoring/service.py](mdsa/monitoring/service.py)

**Features:**
- ✅ Works with ANY MDSA application (Medical Chatbot, EduAI, custom apps)
- ✅ No hardcoding - applications register themselves automatically
- ✅ File-based shared state (no Redis/database needed)
- ✅ Thread-safe operations
- ✅ Automatic cleanup of old metrics
- ✅ Dashboard can read from ALL connected applications

---

## 🔧 How to Integrate into Applications

### Medical Chatbot Integration

Add this to [enhanced_medical_chatbot_fixed.py](chatbot_app/medical_app/enhanced_medical_chatbot_fixed.py):

```python
# At top of file (with other imports):
from mdsa.monitoring import MonitoringService

# In create_orchestrator() function (after orchestrator creation):
# Initialize monitoring service
monitor = MonitoringService(app_name="MedicalChatbot")
orchestrator.monitor = monitor  # Attach to orchestrator

# In process_user_query() function (after getting result):
# Publish metrics if monitoring enabled
if hasattr(orchestrator, 'monitor'):
    orchestrator.monitor.publish_request(
        query=message,
        domain=result.get('metadata', {}).get('domain', 'unknown'),
        confidence=result.get('metadata', {}).get('confidence', 0.0),
        latency_ms=result.get('metadata', {}).get('latency_ms', 0.0),
        success=result.get('status') == 'success',
        error=result.get('error') if result.get('status') != 'success' else None
    )
```

---

### EduAI Integration (Future)

```python
# In EduAI application:
from mdsa.monitoring import MonitoringService

# Initialize
monitor = MonitoringService(app_name="EduAI")

# Publish after each query
monitor.publish_request(
    query="What is the quadratic formula?",
    domain="mathematics",
    confidence=0.95,
    latency_ms=842.3,
    success=True
)
```

---

### Dashboard Integration

Update [mdsa/ui/dashboard/app.py](mdsa/ui/dashboard/app.py):

```python
# At top of file:
from mdsa.monitoring import MonitoringService

# In initialization section (around line 50):
# Initialize monitoring subscriber (reads from all apps)
monitoring_service = MonitoringService()  # No app_name = subscriber mode

# Update get_current_metrics() endpoint (around line 440):
@app.get("/api/metrics")
async def get_current_metrics():
    """Get real-time metrics from all connected applications."""
    try:
        # Get metrics from monitoring service
        stats = monitoring_service.get_summary_stats()
        active_apps = monitoring_service.get_active_apps()

        return {
            "timestamp": datetime.now().isoformat(),
            "domains": len(stats.get('domains', {})),
            "total_requests": stats.get('total_requests', 0),
            "successful_requests": stats.get('successful_requests', 0),
            "failed_requests": stats.get('failed_requests', 0),
            "avg_latency_ms": stats.get('avg_latency_ms', 0.0),
            "domain_stats": stats.get('domains', {}),
            "active_applications": active_apps,
            "rag": {"global_rag": {"document_count": 0}, "local_rags": {}}
        }
    except Exception as e:
        logger.error(f"Error getting metrics: {e}")
        return {"error": str(e)}

# Update get_visualization_data() endpoint (around line 377):
@app.get("/api/visualization-data")
async def get_visualization_data():
    """Get data for D3.js visualizations from monitoring service."""
    try:
        # Get all metrics
        metrics = monitoring_service.get_all_metrics(max_age_hours=24)

        # Build Sankey data (query flow)
        sankey_nodes = ["User Queries", "TinyBERT Router"]
        sankey_links = []

        domain_counts = {}
        for metric in metrics:
            domain = metric.domain
            if domain not in domain_counts:
                domain_counts[domain] = 0
            domain_counts[domain] += 1

        # Add domain nodes
        for domain in domain_counts:
            sankey_nodes.append(domain)
            # Link: Router -> Domain
            sankey_links.append({
                "source": 1,  # TinyBERT Router
                "target": len(sankey_nodes) - 1,
                "value": domain_counts[domain]
            })

        # Build latency heatmap
        heatmap = []
        for metric in metrics:
            heatmap.append({
                "domain": metric.domain,
                "timestamp": metric.timestamp,
                "latency": metric.latency_ms
            })

        # Build timeline
        timeline = {}
        for metric in metrics:
            minute = int(metric.timestamp // 60) * 60
            if minute not in timeline:
                timeline[minute] = 0
            timeline[minute] += 1

        timeline_data = [
            {"timestamp": ts, "count": count}
            for ts, count in sorted(timeline.items())
        ]

        return {
            "sankey": {"nodes": sankey_nodes, "links": sankey_links},
            "heatmap": heatmap,
            "timeline": timeline_data,
            "pie": [
                {"domain": domain, "count": count}
                for domain, count in domain_counts.items()
            ]
        }

    except Exception as e:
        logger.error(f"Error getting visualization data: {e}")
        return {"error": str(e)}
```

---

## 📊 Shared Metrics Location

All metrics are stored in:
```
~/.mdsa/metrics/
├── requests.jsonl          # All request metrics (JSONL format)
└── applications.json       # Registered applications
```

**Example requests.jsonl:**
```jsonl
{"timestamp": 1733879400.123, "app_name": "MedicalChatbot", "query": "What is diabetes?", "domain": "clinical_diagnosis", "confidence": 0.92, "latency_ms": 1245.3, "success": true, "error": null, "metadata": {}}
{"timestamp": 1733879405.456, "app_name": "EduAI", "query": "Quadratic formula?", "domain": "mathematics", "confidence": 0.95, "latency_ms": 842.1, "success": true, "error": null, "metadata": {}}
```

**Example applications.json:**
```json
{
  "MedicalChatbot": {
    "name": "MedicalChatbot",
    "registered_at": "2025-12-11T00:30:00",
    "last_seen": "2025-12-11T00:35:12",
    "pid": 12345
  },
  "EduAI": {
    "name": "EduAI",
    "registered_at": "2025-12-11T00:32:00",
    "last_seen": "2025-12-11T00:35:10",
    "pid": 12789
  }
}
```

---

## 🚀 How It Works

### 1. **Application Publishes Metrics**
```python
monitor = MonitoringService(app_name="MedicalChatbot")
monitor.publish_request(
    query="What is diabetes?",
    domain="clinical_diagnosis",
    confidence=0.92,
    latency_ms=1245.3,
    success=True
)
```

↓ Writes to `~/.mdsa/metrics/requests.jsonl`

### 2. **Dashboard Reads Metrics**
```python
monitor = MonitoringService()  # Subscriber mode
metrics = monitor.get_all_metrics()  # Reads from shared file
stats = monitor.get_summary_stats()  # Aggregates across ALL apps
```

### 3. **Multiple Applications Coexist**
- Medical Chatbot writes: `{"app_name": "MedicalChatbot", ...}`
- EduAI writes: `{"app_name": "EduAI", ...}`
- Dashboard reads BOTH and displays unified view

---

## ✅ Benefits

1. **No Hardcoding**: Applications automatically register themselves
2. **Multi-App Support**: Dashboard shows metrics from ALL MDSA apps
3. **Zero Dependencies**: Uses only Python stdlib (no Redis, no database)
4. **Thread-Safe**: Multiple apps can write concurrently
5. **Auto-Cleanup**: Old metrics automatically removed (default: 24 hours)
6. **Portable**: Works on Windows, Linux, macOS

---

## 🧪 Testing

### Test Medical Chatbot Monitoring:
```python
from mdsa.monitoring import MonitoringService

# Simulate publishing
monitor = MonitoringService(app_name="TestApp")
monitor.publish_request(
    query="Test query",
    domain="test_domain",
    confidence=0.90,
    latency_ms=100.5,
    success=True
)

# Read back
metrics = monitor.get_all_metrics()
print(f"Total metrics: {len(metrics)}")

stats = monitor.get_summary_stats()
print(f"Total requests: {stats['total_requests']}")
print(f"Applications: {list(stats['applications'].keys())}")
```

---

## 📝 Next Steps

1. ✅ Monitoring service created
2. ⏳ Integrate into medical chatbot
3. ⏳ Update dashboard to read from monitoring service
4. ⏳ Test with medical chatbot
5. ⏳ Use same pattern for EduAI (no changes needed!)

---

**Status:** ✅ Monitoring service ready
**Integration:** ⏳ Pending (add 3 lines to medical chatbot, update dashboard endpoints)
**Works with:** ANY MDSA application without hardcoding
