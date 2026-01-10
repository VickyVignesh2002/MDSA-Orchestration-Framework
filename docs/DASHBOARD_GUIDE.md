# MDSA Dashboard Guide

The MDSA Framework includes a production-ready monitoring dashboard for real-time visibility into system performance, domain routing, and knowledge base management.

## Overview

The dashboard provides:
- Real-time metrics monitoring
- Domain management and visualization
- RAG knowledge base administration
- Model configuration and status
- Tool registry management
- Authentication and access control

## Quick Start

### Starting the Dashboard

```bash
# Start dashboard on default port (9000)
python -m mdsa.ui.dashboard.app

# Start on custom port
python -m mdsa.ui.dashboard.app --port 8080

# Start with debug mode
python -m mdsa.ui.dashboard.app --debug
```

### Accessing the Dashboard

Open your browser to: `http://localhost:9000`

Default credentials:
- **Username**: `admin`
- **Password**: Set via `MDSA_ADMIN_PASSWORD` environment variable

## Dashboard Features

### 1. Main Dashboard (`/dashboard`)

The main view provides an overview of system health:

| Section | Description |
|---------|-------------|
| **Active Domains** | Number of registered domains |
| **RAG Documents** | Total documents in knowledge bases |
| **Active Tools** | Registered external tools |
| **Uptime** | System uptime since last restart |
| **Request Metrics** | P50, P95, P99 latency charts |
| **Domain Distribution** | Pie chart of query routing |

### 2. Domains Management (`/dashboard/domains`)

View and configure domain specialists:

- **Domain List**: All registered domains with descriptions
- **Keywords**: Domain-specific trigger keywords
- **Model Assignment**: Which LLM handles each domain
- **Confidence Thresholds**: Routing confidence settings

**API Endpoint**: `GET /api/domains`

```json
{
  "domains": [
    {
      "name": "medical_coding",
      "description": "Medical coding for ICD-10, CPT codes",
      "model": "deepseek-coder:1.3b",
      "keywords": ["code", "icd", "cpt", "diagnosis"],
      "source": "running_app"
    }
  ]
}
```

### 3. RAG Administration (`/dashboard/admin/rag`)

Manage knowledge bases:

**Upload Documents**:
- Drag-and-drop file upload
- Supported formats: PDF, TXT, MD, JSON
- Automatic chunking (500-1000 tokens)

**Knowledge Base Statistics**:
- Global KB document count
- Per-domain local KB counts
- Embedding status

**Document Management**:
- View indexed documents
- Delete documents
- Re-index knowledge base

### 4. Models Configuration (`/dashboard/admin/models`)

Configure LLM providers:

**Local Models (Ollama)**:
- List available models
- Pull new models
- Configure quantization

**Cloud Models**:
- API key configuration
- Model selection
- Rate limit settings

### 5. Tools Registry (`/dashboard/admin/tools`)

Manage external tool integrations:

- View registered tools
- Enable/disable tools
- Configure tool parameters
- Test tool execution

## Dashboard Architecture

```
mdsa/ui/dashboard/
├── app.py                 # FastAPI application (main entry)
├── templates/
│   ├── base.html          # Base template with navigation
│   ├── welcome.html       # Landing/login page
│   ├── dashboard.html     # Main dashboard view
│   ├── domains.html       # Domain management
│   ├── admin_rag.html     # RAG administration
│   ├── admin_models.html  # Model configuration
│   └── admin_tools.html   # Tools registry
└── static/
    ├── css/
    │   └── dashboard.css  # Dark theme styles (CSS variables)
    └── js/
        └── visualizations.js  # D3.js charts
```

## Color Customization

The dashboard uses CSS custom properties for theming. Edit `dashboard.css` to customize:

```css
:root {
    /* Primary Colors */
    --primary: #6366F1;        /* Indigo - main accent */
    --primary-dark: #4F46E5;   /* Darker accent for hover */
    --secondary: #8B5CF6;      /* Violet - secondary accent */

    /* Status Colors */
    --success: #10B981;        /* Green */
    --warning: #F59E0B;        /* Orange/Amber */
    --danger: #EF4444;         /* Red */

    /* Background Colors */
    --background: #0F172A;     /* Page background - Dark slate */
    --surface: #1E293B;        /* Card backgrounds */
    --surface-light: #334155;  /* Hover states */

    /* Text Colors */
    --text-primary: #F1F5F9;   /* Main text */
    --text-secondary: #CBD5E1; /* Secondary text */
    --border: #475569;         /* Border color */
}
```

### Changing to Light Theme

To switch to a light theme, update the variables:

```css
:root {
    --background: #F8FAFC;
    --surface: #FFFFFF;
    --surface-light: #F1F5F9;
    --text-primary: #1E293B;
    --text-secondary: #64748B;
    --border: #E2E8F0;
}
```

## Security Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `MDSA_ADMIN_PASSWORD` | Dashboard admin password | Yes |
| `MDSA_JWT_SECRET` | JWT token signing secret | Yes |
| `MDSA_ENCRYPTION_KEY` | Data encryption key | Recommended |

### Example `.env` File

```bash
MDSA_ADMIN_PASSWORD=your_secure_password_here
MDSA_JWT_SECRET=your_64_char_hex_secret_here
MDSA_ENCRYPTION_KEY=your_64_char_hex_key_here
```

### Authentication Flow

1. User visits dashboard → Redirected to `/welcome` (login)
2. Enter credentials → POST to `/auth/login`
3. Server validates → Returns JWT token in cookie
4. Browser stores cookie → Sent with subsequent requests
5. Protected routes check JWT → Allow/deny access

## API Reference

### Public Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Redirect to dashboard |
| `/welcome` | GET | Login page |
| `/auth/login` | POST | Authenticate user |
| `/auth/logout` | POST | End session |
| `/health` | GET | System health check |

### Protected Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/dashboard` | GET | Main dashboard |
| `/dashboard/domains` | GET | Domain management |
| `/dashboard/admin/rag` | GET | RAG administration |
| `/api/domains` | GET | List domains (JSON) |
| `/api/metrics` | GET | Current metrics (JSON) |
| `/api/rag/stats` | GET | RAG statistics (JSON) |
| `/api/rag/documents` | POST | Upload document |
| `/api/rag/documents/{id}` | DELETE | Delete document |

## Troubleshooting

### Port Already in Use

```bash
# Find process using port 9000
netstat -ano | findstr :9000

# Kill the process (Windows)
taskkill /PID <process_id> /F

# Or start on different port
python -m mdsa.ui.dashboard.app --port 9001
```

### RAG Shows 0 Documents

1. Ensure ChromaDB is installed: `pip install chromadb`
2. Check knowledge base path exists
3. Verify documents are indexed:
   ```python
   from mdsa import DualRAG
   rag = DualRAG()
   print(rag.global_rag.get_document_count())
   ```

### Dashboard Not Loading

1. Check console for JavaScript errors
2. Verify static files are served correctly
3. Clear browser cache
4. Check Flask/FastAPI server logs

### Authentication Issues

1. Verify `MDSA_ADMIN_PASSWORD` is set
2. Check JWT secret is valid (64 hex characters)
3. Clear cookies and re-login
4. Check server logs for authentication errors

## Integration with MDSA Apps

The dashboard can connect to running MDSA applications:

```python
from mdsa.ui.dashboard.app import DashboardRegistry

# Register your app with the dashboard
registry = DashboardRegistry()
registry.register_app(
    name="medical_chatbot",
    endpoint="http://localhost:8000",
    domains=["medical_coding", "medical_billing"]
)
```

Once registered, the dashboard will:
- Fetch live metrics from your app
- Display domains from your app
- Aggregate RAG statistics

## Version

- **Dashboard Version**: 1.0.3
- **Framework**: FastAPI + Jinja2 + D3.js
- **Theme**: Dark (CSS Custom Properties)
