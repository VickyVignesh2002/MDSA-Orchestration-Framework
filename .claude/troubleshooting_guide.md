# MDSA Framework - Troubleshooting Guide

## Common Issues and Solutions

### Installation Issues

**Issue: pip install fails**

```bash
# Solution: Upgrade pip and setuptools
pip install --upgrade pip setuptools wheel
pip install -e .
```

**Issue: torch not found**

```bash
# Solution: Install PyTorch separately
pip install torch --index-url https://download.pytorch.org/whl/cpu
```

### Model Loading Issues

**Issue: HuggingFace model won't download**

- Check internet connection
- Verify model ID is correct
- Set HF_TOKEN environment variable if needed

**Issue: Out of memory when loading model**

- Use quantization: `quantization="8bit"`
- Reduce batch size
- Close other applications

### RAG Issues

**Issue: Documents not retrieved**

- Check if documents were indexed
- Verify embedding model loaded
- Check query similarity threshold

### Monitoring Issues

**Issue: Cannot access localhost:8000/monitor**

- Check if port 8000 is available
- Verify monitoring server started
- Check firewall settings

**Issue: WebSocket not connecting**

- Verify WebSocket support in browser
- Check network/proxy settings
- Try different port

### Performance Issues

**Issue: Slow inference**

- Use GPU if available
- Apply quantization
- Reduce context length
- Check if multiple models loaded

**Issue: High memory usage**

- Unload unused models
- Reduce number of active domains
- Clear model cache

## Debug Mode

Enable debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Getting Help

1. Check documentation in docs/
2. Run examples to verify setup
3. Check GitHub issues
4. Enable debug logging for details
