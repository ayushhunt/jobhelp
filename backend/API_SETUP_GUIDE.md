# JobHelp AI - Multi-Provider Setup Guide

## 🚀 Quick Start for Cost Optimization

### Recommended Setup (Best Value)
```bash
# Get a Groq API key (fastest, cheapest)
export GROQ_API_KEY="gsk_your-groq-api-key-here"

# Optional: OpenAI as backup
export OPENAI_API_KEY="sk-your-openai-api-key-here"
```

## 💰 Cost Comparison (per 1M tokens)

| Provider | Model | Cost | Speed | Quality | Best For |
|----------|-------|------|-------|---------|----------|
| **Groq** | llama-3.1-8b | $0.05 | ⚡⚡⚡ | ⭐⭐⭐ | **Free tier** |
| **Groq** | mixtral-8x7b | $0.24 | ⚡⚡⚡ | ⭐⭐⭐⭐ | **Balanced** |
| **Groq** | llama-3.1-70b | $0.59 | ⚡⚡⚡ | ⭐⭐⭐⭐⭐ | **Premium** |
| OpenAI | gpt-4o-mini | $0.15 | ⚡⚡ | ⭐⭐⭐⭐ | Backup |
| OpenAI | gpt-4o | $5.00 | ⚡ | ⭐⭐⭐⭐⭐ | Enterprise |
| Anthropic | claude-haiku | $0.25 | ⚡⚡ | ⭐⭐⭐⭐ | Alternative |
| **Ollama** | llama3.1 | **FREE** | ⚡ | ⭐⭐⭐ | **Local** |

## 🔧 Provider Setup Instructions

### 1. Groq (Recommended - Cheapest & Fastest)
```bash
# 1. Get API key from https://console.groq.com/
# 2. Set environment variable
export GROQ_API_KEY="gsk_your-groq-api-key-here"

# Available models:
# - llama-3.1-8b-instant (ultra-cheap)
# - mixtral-8x7b-32768 (balanced)  
# - llama-3.1-70b-versatile (premium)
```

### 2. OpenAI (Backup)
```bash
# 1. Get API key from https://platform.openai.com/
# 2. Set environment variable
export OPENAI_API_KEY="sk-your-openai-api-key-here"

# Available models:
# - gpt-4o-mini (cost-effective)
# - gpt-4o (premium quality)
```

### 3. Anthropic (Alternative)
```bash
# 1. Get API key from https://console.anthropic.com/
# 2. Set environment variable
export ANTHROPIC_API_KEY="sk-ant-your-anthropic-api-key-here"

# Available models:
# - claude-3-haiku (fast)
# - claude-3-sonnet (premium)
```

### 4. Ollama (Free Local)
```bash
# 1. Install Ollama from https://ollama.ai/
# 2. Pull models
ollama pull llama3.1
ollama pull phi3

# 3. Start Ollama (usually auto-starts)
ollama serve

# 4. Set base URL (optional if using default)
export OLLAMA_BASE_URL="http://localhost:11434"
```

## 📊 Usage Strategy

### For Free Tier (3 requests/day)
```python
# Model preference order:
1. llama-3.1-8b (Groq) - $0.05/1M tokens
2. mixtral-8x7b (Groq) - $0.24/1M tokens  
3. gpt-4o-mini (OpenAI) - $0.15/1M tokens
4. phi3 (Ollama) - FREE
```

### For Premium Tier (Unlimited)
```python
# Model preference order:
1. llama-3.1-70b (Groq) - $0.59/1M tokens
2. claude-3-sonnet (Anthropic) - $3.00/1M tokens
3. gpt-4o (OpenAI) - $5.00/1M tokens
4. llama-3.1-8b (Groq) - Fallback
```

## 🎯 Cost Optimization Tips

### Extreme Budget (< $1/month)
```bash
# Use only Groq with smallest model
export GROQ_API_KEY="your-key"
# Model: llama-3.1-8b-instant
# Cost: ~1000 requests for $0.50
```

### Balanced Budget ($5-10/month)
```bash
# Use Groq + OpenAI backup
export GROQ_API_KEY="your-groq-key"
export OPENAI_API_KEY="your-openai-key"
# Primary: mixtral-8x7b, Backup: gpt-4o-mini
```

### Quality Focused ($20+/month)
```bash
# Use all providers
export GROQ_API_KEY="your-groq-key"
export ANTHROPIC_API_KEY="your-anthropic-key"
export OPENAI_API_KEY="your-openai-key"
# Primary: llama-3.1-70b, Premium: claude-sonnet
```

### Completely Free
```bash
# Use only Ollama (local)
ollama pull llama3.1
ollama pull phi3
ollama serve
# Zero API costs, but requires local setup
```

## 🔍 Monitoring & Testing

### Check Available Models
```bash
curl http://localhost:8000/ai-models
```

### View Cost Comparison
```bash
curl http://localhost:8000/ai-costs
```

### Test Analysis
```bash
curl -X POST "http://localhost:8000/analyze?use_ai=true" \
  -F "resume_text=Software Engineer with 3 years Python experience" \
  -F "job_description_text=Looking for Python developer with 2+ years"
```

## 🚨 Important Notes

1. **Groq is the sweet spot** - 10x cheaper than OpenAI with similar speed
2. **Start with one provider** - Add others as backups
3. **Ollama is free** but requires local GPU/CPU resources
4. **Monitor usage** via `/ai-usage` endpoint
5. **Automatic fallback** - System tries cheaper models first

## 🔄 Runtime Model Switching

The system automatically:
- Tries cheapest available model first
- Falls back to more expensive models if needed
- Tracks costs and usage per model
- Optimizes based on user tier (free/premium)

No code changes needed - just set the API keys! 🎉
