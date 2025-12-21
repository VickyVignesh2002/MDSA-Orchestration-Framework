
# MDSA Framework - Deployment Guide

## Docker Deployment

### Build Image

```bash
docker build -t mdsa-framework:latest .
```

### Run Container

```bash
docker run -d \
  --name mdsa \
  -p 8000:8000 \
  -v ~/.mdsa:/root/.mdsa \
  -v $(pwd)/configs:/app/configs \
  --gpus all \
  mdsa-framework:latest
```

## Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mdsa-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: mdsa
  template:
    metadata:
      labels:
        app: mdsa
    spec:
      containers:
      - name: mdsa
        image: mdsa-framework:latest
        ports:
        - containerPort: 8000
        resources:
          limits:
            nvidia.com/gpu: 1
            memory: 16Gi
          requests:
            memory: 4Gi
```

## Environment Variables

```bash
# Model cache location
mdsa_CACHE_DIR=~/.mdsa/models

# Configuration file
mdsa_CONFIG=/path/to/config.yaml

# API keys
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
HUGGINGFACE_TOKEN=hf_...

# Monitoring
mdsa_MONITORING_PORT=8000
mdsa_METRICS_PORT=9090

# Logging
mdsa_LOG_LEVEL=INFO
mdsa_LOG_FILE=/var/log/mdsa.log
```

## Production Checklist

- [ ] Set up reverse proxy (nginx)
- [ ] Enable HTTPS/TLS
- [ ] Configure logging
- [ ] Set up monitoring (Prometheus/Grafana)
- [ ] Configure backup for models and configs
- [ ] Set resource limits
- [ ] Enable auto-restart
- [ ] Configure health checks
- [ ] Set up alerting
- [ ] Document disaster recovery

```

---

## Summary

**Create these files in your project directory:**

1. `architecture.md` - ✅ Already provided
2. `plan.md` - ✅ Already provided  
3. `plan_1.md` - ✅ Already provided
4. `implementation_checklist.md` - ⬆️ Create from above
5. `troubleshooting_guide.md` - ⬆️ Create from above
6. `performance_benchmarks.md` - ⬆️ Create from above
7. `api_examples.md` - ⬆️ Create from above
8. `deployment_guide.md` - ⬆️ Create from above

**Then provide this prompt to Claude Code:**
```

I have the following documentation files in my project directory:

- architecture.md (system architecture with Mermaid diagrams)
- plan.md (detailed implementation plan)
- plan_1.md (additional specifications)
- implementation_checklist.md (phase-by-phase checklist)
- troubleshooting_guide.md (common issues and solutions)
- performance_benchmarks.md (target metrics)
- api_examples.md (usage examples)
- deployment_guide.md (production deployment)

Please read all these files carefully, then begin building the mdsa framework following the comprehensive development instructions provided. Start with Phase 1: Project Setup.
