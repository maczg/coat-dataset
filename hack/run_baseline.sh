#!/bin/bash

# Load environment variables
export PYTHONPATH=.
source .env

# List of rubric items
rubric_items=(
    "behavioral-marketing"
    "data-breaches"
    "data-collection-reasoning"
    "data-deletion"
    "history"
    "law-enforcement"
    "list-collected"
    "noncritical-purposes"
    "revision-notify"
    "security"
    "third-party-access"
    "third-party-collection"
)

# Run the script for each rubric item
for rubric in "${rubric_items[@]}"; do
    echo "Running baseline_ollama.py with rubric: $rubric on $OLLAMA_HOST"
    echo "----------------------------------------"
    python scripts/baseline_ollama.py -r "$rubric"
    echo ""
done