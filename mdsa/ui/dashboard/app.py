"""
MDSA Framework Monitoring Dashboard

FastAPI-based real-time monitoring UI for MDSA framework.
Provides visualization of domains, models, RAG, metrics, and request flows.

Routes:
- GET /welcome - Landing page
- GET /monitor - Real-time monitoring dashboard
- GET /api/health - Health check
- GET /api/domains - List all domains
- GET /api/models - List loaded models
- GET /api/metrics - System metrics
- GET /api/requests - Request history
- POST /api/query - Process query through MDSA
- WS /ws/metrics - WebSocket for real-time metrics

Usage:
    python mdsa/ui/dashboard/app.py

Then open: http://localhost:5000/welcome
"""

import os
import sys
import json
import asyncio
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from pydantic import BaseModel
import uvicorn

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from mdsa.core.orchestrator import TinyBERTOrchestrator
from mdsa.domains.registry import DomainRegistry
from mdsa.models.loader import ModelLoader
from mdsa.memory.dual_rag import DualRAG

# Initialize FastAPI
app = FastAPI(
    title="MDSA Monitoring Dashboard",
    description="Real-time monitoring and visualization for Multi-Domain Specialized Agents Framework",
    version="1.0.0"
)

# Setup templates and static files
BASE_DIR = Path(__file__).parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

# Global MDSA instance (will be initialized on startup)
mdsa_orchestrator: Optional[TinyBERTOrchestrator] = None
domain_registry: Optional[DomainRegistry] = None
model_loader: Optional[ModelLoader] = None
dual_rag: Optional[DualRAG] = None

# Request history storage
request_history: List[Dict] = []
MAX_HISTORY = 1000

# WebSocket connections
active_connections: List[WebSocket] = []


# ============================================================================
# Pydantic Models
# ============================================================================

class QueryRequest(BaseModel):
    """Query request model"""
    query: str
    context: Optional[Dict] = None


class DomainInfo(BaseModel):
    """Domain information model"""
    domain_id: str
    model_name: str
    description: str
    keywords: List[str]
    status: str


# ============================================================================
# Startup/Shutdown Events
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Initialize MDSA components on startup"""
    global mdsa_orchestrator, domain_registry, model_loader, dual_rag

    print("="*60)
    print("MDSA Monitoring Dashboard Starting...")
    print("="*60)

    try:
        # Initialize orchestrator (it creates its own internal components)
        mdsa_orchestrator = TinyBERTOrchestrator(
            enable_reasoning=True,
            complexity_threshold=0.3
        )

        # Access orchestrator's internal components for API endpoints
        domain_registry = mdsa_orchestrator.domains  # Access internal domain registry
        # Note: model_loader and dual_rag are not exposed by TinyBERTOrchestrator
        # We'll work with what's available

        print("✓ MDSA orchestrator initialized")
        print("✓ Dashboard ready")
        print("\nAccess dashboard at: http://localhost:5000/welcome")
        print("="*60)

    except Exception as e:
        print(f"✗ Initialization error: {e}")
        import traceback
        traceback.print_exc()


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    print("\nShutting down MDSA Dashboard...")


# ============================================================================
# WebSocket Manager
# ============================================================================

async def broadcast_metrics():
    """Broadcast metrics to all connected WebSocket clients"""
    while True:
        if active_connections:
            metrics = get_current_metrics()
            for connection in active_connections:
                try:
                    await connection.send_json(metrics)
                except:
                    active_connections.remove(connection)
        await asyncio.sleep(2)  # Update every 2 seconds


# ============================================================================
# Page Routes
# ============================================================================

@app.get("/", response_class=HTMLResponse)
@app.get("/welcome", response_class=HTMLResponse)
async def welcome_page(request: Request):
    """Landing page with framework overview"""
    # Get domain list with details
    domains_list = []
    if mdsa_orchestrator:
        for domain_id, config in mdsa_orchestrator.domains.items():
            domains_list.append({
                "id": domain_id,
                "name": config.get('description', domain_id.replace('_', ' ').title()),
                "keywords": config.get('keywords', []),
                "model": config.get('model_name', 'unknown')
            })

    # Get RAG stats (RAG not exposed by orchestrator, set to 0)
    rag_docs = 0

    stats = {
        "total_domains": len(mdsa_orchestrator.domains) if mdsa_orchestrator else 0,
        "total_requests": len(request_history),
        "active_models": len(set(d.get('model_name', '') for d in mdsa_orchestrator.domains.values())) if mdsa_orchestrator else 0,
        "rag_documents": rag_docs
    }

    return templates.TemplateResponse(
        "welcome.html",
        {"request": request, "stats": stats, "domains": domains_list}
    )


@app.get("/monitor", response_class=HTMLResponse)
async def monitor_page(request: Request):
    """Real-time monitoring dashboard with visualizations"""
    return templates.TemplateResponse(
        "monitor.html",
        {"request": request}
    )


# ============================================================================
# API Routes
# ============================================================================

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "components": {
            "orchestrator": mdsa_orchestrator is not None,
            "domain_registry": domain_registry is not None,
            "model_loader": False,  # Not exposed by orchestrator
            "dual_rag": False  # Not exposed by orchestrator
        }
    }


@app.get("/api/domains")
async def list_domains():
    """List all registered domains"""
    if not mdsa_orchestrator:
        raise HTTPException(status_code=503, detail="Orchestrator not initialized")

    domains = []
    for domain_id, config in mdsa_orchestrator.domains.items():
        domains.append({
            "domain_id": domain_id,
            "model_name": config.get('model_name', 'unknown'),
            "description": config.get('description', 'No description'),
            "keywords": config.get('keywords', []),
            "status": "active",
            "device": config.get('device', 'cpu')
        })

    return {"domains": domains, "count": len(domains)}


@app.get("/api/models")
async def list_models():
    """List all loaded models"""
    if not mdsa_orchestrator:
        raise HTTPException(status_code=503, detail="Orchestrator not initialized")

    # Extract models from domains
    models = []
    seen_models = set()
    for _, config in mdsa_orchestrator.domains.items():
        model_name = config.get('model_name', 'unknown')
        if model_name not in seen_models:
            seen_models.add(model_name)
            models.append({
                "model_name": model_name,
                "device": config.get('device', 'cpu'),
                "domains_using": [d for d, c in mdsa_orchestrator.domains.items() if c.get('model_name') == model_name]
            })

    return {
        "models": models,
        "count": len(models)
    }


@app.get("/api/metrics")
async def get_metrics():
    """Get current system metrics"""
    return get_current_metrics()


@app.get("/api/requests")
async def get_requests(limit: int = 100):
    """Get request history"""
    return {
        "requests": request_history[-limit:],
        "total": len(request_history),
        "limit": limit
    }


@app.post("/api/query")
async def process_query(query_request: QueryRequest):
    """Process a query through MDSA"""
    if not mdsa_orchestrator:
        raise HTTPException(status_code=503, detail="Orchestrator not initialized")

    start_time = datetime.now()

    try:
        # Process query
        result = mdsa_orchestrator.process_request(
            query=query_request.query,
            context=query_request.context
        )

        # Calculate latency
        latency_ms = (datetime.now() - start_time).total_seconds() * 1000

        # Store in history
        history_entry = {
            "timestamp": start_time.isoformat(),
            "query": query_request.query,
            "domain": result.get('domain', 'unknown'),
            "status": result.get('status', 'unknown'),
            "latency_ms": latency_ms,
            "response_preview": result.get('response', '')[:100]
        }
        request_history.append(history_entry)
        if len(request_history) > MAX_HISTORY:
            request_history.pop(0)

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/visualization-data")
async def get_visualization_data():
    """Get data formatted for D3.js visualizations"""
    if not mdsa_orchestrator:
        raise HTTPException(status_code=503, detail="Orchestrator not initialized")

    # Analyze request history for visualizations
    domain_stats = {}
    latency_data = {}
    timeline_buckets = {}

    for req in request_history:
        domain = req.get('domain', 'unknown')
        latency = req.get('latency_ms', 0)
        timestamp = req.get('timestamp', '')
        status = req.get('status', 'unknown')

        # Domain statistics
        if domain not in domain_stats:
            domain_stats[domain] = {
                'requests': 0,
                'successes': 0,
                'latencies': []
            }

        domain_stats[domain]['requests'] += 1
        domain_stats[domain]['latencies'].append(latency)
        if status == 'success':
            domain_stats[domain]['successes'] += 1

        # Latency heatmap data (by hour)
        if timestamp:
            try:
                dt = datetime.fromisoformat(timestamp)
                hour_bucket = dt.strftime('%H:00')
                if hour_bucket not in latency_data:
                    latency_data[hour_bucket] = {}
                if domain not in latency_data[hour_bucket]:
                    latency_data[hour_bucket][domain] = []
                latency_data[hour_bucket][domain].append(latency)
            except:
                pass

        # Timeline data (by minute)
        if timestamp:
            try:
                dt = datetime.fromisoformat(timestamp)
                minute_bucket = dt.strftime('%H:%M')
                timeline_buckets[minute_bucket] = timeline_buckets.get(minute_bucket, 0) + 1
            except:
                pass

    # Format Sankey data
    sankey_domains = []
    for domain, stats in domain_stats.items():
        sankey_domains.append({
            'name': domain,
            'requests': stats['requests'],
            'success_rate': stats['successes'] / stats['requests'] if stats['requests'] > 0 else 0
        })

    # Format heatmap data
    all_domains = list(domain_stats.keys())
    time_buckets = sorted(list(latency_data.keys()))[-12:]  # Last 12 hours

    heatmap_matrix = []
    for domain in all_domains:
        row = []
        for bucket in time_buckets:
            latencies = latency_data.get(bucket, {}).get(domain, [])
            avg_latency = sum(latencies) / len(latencies) if latencies else 0
            row.append(avg_latency)
        heatmap_matrix.append(row)

    # Format RAG data (RAG not exposed by orchestrator)
    global_docs = 0
    local_docs = {}

    # Format timeline data
    timeline_data = [
        {'timestamp': datetime.now().replace(hour=int(t.split(':')[0]), minute=int(t.split(':')[1])).isoformat(), 'count': count}
        for t, count in sorted(timeline_buckets.items())[-20:]  # Last 20 minutes
    ]

    # Format pie chart data
    pie_data = [
        {'domain': domain, 'requests': stats['requests']}
        for domain, stats in domain_stats.items()
    ]

    return {
        "sankey": {
            "domains": sankey_domains,
            "total_requests": len(request_history)
        },
        "heatmap": {
            "domains": all_domains,
            "time_buckets": time_buckets,
            "latencies": heatmap_matrix
        },
        "rag": {
            "global_docs": global_docs,
            "local_docs": local_docs
        },
        "timeline": {
            "timeline": timeline_data
        },
        "pie": pie_data
    }


# ============================================================================
# WebSocket Route
# ============================================================================

@app.websocket("/ws/metrics")
async def metrics_websocket(websocket: WebSocket):
    """WebSocket endpoint for real-time metrics streaming"""
    await websocket.accept()
    active_connections.append(websocket)

    try:
        while True:
            # Keep connection alive and send metrics every 2 seconds
            metrics = get_current_metrics()
            await websocket.send_json(metrics)
            await asyncio.sleep(2)

    except WebSocketDisconnect:
        active_connections.remove(websocket)


# ============================================================================
# Helper Functions
# ============================================================================

def get_current_metrics() -> Dict:
    """Get current system metrics"""
    metrics = {
        "timestamp": datetime.now().isoformat(),
        "domains": {
            "total": len(mdsa_orchestrator.domains) if mdsa_orchestrator else 0,
            "active": 0  # TODO: Track active domains
        },
        "requests": {
            "total": len(request_history),
            "recent": len([r for r in request_history if datetime.fromisoformat(r['timestamp']) > datetime.now().replace(microsecond=0).replace(second=0)]) if request_history else 0
        },
        "rag": {"global_rag": {"document_count": 0}, "local_rags": {}},  # RAG not exposed by orchestrator
        "orchestrator": mdsa_orchestrator.get_stats() if mdsa_orchestrator else {}
    }

    return metrics


# ============================================================================
# Main Entry Point
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*60)
    print("MDSA Framework - Monitoring Dashboard")
    print("="*60)
    print("\nStarting server...")
    print("Dashboard will be available at: http://localhost:5000/welcome")
    print("\nRoutes:")
    print("  - http://localhost:5000/welcome (Landing page)")
    print("  - http://localhost:5000/monitor (Monitoring dashboard)")
    print("  - http://localhost:5000/docs (API documentation)")
    print("="*60 + "\n")

    # Start background task for WebSocket broadcasting
    # asyncio.create_task(broadcast_metrics())  # Commented out - will work when run with uvicorn

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=5000,
        log_level="info"
    )
