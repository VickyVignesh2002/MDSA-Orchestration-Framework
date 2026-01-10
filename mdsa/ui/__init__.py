"""
MDSA UI Module

Full-featured FastAPI Dashboard with:
- Dark theme modern UI
- Real-time monitoring with D3.js visualizations
- RAG document upload and management
- Tool integration UI
- Model management
- Domain management
- WebSocket for live metrics
"""

from mdsa.ui.dashboard import run_dashboard, DASHBOARD_DIR
from mdsa.ui.dashboard.app import app as dashboard_app

__all__ = ['run_dashboard', 'DASHBOARD_DIR', 'dashboard_app']
