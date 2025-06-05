# COAT Privacy Policy Analysis Dataset

The COAT (Comprehensive Online Agreement Transparency) project employs LLMs to analyze, interpret, and 
evaluate privacy policies autonomously. In this early stage of development, COAT quantifies privacy risks through 
a structured scoring methodology and provides accessible citations of crucial policysegments to justify computed scores,
following the [PrivacySpy](https://github.com/politiwatch/privacyspy) methodology but leveraging LLM capabilities.

## Overview

This dataset contains privacy policy analysis results from multiple LLM models using the methodology proposed by
[PrivacySpy](https://github.com/politiwatch/privacyspy) to assess a comprehensive evaluation and scoring of privacy policies.
A big thanks to the PrivacySpy contributors for their work.

More details about the evaluation algorithm in PrivacySpy [About](https://privacyspy.org/about/) page and in the
paper [published soon]().

The input text for the models is the composition of PrivacySpy policy citations, using the same PrivacySpy rubric as 
the evaluation criteria. The dataset includes baseline PrivacySpy scores and LLM-generated assessments.

## Dataset Information
- Version: 1.0
- Date: 2025-06-05
- Total Policies: 269
- Models: baseline, o1, o3, o4-mini, qwen3:30b-a3b (ollama)

## File Structure
- `dataset.json`: Complete dataset in JSON format
- `dataset.csv`: Flattened dataset in CSV format
- `dataset_policies.parquet`: Policy information in Parquet format
- `dataset_scores.parquet`: Model scores and rubric details in Parquet format
- `schema.json`: Dataset schema definition

## Data Format

### 1. Policy Information
- Basic policy details (ID, name, slug, description)
- Sources and hostnames
- Last updated date

### 2. Model Scores
- Overall scores for each model
- Performance metrics (latency, experiment IDs)
- Token usage (prompt_tokens, response_tokens)
- Detailed rubric assessments including:
    - Individual rubric item scores
    - Selected options for each rubric item
    - Citations from the policy text
    - Score breakdowns by category

### 3. Statistics
- Model performance metrics
- Score distributions
- Query statistics
- Token usage statistics

## File Formats

### JSON Format
Complete nested structure with all details, including:
- Full policy information
- Complete rubric assessments
- All model scores and metrics
- Token usage information
- Detailed statistics

### CSV Format
Flattened structure with columns for:
- Basic policy information
- Overall model scores
- Token usage metrics (prompt_tokens, response_tokens)
- Individual rubric scores (format: {model}_rubric_{slug}_score)
- Rubric options and citations
- Performance metrics

### Parquet Format
Two separate files:
1. `dataset_policies.parquet`:
    - Basic policy information
    - Metadata fields

2. `dataset_scores.parquet`:
    - Policy ID and model information
    - Overall scores and metrics
    - Token usage information
    - Detailed rubric assessments:
        - Rubric slug
        - Individual scores
        - Selected options
        - Citations

## Usage Examples

### CSV Analysis
```python
import pandas as pd
df = pd.read_csv('dataset.csv')
# Get all rubric scores for a specific model
o1_rubric_scores = df.filter(regex='^o1_rubric_.*_score$')
# Analyze token usage
token_usage = df[['o1_prompt_tokens', 'o1_response_tokens']]
```

### Parquet Analysis
```python
import pandas as pd
# Load scores with rubric details
scores_df = pd.read_parquet('dataset_scores.parquet')
# Analyze specific rubric items
behavioral_marketing = scores_df[scores_df['rubric_slug'] == 'behavioral-marketing']
# Analyze token usage
token_stats = scores_df.groupby('model')[['prompt_tokens', 'response_tokens']].mean()
```

## Citation
If you use this dataset in your research, please cite: **WIP**


## Acknowledgments

This work is part of the COAT project, which is funded by the European Union's Horizon Europe research program, 
promoted by European Commission-funded cascade funding NGI Sargasso.

<img src="img/sargasso_logo.png" alt="sargasso" width="200" height="50"/>

<img src="img/eu_logo_1.jpg" alt="sargasso" width="200" height="50"/>
