#!/bin/bash
# Autonomous LLM Archive Workflow Trigger

echo "🚀 Booting Local LLM Workflow Agent..."

# Check if Ollama is responding
if curl -s http://localhost:11434/api/tags > /dev/null; then
    echo "✅ Ollama API is active."
    echo "🧠 Initiating semantic categorization..."
    python3 auto_organize.py
else
    echo "❌ Error: Local Ollama service is not running. Please start Ollama first."
    exit 1
fi