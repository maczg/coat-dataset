from typing import Any, Dict, Optional
from sqlmodel import SQLModel
from langchain_core.prompt_values import PromptValue
from langchain_core.prompts import ChatPromptTemplate

class RubricResponse(SQLModel):
    description: Optional[str] = None
    option_key: Optional[str] = None
    percent: Optional[float] = None
    text: Optional[str] = None
    citation: Optional[str] = None

def build_system_prompt(sample: Dict[str, Any]) -> str:
    options_text = "\n".join([
        f"  - **{opt['option_key']}** ({opt['percent']}%): {opt['text']}" +
        (f"\n    Description: {opt['description']}" if opt['description'] else "")
        for opt in sample['available_options']
    ])

    return f"""
    You are a privacy policy evaluator. Your task is to analyze privacy policies and classify them according to a detailed rubric.
    **Rubric Item:**
        - **Slug:** {sample['question_slug']}
        - **Category:** {sample['question_category']}
        - **Question:** {sample['question_text']}
        - **Points:** {sample['question_points']}
    **Available Options:**
        {options_text}
        """ + """
    **Instructions:**
    1. Read the privacy policy carefully
    2. Select the most appropriate option based on the policy content
    3. Provide a direct citation from the policy that supports your selection
    4. Format your response as JSON with: option_key (matching one of the available option keys), option_text, and citation
    4. *JSON Output Only**: Format your analysis as a JSON object strictly following the structure below,with no additional commentary or text.
    Example JSON Response:
    {{
        "description": "",
        "option_key": "no",
        "percent": 100,
        "text": "No",
        "citation": "..."
    }}

Be precise and evidence-based in your classification."""


def build_prompt_value(sample) -> PromptValue:
    system_prompt = build_system_prompt(sample)

    user_template = """Here is the privacy policy to evaluate:
        {privacy_policy}
        Please provide your classification in JSON format."""

    prompt_template = ChatPromptTemplate(
        messages=[
            ("system", system_prompt),
            ("user", user_template)
        ],
        input_variables=["privacy_policy"]
    )
    return prompt_template.invoke({"privacy_policy": sample["policy_text"]})