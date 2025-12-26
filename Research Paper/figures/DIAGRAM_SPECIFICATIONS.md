# MDSA Research Paper - Diagram Specifications

This document provides detailed specifications for the 6 professional diagrams required for the research paper. Each diagram should be created as a PNG file with 300 DPI resolution, dimensions approximately 6-8 inches wide to fit IEEE conference format.

---

## Figure 1: System Architecture Diagram
**Filename**: `architecture_diagram.png`

### Purpose
Show the overall MDSA system architecture from query input to response output.

### Components to Include

1. **User Query Input** (Top)
   - Arrow labeled "User Query q"

2. **TinyBERT Router** (First major component)
   - Box labeled "TinyBERT Router (67M params)"
   - Sub-component: "Domain Classification: 25-61ms"
   - Side cache: "Domain Embedding Cache" (shown as cylinder/database)
   - Arrow showing "80% faster with cache"

3. **Response Cache Check** (Second component)
   - Box labeled "Response Cache"
   - Diamond decision: "Cache Hit?"
   - Path: YES → Return cached response (<10ms)
   - Path: NO → Continue to RAG

4. **Dual RAG System** (Third component)
   - Two parallel boxes:
     * "Global Knowledge Base (10,000+ docs)"
     * "Local Domain KB (1,000 docs per domain)"
   - Arrows converging to "Context Retrieval (60ms)"
   - Label: "Precision@3: 87.3%"

5. **Hybrid Orchestrator** (Fourth component)
   - Diamond decision: "Complex Query?"
   - Path: YES → "Phi-2 Reasoner (2.7B params)"
   - Path: NO → "Domain Specialist Model (Ollama)"
   - Both paths show "Inference: ~500ms"

6. **Response Generation & Tracking** (Bottom)
   - Box: "Generate Response"
   - Arrows to:
     * "Cache Response" (feedback loop)
     * "Log to Dashboard"
     * "Return to User"

7. **Monitoring Dashboard** (Side panel)
   - Box: "Flask Dashboard (port 9000)"
   - Metrics listed:
     * Real-time request tracking
     * Performance metrics
     * Domain distribution
     * Cache hit rates

### Color Scheme
- TinyBERT Router: Light blue (#3498db)
- Caches: Yellow (#f39c12)
- RAG System: Green (#27ae60)
- Models: Purple (#9b59b6)
- Dashboard: Orange (#e67e22)

### Style
- Clean, professional boxes with rounded corners
- Arrows with labels showing latency/timing
- Use different shapes: rectangles for processes, cylinders for databases, diamonds for decisions
- Include performance metrics as annotations

---

## Figure 2: Sequence Diagram
**Filename**: `sequence_diagram.png`

### Purpose
Show the temporal flow of a query through the system with timing annotations.

### Actors (Vertical Lifelines)
1. User
2. TinyBERT Router
3. Domain Embedding Cache
4. Response Cache
5. Dual RAG System
6. Domain Specialist Model
7. Dashboard

### Sequence Flow

1. **User → Router**: Submit query q
2. **Router → Domain Embedding Cache**: Check cache (5ms)
3. **Domain Embedding Cache → Router**: Cache hit/miss
4. **Router (self)**: Classify domain (25-61ms)
5. **Router → Response Cache**: Check for cached response (1ms)
6. **Response Cache → Router**: Cache miss
7. **Router → RAG System**: Retrieve context for domain
8. **RAG System (self)**: Search global + local KB (60ms)
9. **RAG System → Router**: Return top-k documents
10. **Router → Domain Model**: Generate response with context
11. **Domain Model (self)**: Inference (500ms)
12. **Domain Model → Router**: Return generated response
13. **Router → Response Cache**: Cache response
14. **Router → Dashboard**: Log metrics (async)
15. **Router → User**: Return response

### Timing Annotations
- Show cumulative time on right side:
  * 0ms: Query received
  * 5ms: Cache check complete
  * 66ms: Domain classified
  * 67ms: Response cache check
  * 127ms: RAG retrieval complete
  * 627ms: Response generated
  * 630ms: Response cached and logged
  * 630ms: Response returned

- Total latency: **630ms** (highlight this)

### Style
- Standard UML sequence diagram format
- Dashed return arrows
- Timing annotations in boxes on the right
- Critical path highlighted in bold/color

---

## Figure 3: Technology Stack Diagram
**Filename**: `tech_stack_diagram.png`

### Purpose
Show the layered technology architecture.

### Layers (Bottom to Top)

**Layer 1: Storage & Infrastructure**
- ChromaDB (Vector database)
- In-Memory Cache (Response cache)
- Ollama (Local model server)
- File System (Knowledge base documents)

**Layer 2: Core Models**
- TinyBERT (67M - Router)
- Phi-2 (2.7B - Reasoner)
- Domain Models (Deepseek, Llama, Mistral)
- Sentence Transformers (Embeddings)

**Layer 3: Framework Core**
- Router Module
- Orchestrator Module
- RAG Engine (Dual KB)
- Cache Manager
- Domain Manager

**Layer 4: APIs & Integrations**
- Ollama Integration
- OpenAI API
- Anthropic API
- Google Gemini API
- Custom Tool System

**Layer 5: Application Layer**
- Flask Dashboard (UI)
- Gradio Interface (Chatbot)
- REST API (FastAPI)
- Monitoring & Logging

**Layer 6: Client Applications**
- Web Browser
- API Clients
- Mobile Apps (future)

### Visual Style
- Horizontal layers, stacked vertically
- Each layer has multiple components shown as boxes
- Arrows showing dependencies between layers
- Technology logos if possible (e.g., Python, Flask, D3.js)
- Color-coded by function type (data=blue, models=purple, APIs=green, UI=orange)

---

## Figure 4: Performance Comparison Chart
**Filename**: `performance_comparison.png`

### Purpose
Visual comparison of MDSA vs alternatives across key metrics.

### Chart Type
Combined bar chart with 3 sub-charts side-by-side:

**Sub-chart 1: Latency (ms)**
- X-axis: MDSA, LangChain, AutoGen, CrewAI
- Y-axis: Milliseconds (0-2500)
- Bars:
  * MDSA: 625ms (GREEN - best)
  * LangChain: 1,850ms (YELLOW)
  * AutoGen: 2,100ms (ORANGE)
  * CrewAI: 1,950ms (ORANGE)
- Title: "Average Response Latency"
- Annotation: "MDSA: 2.4x faster"

**Sub-chart 2: Memory (MB)**
- X-axis: MDSA, LangChain, AutoGen, CrewAI
- Y-axis: Megabytes (0-4000)
- Bars:
  * MDSA: 910MB (GREEN - best)
  * LangChain: 2,300MB (YELLOW)
  * AutoGen: 3,500MB (RED)
  * CrewAI: 2,800MB (ORANGE)
- Title: "Memory Consumption"
- Annotation: "MDSA: 60% reduction"

**Sub-chart 3: Annual Cost ($)**
- X-axis: MDSA, LangChain, AutoGen, CrewAI
- Y-axis: Dollars (0-6000)
- Bars:
  * MDSA: $720 (GREEN - best)
  * LangChain: $2,900 (YELLOW)
  * AutoGen: $5,800 (RED)
  * CrewAI: $3,630 (ORANGE)
- Title: "Total Cost/Year (10K queries/day)"
- Annotation: "MDSA: 75-88% savings"

### Style
- Clean bar charts with grid lines
- Color coding: Green=best, Yellow=acceptable, Orange=higher, Red=highest
- Value labels on top of each bar
- Consistent axis scales for comparison
- Professional font (Arial or similar)

---

## Figure 5: Domain Classification Flow
**Filename**: `domain_classification_flow.png`

### Purpose
Detailed flowchart showing how domain classification works.

### Flow Steps

1. **Start**: Query q received
   ↓
2. **Compute Embedding**: e(q) = SentenceTransformer(q)
   ↓
3. **Decision: Cache Check**
   - Check if similar embedding in cache
   - If cosine_similarity > 0.95 → **Use Cached Domain** (Exit Fast Path)
   - Else → Continue
   ↓
4. **TinyBERT Classification**
   - Input: Query embedding e(q)
   - Process: Forward pass through TinyBERT
   - Output: Probability distribution p(d₁|q), p(d₂|q), ..., p(dₙ|q)
   ↓
5. **Select Max Probability**
   - d* = argmax(p(dᵢ|q))
   - confidence = max(p(dᵢ|q))
   ↓
6. **Decision: Confidence Threshold**
   - If confidence > 0.85 → **High Confidence** → Route to domain specialist
   - If 0.65 < confidence ≤ 0.85 → **Medium Confidence** → Route to domain + use Phi-2 reasoner
   - If confidence ≤ 0.65 → **Low Confidence** → Route to general reasoner
   ↓
7. **Cache Embedding**
   - Store e(q) → domain mapping in cache
   - Update cache hit statistics
   ↓
8. **End**: Return domain d* and confidence

### Visual Elements
- Rectangles for processes
- Diamonds for decisions
- Different colors for paths:
  * Fast path (cache hit): Green
  * High confidence: Blue
  * Medium confidence: Yellow
  * Low confidence: Orange
- Timing annotations (25-61ms total, 5ms cache, 20-56ms classification)

---

## Figure 6: Deployment Architecture
**Filename**: `deployment_architecture.png`

### Purpose
Show production deployment topology including scaling patterns.

### Components

**Client Tier**
- Multiple client boxes: Web Browser, Mobile App, API Client
- Arrow to Load Balancer

**Load Balancer**
- nginx (80/443)
- Round-robin routing
- Health check endpoint

**Application Tier** (Horizontal scaling)
- 3x MDSA Instances shown in parallel:
  * Instance 1 (port 5000)
  * Instance 2 (port 5001)
  * Instance 3 (port 5002)
- Each instance contains:
  - Flask API
  - Router
  - Orchestrator
  - RAG Engine

**Model Serving Tier**
- Ollama Server (localhost:11434)
- Model pool:
  * Deepseek-v3.1 (6.8B)
  * Phi-2 (2.7B)
  * TinyBERT (67M)
- GPU acceleration (RTX 3060)

**Storage Tier**
- ChromaDB (Vector database)
  * Global KB collection
  * Domain KB collections (x5)
- Shared cache (Redis - optional)
- Knowledge base files (mounted volume)

**Monitoring Tier**
- Dashboard (port 9000)
- Prometheus metrics scraper
- Grafana visualization
- Log aggregation (ELK stack - optional)

### Connections
- Clients → Load Balancer (HTTPS)
- Load Balancer → MDSA Instances (HTTP)
- MDSA Instances → Ollama (HTTP API)
- MDSA Instances → ChromaDB (Python client)
- MDSA Instances → Dashboard (metrics push)

### Annotations
- Instance capacity: 12.5 req/s each → 37.5 req/s total
- Failover: If instance fails, load balancer routes to healthy instances
- Scaling: Add instances horizontally to increase capacity
- Model sharing: All instances share Ollama server (single GPU)

### Visual Style
- Network diagram style
- Boxes for components, grouped by tier
- Dotted boxes for optional components
- Arrows labeled with protocols
- Color-coded by function (clients=blue, app=green, models=purple, storage=yellow, monitoring=orange)

---

## Creating the Diagrams

### Recommended Tools

**Option 1: Draw.io (Free, Web-based)**
1. Visit https://app.diagrams.net/
2. Create new diagram
3. Use shapes from library (flowchart, UML, network)
4. Export as PNG (300 DPI)

**Option 2: Lucidchart (Freemium)**
1. Sign up at https://www.lucidchart.com/
2. Use templates for flowcharts, sequence diagrams, architecture
3. Export as PNG (high quality)

**Option 3: Python Matplotlib/Seaborn (Programmatic)**
For Figure 4 (Performance Comparison):
```python
import matplotlib.pyplot as plt
import numpy as np

# Data
frameworks = ['MDSA', 'LangChain', 'AutoGen', 'CrewAI']
latency = [625, 1850, 2100, 1950]
memory = [910, 2300, 3500, 2800]
cost = [720, 2900, 5800, 3630]

# Create figure with 3 subplots
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))

# Latency chart
colors = ['green', 'yellow', 'orange', 'orange']
ax1.bar(frameworks, latency, color=colors)
ax1.set_ylabel('Milliseconds')
ax1.set_title('Average Response Latency')
ax1.text(0, 625, '625ms', ha='center', va='bottom')
# ... add more labels

# Memory chart
ax2.bar(frameworks, memory, color=colors)
ax2.set_ylabel('Megabytes')
ax2.set_title('Memory Consumption')

# Cost chart
ax3.bar(frameworks, cost, color=colors)
ax3.set_ylabel('Dollars')
ax3.set_title('Total Cost/Year')

plt.tight_layout()
plt.savefig('performance_comparison.png', dpi=300, bbox_inches='tight')
```

**Option 4: Microsoft Visio (Commercial)**
- Professional diagramming tool
- Templates for all diagram types
- Export high-quality PNG

### Export Settings
- **Format**: PNG
- **Resolution**: 300 DPI minimum
- **Width**: 6-8 inches (1800-2400 pixels at 300 DPI)
- **Background**: White
- **Fonts**: Arial, Helvetica, or similar sans-serif (10-12pt)
- **File size**: <1MB each (optimize if needed)

### Placement in LaTeX
Diagrams are referenced in the main paper using:
```latex
\begin{figure}[htbp]
\centering
\includegraphics[width=\columnwidth]{figures/architecture_diagram.png}
\caption{MDSA System Architecture showing TinyBERT router, dual RAG system, and hybrid orchestration.}
\label{fig:architecture}
\end{figure}
```

Replace the corresponding figure references in the LaTeX file once diagrams are created.

---

## Next Steps

1. **Create diagrams** using one of the recommended tools
2. **Save PNG files** to the `figures/` directory with specified filenames
3. **Update LaTeX**: Replace figure placeholders with actual `\includegraphics` commands
4. **Compile PDF**: Run `pdflatex` → `bibtex` → `pdflatex` → `pdflatex`
5. **Review**: Check that all figures render correctly and are referenced in text

---

**Total Diagrams**: 6
**Estimated Time**: 2-4 hours for all diagrams
**Quality Goal**: Publication-ready for IEEE conference submission
