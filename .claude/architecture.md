# MDSA Framework - Complete Architecture Documentation with Mermaid Diagrams

## 1. HIGH-LEVEL SYSTEM ARCHITECTURE

```mermaid
graph TB
    subgraph "User Interface Layer"
        UI[Web UI - localhost:8000/monitor]
        API[REST API Endpoints]
        CLI[Command Line Interface]
    end
  
    subgraph "Core Orchestration Layer"
        ORCH[TinyBERT Orchestrator<br/>67M params - CPU]
        ROUTER[Intent Router<br/>95% Accuracy]
        SM[State Machine<br/>Workflow Controller]
        MB[Message Bus<br/>Event System]
    end
  
    subgraph "Domain Management Layer"
        DR[Domain Registry]
        DB[Domain Builder]
        DT[Domain Templates]
    
        subgraph "Domain 1: Finance"
            D1M1[SLM-Transactions 8B]
            D1M2[SLM-Reporting 13B]
            D1M3[SLM-Risk 13B]
            D1RAG[Local RAG]
        end
    
        subgraph "Domain 2: Development"
            D2M1[SLM-CodeAnalysis 13B]
            D2M2[SLM-Testing 8B]
            D2M3[SLM-Integration 8B]
            D2RAG[Local RAG]
        end
    
        subgraph "Domain 3: Customer Service"
            D3M1[SLM-Support 8B]
            D3M2[SLM-Routing 7B]
            D3RAG[Local RAG]
        end
    end
  
    subgraph "Model Management Layer"
        MM[Model Manager]
    
        subgraph "Model Loaders"
            HF[HuggingFace Loader]
            GH[GitHub Loader]
            LOCAL[Local Loader]
            OLLAMA[Ollama Loader]
            OPENAI[OpenAI Loader]
            CUSTOM[Custom Loader]
        end
    end
  
    subgraph "RAG System Layer"
        LRAG[Local RAG Engine<br/>Per-Domain Knowledge]
        GRAG[Global RAG Engine<br/>Cross-Domain Knowledge]
        VS[Vector Store<br/>Chroma/FAISS/Pinecone]
        EMB[Embedding Models<br/>SentenceTransformers]
    end
  
    subgraph "Communication Layer"
        BUS[Message Bus]
        BRIDGE[SLM Bridge<br/>Model-to-Model]
        TOOL[Tool Adapter<br/>Model-to-Tool]
        PROTO[Communication Protocols]
    end
  
    subgraph "Validation Layer"
        RULES[Rule-Based Validator<br/>Pure Python]
        REASON[Reasoning Validator<br/>Phi-1.5 1.3B]
        SCHEMA[Schema Validator<br/>JSON Schema]
    end
  
    subgraph "Integration Layer"
        MCP[MCP Manager<br/>Model Context Protocol]
        APIM[API Key Manager<br/>Encrypted Storage]
        TOOLS[External Tools]
    end
  
    subgraph "Monitoring & Observability Layer"
        MC[Metrics Collector]
        ET[Event Tracker]
        RM[Resource Monitor<br/>CPU/GPU/Memory]
        FA[Flow Analyzer]
        WS[WebSocket Server]
        PROM[Prometheus Exporter]
    end
  
    subgraph "Storage Layer"
        CACHE[Model Cache<br/>~/.mdsa/models/]
        VSTORE[Vector Store DB]
        LOGS[Log Storage]
        CONFIG[Config Files<br/>YAML]
    end
  
    UI --> API
    CLI --> API
    API --> ORCH
  
    ORCH --> ROUTER
    ORCH --> SM
    ORCH --> MB
  
    ROUTER --> DR
    SM --> DR
    MB --> BUS
  
    DR --> D1M1 & D1M2 & D1M3
    DR --> D2M1 & D2M2 & D2M3
    DR --> D3M1 & D3M2
  
    D1M1 & D1M2 & D1M3 --> D1RAG
    D2M1 & D2M2 & D2M3 --> D2RAG
    D3M1 & D3M2 --> D3RAG
  
    D1RAG & D2RAG & D3RAG --> LRAG
    LRAG --> GRAG
    GRAG --> VS
    VS --> EMB
  
    MM --> HF & GH & LOCAL & OLLAMA & OPENAI & CUSTOM
    MM --> CACHE
  
    D1M1 & D1M2 & D1M3 & D2M1 & D2M2 & D2M3 & D3M1 & D3M2 --> MM
  
    BUS --> BRIDGE
    BUS --> TOOL
    BRIDGE --> PROTO
  
    SM --> RULES
    SM --> REASON
    SM --> SCHEMA
  
    ORCH --> MCP
    MCP --> APIM
    MCP --> TOOLS
  
    ORCH --> MC
    BUS --> ET
    MM --> RM
    ROUTER --> FA
  
    MC & ET & RM & FA --> WS
    MC --> PROM
    WS --> UI
  
    CONFIG --> DR
    LOGS --> ET
    VSTORE --> VS
  
    style UI fill:#e1f5ff
    style ORCH fill:#fff9c4
    style D1M1 fill:#00008B
    style D2M1 fill:#00008B
    style D3M1 fill:#00008B
    style LRAG fill:#c8e6c9
    style MC fill:#f5f5f5

```

## 2. DETAILED ORCHESTRATION FLOW

```mermaid
stateDiagram-v2
    [*] --> INIT: User Query Received
  
    INIT --> CLASSIFY: Parse & Validate Input
  
    CLASSIFY --> ROUTE: TinyBERT Classification
  
    ROUTE --> CONFIDENCE_CHECK: Domain + Score
  
    CONFIDENCE_CHECK --> ESCALATE: Confidence < 0.85
    CONFIDENCE_CHECK --> LOAD_DOMAIN: Confidence >= 0.85
  
    ESCALATE --> HUMAN_REVIEW: Low Confidence
    HUMAN_REVIEW --> [*]
  
    LOAD_DOMAIN --> CHECK_RAG: Activate Domain SLMs
  
    CHECK_RAG --> RETRIEVE_LOCAL: RAG Enabled (Local)
    CHECK_RAG --> RETRIEVE_GLOBAL: RAG Enabled (Global)
    CHECK_RAG --> PLAN: RAG Disabled
  
    RETRIEVE_LOCAL --> PLAN: Context Retrieved
    RETRIEVE_GLOBAL --> PLAN: Context Retrieved
  
    PLAN --> VALIDATE_PRE: Generate Action Plan
  
    VALIDATE_PRE --> SCHEMA_VAL: Check Preconditions
  
    SCHEMA_VAL --> RULES_VAL: Schema Valid
    SCHEMA_VAL --> VALIDATION_FAILED: Schema Invalid
  
    RULES_VAL --> REASONING_VAL: Rules Passed
    RULES_VAL --> VALIDATION_FAILED: Rules Failed
  
    REASONING_VAL --> EXECUTE: Complex Logic Validated
    REASONING_VAL --> VALIDATION_FAILED: Reasoning Failed
  
    EXECUTE --> TOOL_CALL: Invoke External Tools
    EXECUTE --> SLM_PROCESS: Direct SLM Processing
  
    TOOL_CALL --> SLM_PROCESS: Tool Results Retrieved
  
    SLM_PROCESS --> VALIDATE_POST: Generate Response
  
    VALIDATE_POST --> OUTPUT_VAL: Check Response
  
    OUTPUT_VAL --> LOG: Output Valid
    OUTPUT_VAL --> RETRY: Output Invalid (Retry < 3)
    OUTPUT_VAL --> VALIDATION_FAILED: Output Invalid (Retry >= 3)
  
    RETRY --> PLAN: Retry with Feedback
  
    LOG --> UNLOAD_DOMAIN: Record Execution
  
    UNLOAD_DOMAIN --> UPDATE_METRICS: Cleanup Resources
  
    UPDATE_METRICS --> RETURN: Update Monitoring
  
    RETURN --> [*]: Send Response to User
  
    VALIDATION_FAILED --> ERROR_HANDLER: Handle Failure
    ERROR_HANDLER --> [*]: Return Error Response
```

## 3. DOMAIN CREATION WORKFLOW

```mermaid
flowchart TD
    START([User Wants New Domain]) --> METHOD{Choose Creation Method}
  
    METHOD -->|Beginner| SIMPLE[SimpleDomainAPI.create_domain]
    METHOD -->|Intermediate| YAML[YAML Configuration]
    METHOD -->|Advanced| PYTHON[Python API]
    METHOD -->|Interactive| CLI[Interactive CLI Builder]
  
    SIMPLE --> SIMPLE_INPUT[/name: str<br/>model: str/]
    SIMPLE_INPUT --> QUICK_BUILD[DomainBuilder.quick_start]
  
    YAML --> YAML_FILE[Create domain.yaml]
    YAML_FILE --> YAML_PARSE[Parse YAML Config]
    YAML_PARSE --> EXTRACT_CONFIG[Extract Settings:<br/>- Models<br/>- RAG<br/>- Tools<br/>- Validators]
  
    PYTHON --> DICT_CONFIG[/Create config dict/]
    DICT_CONFIG --> FROM_DICT[DomainBuilder.from_dict]
  
    CLI --> PROMPTS[Interactive Prompts:<br/>1. Domain name<br/>2. Model source<br/>3. Model path<br/>4. RAG settings<br/>5. Tools]
    PROMPTS --> CLI_BUILD[Generate Config]
    CLI_BUILD --> SAVE_YAML[Save to YAML]
    SAVE_YAML --> YAML_PARSE
  
    QUICK_BUILD --> VALIDATE{Validate Config}
    EXTRACT_CONFIG --> VALIDATE
    FROM_DICT --> VALIDATE
  
    VALIDATE -->|Invalid| ERROR[Show Error Message]
    ERROR --> METHOD
  
    VALIDATE -->|Valid| INIT_DOMAIN[Initialize Domain Object]
  
    INIT_DOMAIN --> SETUP_MODELS[Setup Models:<br/>1. Detect source<br/>2. Load appropriate loader<br/>3. Download if needed<br/>4. Quantize if specified]
  
    SETUP_MODELS --> SETUP_RAG{RAG Enabled?}
  
    SETUP_RAG -->|Yes| RAG_CONFIG[Configure RAG:<br/>1. Initialize vector store<br/>2. Load embeddings<br/>3. Index documents<br/>4. Set scope local/global]
    SETUP_RAG -->|No| SETUP_TOOLS
  
    RAG_CONFIG --> SETUP_TOOLS[Setup Tools:<br/>1. Parse tool configs<br/>2. Initialize connections<br/>3. Validate endpoints]
  
    SETUP_TOOLS --> SETUP_VALIDATORS[Setup Validators:<br/>1. Schema validators<br/>2. Rule-based<br/>3. Reasoning validators]
  
    SETUP_VALIDATORS --> SETUP_COMMS[Setup Communication:<br/>1. Register with message bus<br/>2. Connect to other domains<br/>3. Setup protocols]
  
    SETUP_COMMS --> REGISTER[Register with Domain Registry]
  
    REGISTER --> VERIFY[Verification Tests:<br/>1. Model loads<br/>2. RAG queries work<br/>3. Tools respond<br/>4. Validators pass]
  
    VERIFY -->|Failed| ROLLBACK[Rollback & Cleanup]
    ROLLBACK --> ERROR
  
    VERIFY -->|Passed| ACTIVATE[Activate Domain]
  
    ACTIVATE --> MONITOR[Start Monitoring:<br/>1. Register metrics<br/>2. Setup event tracking<br/>3. Enable UI visibility]
  
    MONITOR --> READY([Domain Ready for Use])
  
    style START fill:#e1f5ff
    style READY fill:#c8e6c9
    style ERROR fill:#ffcdd2
    style VALIDATE fill:#fff9c4
```

## 4. MODEL LOADING ARCHITECTURE

```mermaid
flowchart LR
    subgraph "Model Sources"
        HF[🤗 HuggingFace<br/>Hub]
        GH[🌐 GitHub<br/>Repositories]
        LOCAL[💾 Local Files<br/>/path/to/model]
        OLLAMA[🦙 Ollama<br/>Server]
        OPENAI[🔑 OpenAI<br/>API]
        CUSTOM[⚙️ Custom<br/>Endpoint]
    end
  
    subgraph "Model Manager"
        DETECT[Source Detector]
        ROUTER[Loader Router]
        CACHE_CHECK{In Cache?}
        DOWNLOAD[Download Manager<br/>Progress Bar]
        QUANTIZE{Quantization?}
        LOAD[Model Loader]
        REGISTRY[Model Registry<br/>Tracking]
    end
  
    subgraph "Model Loaders"
        HFL[HuggingFace Loader<br/>transformers]
        GHL[GitHub Loader<br/>HTTP Download]
        LOCALL[Local Loader<br/>File System]
        OLLAMAL[Ollama Loader<br/>REST API]
        OPENAIL[OpenAI Loader<br/>API Client]
        CUSTOML[Custom Loader<br/>Plugin System]
    end
  
    subgraph "Post-Processing"
        QUANT4[4-bit Quantization<br/>bitsandbytes]
        QUANT8[8-bit Quantization<br/>bitsandbytes]
        LORA[LoRA Adapter<br/>PEFT]
        DEVICE[Device Placement<br/>CPU/CUDA/MPS]
    end
  
    subgraph "Cache Storage"
        MODELCACHE[~/.mdsa/models/<br/>Model Files]
        METADATA[Model Metadata<br/>config.json]
    end
  
    REQUEST[Model Load Request<br/>name, source, path] --> DETECT
  
    DETECT --> ROUTER
  
    ROUTER --> CACHE_CHECK
  
    CACHE_CHECK -->|Yes| LOAD
    CACHE_CHECK -->|No| DOWNLOAD
  
    ROUTER -.->|HuggingFace| HFL
    ROUTER -.->|GitHub| GHL
    ROUTER -.->|Local| LOCALL
    ROUTER -.->|Ollama| OLLAMAL
    ROUTER -.->|OpenAI| OPENAIL
    ROUTER -.->|Custom| CUSTOML
  
    HF --> HFL
    GH --> GHL
    LOCAL --> LOCALL
    OLLAMA --> OLLAMAL
    OPENAI --> OPENAIL
    CUSTOM --> CUSTOML
  
    HFL & GHL & LOCALL & OLLAMAL & OPENAIL & CUSTOML --> DOWNLOAD
  
    DOWNLOAD --> MODELCACHE
    MODELCACHE --> LOAD
  
    LOAD --> QUANTIZE
  
    QUANTIZE -->|4-bit| QUANT4
    QUANTIZE -->|8-bit| QUANT8
    QUANTIZE -->|None| DEVICE
  
    QUANT4 --> LORA
    QUANT8 --> LORA
  
    LORA --> DEVICE
  
    DEVICE --> REGISTRY
  
    REGISTRY --> METADATA
  
    REGISTRY --> READY([Model Ready])
  
    style REQUEST fill:#e1f5ff
    style READY fill:#c8e6c9
    style CACHE_CHECK fill:#fff9c4
    style QUANTIZE fill:#fff9c4
```

## 5. RAG SYSTEM ARCHITECTURE

```mermaid
graph TB
    subgraph "Document Sources"
        FILES[Local Files<br/>txt, md, pdf, docx]
        URLS[Web URLs<br/>API Endpoints]
        DB[Databases<br/>SQL, NoSQL]
        CLOUD[Cloud Storage<br/>S3, GCS]
    end
  
    subgraph "Document Processing"
        LOADER[Document Loader]
        PARSER[Format Parser<br/>Text Extraction]
        CHUNKER[Document Chunker<br/>Size: 512, Overlap: 50]
        METADATA[Metadata Extractor<br/>Source, Timestamp, Domain]
    end
  
    subgraph "Embedding Generation"
        EMB_MODEL[Embedding Model<br/>SentenceTransformers]
        EMB_CACHE[Embedding Cache]
    end
  
    subgraph "Local RAG - Per Domain"
        LRAG1[Finance Domain RAG<br/>Chroma Collection]
        LRAG2[Development Domain RAG<br/>Chroma Collection]
        LRAG3[Support Domain RAG<br/>Chroma Collection]
    end
  
    subgraph "Global RAG - Cross Domain"
        GRAG[Global Knowledge Base<br/>Shared Collection]
        DOMAIN_TAG[Domain Tagging System]
    end
  
    subgraph "Vector Stores"
        CHROMA[ChromaDB<br/>Persistent Storage]
        FAISS[FAISS<br/>Fast Similarity Search]
        PINECONE[Pinecone<br/>Cloud Vector DB]
    end
  
    subgraph "Retrieval System"
        QUERY_EMB[Query Embedding]
        SIMILARITY[Similarity Search<br/>Cosine/Euclidean]
        RERANK[Re-ranking<br/>Cross-Encoder]
        FILTER[Domain Filtering]
    end
  
    subgraph "Integration"
        CONTEXT[Context Builder]
        AUGMENT[Prompt Augmentation]
        SLM_INPUT[SLM Input with Context]
    end
  
    FILES & URLS & DB & CLOUD --> LOADER
  
    LOADER --> PARSER
    PARSER --> CHUNKER
    CHUNKER --> METADATA
  
    METADATA --> EMB_MODEL
    EMB_MODEL --> EMB_CACHE
  
    EMB_CACHE -->|Domain Specific| LRAG1 & LRAG2 & LRAG3
    EMB_CACHE -->|Shared Knowledge| GRAG
  
    GRAG --> DOMAIN_TAG
  
    LRAG1 & LRAG2 & LRAG3 --> CHROMA
    GRAG --> CHROMA
  
    CHROMA -.->|Alternative| FAISS
    CHROMA -.->|Alternative| PINECONE
  
    USER_QUERY[User Query] --> QUERY_EMB
    QUERY_EMB --> SIMILARITY
  
    SIMILARITY --> LRAG1 & LRAG2 & LRAG3 & GRAG
  
    LRAG1 & LRAG2 & LRAG3 & GRAG --> FILTER
    FILTER --> RERANK
  
    RERANK --> CONTEXT
    CONTEXT --> AUGMENT
    AUGMENT --> SLM_INPUT
  
    SLM_INPUT --> SLM_PROCESS[SLM Processing<br/>with Retrieved Context]
  
    style USER_QUERY fill:#e1f5ff
    style SLM_PROCESS fill:#c8e6c9
```

## 6. COMMUNICATION & MESSAGE FLOW

```mermaid
sequenceDiagram
    participant User
    participant Orchestrator
    participant MessageBus
    participant Domain1 as Finance Domain
    participant Domain2 as Risk Domain
    participant RAG
    participant Tool as External Tool
    participant Monitor as Monitoring System
  
    User->>Orchestrator: Submit Query
    activate Orchestrator
  
    Orchestrator->>MessageBus: Publish(QUERY, Finance)
    activate MessageBus
  
    MessageBus->>Monitor: Track Event(Query Received)
    MessageBus->>Domain1: Route to Finance Domain
    activate Domain1
  
    Domain1->>RAG: Retrieve Context(query)
    activate RAG
    RAG-->>Domain1: Relevant Documents
    deactivate RAG
  
    Domain1->>Domain1: Generate Action Plan
  
    Domain1->>MessageBus: Publish(MODEL_TO_MODEL, Risk)
    MessageBus->>Domain2: Forward to Risk Domain
    activate Domain2
  
    Domain2->>Domain2: Assess Risk
    Domain2->>MessageBus: Publish(RESPONSE, Finance)
    MessageBus->>Domain1: Risk Assessment Result
    deactivate Domain2
  
    Domain1->>MessageBus: Publish(TOOL_CALL, Budget API)
    MessageBus->>Tool: Execute Tool
    activate Tool
    Tool-->>MessageBus: Tool Result
    MessageBus-->>Domain1: Tool Response
    deactivate Tool
  
    Domain1->>Domain1: Generate Final Response
  
    Domain1->>MessageBus: Publish(RESPONSE, User)
    deactivate Domain1
  
    MessageBus->>Monitor: Track Event(Response Generated)
    MessageBus->>Orchestrator: Final Response
    deactivate MessageBus
  
    Orchestrator-->>User: Return Result
    deactivate Orchestrator
  
    Note over Monitor: Update Metrics:<br/>- Latency<br/>- Token Count<br/>- Resource Usage
```

## 7. VALIDATION PIPELINE

```mermaid
flowchart TD
    START([SLM Output]) --> STAGE1[Stage 1: Schema Validation]
  
    STAGE1 --> SCHEMA_CHECK{JSON Schema<br/>Valid?}
  
    SCHEMA_CHECK -->|No| S1_FAIL[Schema Error:<br/>- Missing fields<br/>- Wrong types<br/>- Invalid format]
    S1_FAIL --> ERROR_HANDLER
  
    SCHEMA_CHECK -->|Yes| STAGE2[Stage 2: Rule-Based Validation]
  
    STAGE2 --> RULES_CHECK{Business Rules<br/>Satisfied?}
  
    RULES_CHECK -->|No| S2_FAIL[Rule Violation:<br/>- Precondition failed<br/>- Permission denied<br/>- Resource unavailable]
    S2_FAIL --> ERROR_HANDLER
  
    RULES_CHECK -->|Yes| NEED_REASONING{Complex Logic<br/>Required?}
  
    NEED_REASONING -->|No| STAGE4
    NEED_REASONING -->|Yes| STAGE3[Stage 3: Reasoning Validation]
  
    STAGE3 --> LOAD_PHI[Load Phi-1.5<br/>Reasoning Model]
    LOAD_PHI --> REASONING_CHECK{Reasoning<br/>Valid?}
  
    REASONING_CHECK -->|No| S3_FAIL[Reasoning Error:<br/>- Logic inconsistency<br/>- Constraint violation<br/>- Invalid inference]
    S3_FAIL --> ERROR_HANDLER
  
    REASONING_CHECK -->|Yes| UNLOAD_PHI[Unload Phi-1.5]
    UNLOAD_PHI --> STAGE4[Stage 4: Output Validation]
  
    STAGE4 --> OUTPUT_CHECK{Output<br/>Consistent?}
  
    OUTPUT_CHECK -->|No| S4_FAIL[Output Error:<br/>- Hallucination detected<br/>- Inconsistent data<br/>- Missing verification]
    S4_FAIL --> RETRY_CHECK{Retry Count<br/>< 3?}
  
    RETRY_CHECK -->|Yes| RETRY[Regenerate with<br/>Feedback]
    RETRY --> START
  
    RETRY_CHECK -->|No| ERROR_HANDLER
  
    OUTPUT_CHECK -->|Yes| LOG_SUCCESS[Log Validation<br/>Success]
  
    LOG_SUCCESS --> METRICS[Update Metrics:<br/>- Precision: 99.2%<br/>- Recall: 95%<br/>- Latency: <100ms]
  
    METRICS --> SUCCESS([Validated Output])
  
    ERROR_HANDLER[Error Handler] --> LOG_ERROR[Log Error Details]
    LOG_ERROR --> ESCALATE{Escalation<br/>Required?}
  
    ESCALATE -->|Yes| HUMAN[Human Review]
    ESCALATE -->|No| ERROR_RESPONSE[Return Error<br/>to User]
  
    HUMAN --> ERROR_RESPONSE
    ERROR_RESPONSE --> END([End with Error])
  
    style START fill:#e1f5ff
    style SUCCESS fill:#c8e6c9
    style END fill:#ffcdd2
    style SCHEMA_CHECK fill:#fff9c4
    style RULES_CHECK fill:#fff9c4
    style REASONING_CHECK fill:#fff9c4
    style OUTPUT_CHECK fill:#fff9c4
```

## 8. MONITORING SYSTEM ARCHITECTURE

```mermaid
graph TB
    subgraph "Data Collection"
        MC[Metrics Collector]
        ET[Event Tracker]
        RM[Resource Monitor]
        FA[Flow Analyzer]
    end
  
    subgraph "Metrics Sources"
        ORCH_M[Orchestrator Metrics:<br/>- Requests/sec<br/>- Classification accuracy<br/>- Routing latency]
    
        DOMAIN_M[Domain Metrics:<br/>- Active domains<br/>- Model status<br/>- Processing latency]
    
        MODEL_M[Model Metrics:<br/>- Inference time<br/>- Token count<br/>- Memory usage]
    
        RAG_M[RAG Metrics:<br/>- Retrieval time<br/>- Relevance score<br/>- Cache hit rate]
    
        RESOURCE_M[Resource Metrics:<br/>- CPU usage %<br/>- Memory usage GB<br/>- GPU usage %]
    
        VALIDATION_M[Validation Metrics:<br/>- Precision<br/>- Recall<br/>- Error rate]
    end
  
    subgraph "Event Sources"
        QUERY_E[Query Events:<br/>- Received<br/>- Classified<br/>- Routed]
    
        DOMAIN_E[Domain Events:<br/>- Activated<br/>- Processing<br/>- Deactivated]
    
        MODEL_E[Model Events:<br/>- Loaded<br/>- Inference<br/>- Unloaded]
    
        COMM_E[Communication Events:<br/>- Message sent<br/>- Message received<br/>- Tool called]
    
        ERROR_E[Error Events:<br/>- Validation failed<br/>- Timeout<br/>- Exception]
    end
  
    subgraph "Data Processing"
        AGG[Aggregator:<br/>- Rolling averages<br/>- Percentiles<br/>- Counters]
    
        ALERT[Alert Engine:<br/>- Threshold checks<br/>- Anomaly detection<br/>- Notifications]
    
        FLOW_PROC[Flow Processor:<br/>- Build graph<br/>- Track paths<br/>- Identify bottlenecks]
    end
  
    subgraph "Storage"
        TS[Time Series DB:<br/>Metrics History]
    
        EVENT_LOG[Event Log:<br/>Structured Logging]
    
        FLOW_STORE[Flow Storage:<br/>Graph Data]
    end
  
    subgraph "Real-time Distribution"
        WS[WebSocket Server:<br/>Port 8000]
    
        SSE[Server-Sent Events:<br/>Alternative Stream]
    
        PROM[Prometheus Exporter:<br/>Port 9090]
    end
  
    subgraph "Web UI"
        DASH[Dashboard Overview]
        DOMAIN_UI[Domain View]
        MODEL_UI[Model Details]
        FLOW_UI[Flow Visualization]
        RESOURCE_UI[Resource Charts]
        LOG_UI[Log Viewer]
    end
  
    ORCH_M --> MC
    DOMAIN_M --> MC
    MODEL_M --> MC
    RAG_M --> MC
    RESOURCE_M --> RM
    VALIDATION_M --> MC
  
    QUERY_E --> ET
    DOMAIN_E --> ET
    MODEL_E --> ET
    COMM_E --> ET
    ERROR_E --> ET
  
    MC --> AGG
    ET --> AGG
    RM --> AGG
    FA --> FLOW_PROC
  
    AGG --> ALERT
    AGG --> TS
    ET --> EVENT_LOG
    FLOW_PROC --> FLOW_STORE
  
    TS --> WS
    EVENT_LOG --> WS
    FLOW_STORE --> WS
  
    AGG --> PROM
  
    WS --> DASH
    WS --> DOMAIN_UI
    WS --> MODEL_UI
    WS --> FLOW_UI
    WS --> RESOURCE_UI
    WS --> LOG_UI
  
    ALERT -.->|Email/Slack| NOTIFY[Notifications]
  
    style WS fill:#e1f5ff
    style DASH fill:#c8e6c9
```

## 9. COMPLETE REQUEST LIFECYCLE

```mermaid
sequenceDiagram
    autonumber
  
    participant User
    participant API as REST API
    participant Orch as Orchestrator
    participant Router as Intent Router
    participant MM as Model Manager
    participant Domain as Finance Domain
    participant RAG as RAG System
    participant Validator as Validation Layer
    participant Tool as External Tool
    participant Bus as Message Bus
    participant Monitor as Monitoring
  
    User->>API: POST /process {"query": "Transfer $5000"}
    activate API
  
    API->>Monitor: Log Request(timestamp, query)
    API->>Orch: process_request(query, context)
    activate Orch
  
    Orch->>Router: classify_intent(query)
    activate Router
  
    Router->>Router: TinyBERT Inference(67M params)
    Router-->>Orch: (domain="finance", confidence=0.93)
    deactivate Router
  
    Orch->>Monitor: Log Classification(finance, 0.93)
  
    alt Confidence < 0.85
        Orch-->>API: Escalate to Human
        API-->>User: Requires Human Review
    else Confidence >= 0.85
        Orch->>MM: activate_domain_slm("finance")
        activate MM
    
        MM->>MM: Check if model loaded
    
        alt Model Not Loaded
            MM->>MM: Load from cache/download
            MM->>MM: Apply quantization (8-bit)
            MM->>MM: Place on GPU/CPU
        end
    
        MM-->>Orch: Model Ready
        deactivate MM
    
        Orch->>Domain: Initialize Processing
        activate Domain
    
        Domain->>Bus: Subscribe to channels
        Domain->>RAG: retrieve_context(query)
        activate RAG
    
        RAG->>RAG: Embed query
        RAG->>RAG: Similarity search
        RAG-->>Domain: Relevant documents
        deactivate RAG
    
        Domain->>Domain: Build prompt with context
        Domain->>Domain: SLM Inference (8B params)
        Domain->>Domain: Generate action plan
    
        Domain->>Validator: validate_pre_execution(plan)
        activate Validator
    
        Validator->>Validator: Schema validation
        Validator->>Validator: Rule-based checks
    
        alt Complex Logic Required
            Validator->>Validator: Load Phi-1.5 (1.3B)
            Validator->>Validator: Reasoning validation
            Validator->>Validator: Unload Phi-1.5
        end
    
        Validator-->>Domain: Validation Passed
        deactivate Validator
    
        Domain->>Bus: Publish TOOL_CALL event
        Bus->>Tool: Execute transfer($5000, A→B)
        activate Tool
        Tool-->>Bus: Tool Result(success=true, txn_id=12345)
        Bus-->>Domain: Tool Response
        deactivate Tool
    
        Domain->>Validator: validate_post_execution(result)
        activate Validator
        Validator->>Validator: Verify transaction exists
        Validator->>Validator: Check consistency
        Validator-->>Domain: Output Valid
        deactivate Validator
    
        Domain->>Domain: Format final response
        Domain->>Bus: Publish RESPONSE event
        Domain-->>Orch: Response(status=success, data={...})
        deactivate Domain
    
        Orch->>MM: unload_domain_slm("finance")
        activate MM
        MM->>MM: Cleanup GPU memory
        MM->>MM: Cache state
        MM-->>Orch: Unloaded
        deactivate MM
    
        Orch->>Monitor: Log Execution(latency=320ms, tokens=150)
        Orch-->>API: Final Response
    end
  
    API-->>User: {"status": "success", "message": "Transfer complete"}
    deactivate API
    deactivate Orch
  
    Monitor->>Monitor: Update Metrics Dashboard
    Monitor->>Monitor: Update Flow Graph
    Monitor->>Monitor: Alert if anomaly detected
```

## 10. CLASS DIAGRAM - CORE COMPONENTS

```mermaid
classDiagram
    class MDSA {
        +Config config
        +Orchestrator orchestrator
        +DomainRegistry domains
        +ModelManager models
        +RAGEngine rag
        +MessageBus bus
        +MonitoringSystem monitoring
        +__init__(config_path)
        +process(query, context)
        +process_async(query, context)
        +register_domain(domain)
        +load_domain_from_yaml(path)
        +list_domains()
        +start_monitoring(port)
    }
  
    class Orchestrator {
        +TinyBERTModel model
        +IntentRouter router
        +StateMachine state_machine
        +MessageBus bus
        +string active_domain
        +process_request(query, context)
        +classify_intent(query)
        +activate_domain(domain_name)
        +deactivate_domain()
    }
  
    class IntentRouter {
        +Model tinybert
        +Tokenizer tokenizer
        +float confidence_threshold
        +classify(query)
        +get_confidence(query, domain)
    }
  
    class StateMachine {
        +State current_state
        +List~State~ valid_transitions
        +transition(new_state)
        +execute_workflow(steps)
        +rollback()
    }
  
    class DomainRegistry {
        +Dict~string,Domain~ domains
        +register(domain)
        +unregister(domain_name)
        +get(domain_name)
        +get_all()
        +discover_domains(path)
    }
  
    class Domain {
        <<abstract>>
        +string name
        +List~Model~ models
        +LocalRAG rag
        +List~Tool~ tools
        +List~Validator~ validators
        +initialize_slm()*
        +process(query, context)*
        +add_tool(tool)
        +add_validator(validator)
    }
  
    class DomainBuilder {
        <<static>>
        +from_yaml(path)$
        +from_dict(config)$
        +quick_start(name, source, model)$
        +interactive_builder()$
    }
  
    class ModelManager {
        +Dict~string,Model~ loaded_models
        +Dict~string,Loader~ loaders
        +Cache cache
        +load_model(name, source, path, kwargs)
        +unload_model(name)
        +get_model(name)
        +list_loaded_models()
    }
  
    class ModelLoader {
        <<interface>>
        +load(path, kwargs)*
        +validate()*
        +get_metadata()*
    }
  
    class HuggingFaceLoader {
        +load(path, kwargs)
        +validate()
        +get_metadata()
    }
  
    class OllamaLoader {
        +string api_url
        +load(path, kwargs)
        +validate()
        +get_metadata()
    }
  
    class LocalRAG {
        +string domain_name
        +EmbeddingModel embedder
        +VectorStore store
        +add_documents(docs)
        +add_from_directory(path)
        +retrieve(query, n_results)
    }
  
    class GlobalRAG {
        +EmbeddingModel embedder
        +VectorStore store
        +add_domain_knowledge(domain, docs)
        +retrieve_cross_domain(query, filter)
    }
  
    class MessageBus {
        +Dict~string,List~Callback~~ subscribers
        +List~Message~ history
        +subscribe(channel, callback)
        +publish(channel, message)
        +get_conversation_history(id)
    }
  
    class ValidationLayer {
        +RuleValidator rules
        +ReasoningValidator reasoning
        +SchemaValidator schema
        +validate_all(request, output, decision)
        +validate_schema(output)
        +validate_rules(request, decision)
        +validate_reasoning(query, response)
    }
  
    class MonitoringSystem {
        +MetricsCollector metrics
        +EventTracker events
        +ResourceMonitor resources
        +FlowAnalyzer flows
        +WebSocketServer ws_server
        +collect_metrics()
        +track_event(event)
        +get_dashboard_data()
        +start_server(port)
    }
  
    MDSA --> Orchestrator
    MDSA --> DomainRegistry
    MDSA --> ModelManager
    MDSA --> GlobalRAG
    MDSA --> MessageBus
    MDSA --> MonitoringSystem
  
    Orchestrator --> IntentRouter
    Orchestrator --> StateMachine
    Orchestrator --> MessageBus
  
    DomainRegistry --> Domain
    DomainBuilder ..> Domain : creates
  
    Domain --> LocalRAG
    Domain --> ModelManager : uses
  
    ModelManager --> ModelLoader
    ModelLoader <|-- HuggingFaceLoader
    ModelLoader <|-- OllamaLoader
  
    GlobalRAG --> LocalRAG : aggregates
  
    StateMachine --> ValidationLayer
  
    MonitoringSystem --> MessageBus : observes
```

## 11. DEPLOYMENT ARCHITECTURE

```mermaid
graph TB
    subgraph "Client Layer"
        WEB[Web Browser<br/>localhost:8000/monitor]
        CLI[CLI Tool<br/>mdsa-cli]
        API_CLIENT[API Client<br/>Python/REST]
    end
  
    subgraph "Application Layer - Docker Container"
        subgraph "MDSA Framework"
            API[FastAPI Server<br/>Port 8000]
            WS[WebSocket Server<br/>Real-time Updates]
            ORCH[Orchestrator Engine]
            REGISTRY[Domain Registry]
        end
    
        subgraph "Model Service"
            MM[Model Manager]
            CACHE[Model Cache<br/>Volume Mount]
        end
    
        subgraph "RAG Service"
            RAG_ENGINE[RAG Engine]
            VECTOR_DB[Vector Database<br/>ChromaDB]
        end
    
        subgraph "Monitoring Service"
            METRICS[Metrics Collector]
            PROM[Prometheus Exporter<br/>Port 9090]
            LOGS[Structured Logging]
        end
    end
  
    subgraph "Storage Layer"
        MODEL_STORAGE[Model Storage<br/>~/.mdsa/models/]
        VECTOR_STORAGE[Vector Store<br/>~/.mdsa/rag/]
        CONFIG_STORAGE[Configurations<br/>~/.mdsa/config/]
        LOG_STORAGE[Logs<br/>~/.mdsa/logs/]
    end
  
    subgraph "External Services"
        HF_HUB[HuggingFace Hub]
        OLLAMA_SERVER[Ollama Server<br/>Port 11434]
        OPENAI_API[OpenAI API]
        EXTERNAL_TOOLS[External Tools<br/>Databases, APIs]
    end
  
    subgraph "Monitoring Stack"
        PROMETHEUS[Prometheus<br/>Metrics Storage]
        GRAFANA[Grafana<br/>Visualization]
        ALERTMANAGER[AlertManager<br/>Notifications]
    end
  
    WEB --> API
    CLI --> API
    API_CLIENT --> API
  
    API --> ORCH
    WS --> WEB
  
    ORCH --> REGISTRY
    ORCH --> MM
    ORCH --> RAG_ENGINE
  
    MM --> CACHE
    RAG_ENGINE --> VECTOR_DB
  
    CACHE --> MODEL_STORAGE
    VECTOR_DB --> VECTOR_STORAGE
    REGISTRY --> CONFIG_STORAGE
    LOGS --> LOG_STORAGE
  
    MM -.->|Download| HF_HUB
    MM -.->|Connect| OLLAMA_SERVER
    MM -.->|API Call| OPENAI_API
  
    ORCH -.->|Tool Calls| EXTERNAL_TOOLS
  
    METRICS --> PROM
    PROM --> PROMETHEUS
    PROMETHEUS --> GRAFANA
    PROMETHEUS --> ALERTMANAGER
  
    style API fill:#e1f5ff
    style ORCH fill:#fff9c4
    style MM fill:#bbdefb
    style RAG_ENGINE fill:#c8e6c9
    style METRICS fill:#f5f5f5
```

## 12. DATA FLOW - END-TO-END

```mermaid
flowchart TB
    START([User Query: Transfer $5000]) --> INPUT_VAL[Input Validation<br/>Check query format]
  
    INPUT_VAL --> ORCH_RECEIVE[Orchestrator<br/>Receive Request]
  
    ORCH_RECEIVE --> INTENT_CLASS[Intent Classification<br/>TinyBERT: 67M params<br/>Latency: 45ms]
  
    INTENT_CLASS --> CONFIDENCE{Confidence<br/>>= 0.85?}
  
    CONFIDENCE -->|No: 0.72| ESCALATE[Escalate to Human<br/>Low Confidence]
    ESCALATE --> END1([End: Human Review])
  
    CONFIDENCE -->|Yes: 0.93| DOMAIN_SELECT[Select Domain:<br/>Finance]
  
    DOMAIN_SELECT --> MODEL_CHECK{Finance Models<br/>Loaded?}
  
    MODEL_CHECK -->|No| LOAD_MODELS[Load Models:<br/>- SLM-Transactions 8B<br/>- SLM-Risk 13B<br/>Latency: 2000ms]
  
    MODEL_CHECK -->|Yes| RAG_CHECK
    LOAD_MODELS --> RAG_CHECK{RAG<br/>Enabled?}
  
    RAG_CHECK -->|Yes| RAG_RETRIEVE[Retrieve Context:<br/>1. Embed query<br/>2. Similarity search<br/>3. Get top 5 docs<br/>Latency: 50ms]
  
    RAG_CHECK -->|No| BUILD_PROMPT
    RAG_RETRIEVE --> BUILD_PROMPT[Build Prompt<br/>with Context]
  
    BUILD_PROMPT --> SLM_INFERENCE[SLM Inference:<br/>SLM-Transactions<br/>Latency: 150ms]
  
    SLM_INFERENCE --> ACTION_PLAN[Generate Action Plan:<br/>1. Validate amount<br/>2. Check balance<br/>3. Execute transfer]
  
    ACTION_PLAN --> VAL_STAGE1[Validation Stage 1:<br/>Schema Check<br/>Latency: 5ms]
  
    VAL_STAGE1 --> SCHEMA_OK{Schema<br/>Valid?}
  
    SCHEMA_OK -->|No| VAL_FAIL[Validation Failed]
    VAL_FAIL --> ERROR_HANDLE[Error Handler]
    ERROR_HANDLE --> END2([End: Error Response])
  
    SCHEMA_OK -->|Yes| VAL_STAGE2[Validation Stage 2:<br/>Business Rules<br/>Latency: 10ms]
  
    VAL_STAGE2 --> RULES_OK{Rules<br/>Pass?}
  
    RULES_OK -->|No| VAL_FAIL
  
    RULES_OK -->|Yes| COMPLEX{Complex<br/>Logic?}
  
    COMPLEX -->|Yes| VAL_STAGE3[Validation Stage 3:<br/>Phi-1.5 Reasoning<br/>Latency: 80ms]
  
    VAL_STAGE3 --> REASONING_OK{Reasoning<br/>Valid?}
    REASONING_OK -->|No| VAL_FAIL
    REASONING_OK -->|Yes| EXECUTE_TOOL
  
    COMPLEX -->|No| EXECUTE_TOOL[Execute Tool:<br/>Bank API Transfer<br/>Latency: 100ms]
  
    EXECUTE_TOOL --> TOOL_RESULT{Tool<br/>Success?}
  
    TOOL_RESULT -->|No| TOOL_ERROR[Tool Error]
    TOOL_ERROR --> RETRY{Retry<br/>< 3?}
    RETRY -->|Yes| EXECUTE_TOOL
    RETRY -->|No| ERROR_HANDLE
  
    TOOL_RESULT -->|Yes| OUTPUT_VAL[Output Validation:<br/>Verify transaction<br/>Latency: 15ms]
  
    OUTPUT_VAL --> OUTPUT_OK{Output<br/>Consistent?}
  
    OUTPUT_OK -->|No| VAL_FAIL
  
    OUTPUT_OK -->|Yes| FORMAT_RESP[Format Response:<br/>Status, TXN ID, Balance]
  
    FORMAT_RESP --> LOG_EXEC[Log Execution:<br/>- Total latency: 320ms<br/>- Tokens used: 150<br/>- Memory: 8GB peak]
  
    LOG_EXEC --> UPDATE_METRICS[Update Metrics:<br/>- Request count +1<br/>- Avg latency: 325ms<br/>- Success rate: 98.5%]
  
    UPDATE_METRICS --> UNLOAD_CHECK{Other<br/>Requests?}
  
    UNLOAD_CHECK -->|No| UNLOAD_MODELS[Unload Finance Models<br/>Free 8GB memory]
    UNLOAD_CHECK -->|Yes| KEEP_LOADED
  
    UNLOAD_MODELS --> SEND_RESPONSE
    KEEP_LOADED[Keep Models Loaded] --> SEND_RESPONSE[Send Response to User]
  
    SEND_RESPONSE --> MONITOR_UPDATE[Update Monitor UI:<br/>- Real-time graph<br/>- Metrics dashboard<br/>- Activity log]
  
    MONITOR_UPDATE --> END3([End: Success])
  
    style START fill:#e1f5ff
    style END3 fill:#c8e6c9
    style END1 fill:#fff9c4
    style END2 fill:#ffcdd2
    style CONFIDENCE fill:#fff9c4
    style SCHEMA_OK fill:#fff9c4
    style RULES_OK fill:#fff9c4
    style REASONING_OK fill:#fff9c4
    style OUTPUT_OK fill:#fff9c4
```

---

## 📊 PERFORMANCE & SCALING METRICS

```mermaid
graph LR
    subgraph "Performance Targets"
        P1[Orchestrator: <50ms]
        P2[Intent Classification: 95%+]
        P3[Domain Processing: <500ms]
        P4[Validation: <100ms]
        P5[RAG Retrieval: <50ms]
        P6[Total Latency: <700ms p99]
    end
  
    subgraph "Resource Utilization"
        R1[Idle Memory: <500MB]
        R2[Active Domain: 8-15GB]
        R3[Peak Concurrent: 3 Domains]
        R4[CPU: 4-8 cores]
        R5[GPU: Optional but recommended]
    end
  
    subgraph "Scaling Characteristics"
        S1[Horizontal: Domain Sharding]
        S2[Vertical: GPU Upgrade]
        S3[Cache: 90% Hit Rate]
        S4[Throughput: 450 req/sec]
        S5[Concurrent Users: 1000+]
    end
  
    style P1 fill:#c8e6c9
    style P2 fill:#c8e6c9
    style P3 fill:#c8e6c9
    style P4 fill:#c8e6c9
    style P5 fill:#c8e6c9
    style P6 fill:#c8e6c9
```

---

This comprehensive architecture documentation provides:

1. ✅ **High-level system overview** showing all major components
2. ✅ **Detailed orchestration flow** with state management
3. ✅ **Domain creation workflow** for beginner-friendly setup
4. ✅ **Model loading architecture** supporting multiple sources
5. ✅ **RAG system design** with local and global capabilities
6. ✅ **Communication patterns** for inter-component messaging
7. ✅ **Validation pipeline** with three-stage verification
8. ✅ **Monitoring architecture** for real-time observability
9. ✅ **Complete request lifecycle** sequence diagram
10. ✅ **Class diagram** showing object relationships
11. ✅ **Deployment architecture** for production
12. ✅ **End-to-end data flow** with latency metrics

All diagrams are in Mermaid format, logically organized, and production-ready for implementation!
