"""
MDSA Full-Featured Dashboard Module

This is the FastAPI-based dashboard with:
- Dark theme UI
- Real-time monitoring with D3.js visualizations
- RAG document upload and management
- Tool integration UI
- Model management
- Domain management
"""

from pathlib import Path

DASHBOARD_DIR = Path(__file__).parent

def run_dashboard(port: int = 9000, host: str = '0.0.0.0'):
    """Run the FastAPI dashboard server."""
    import uvicorn
    from .app import app
    
    print(f'Starting MDSA Dashboard on http://{host}:{port}')
    uvicorn.run(app, host=host, port=port)

__all__ = ['run_dashboard', 'DASHBOARD_DIR']
