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

alpaca_prompt_style="""###Instruction:
You are a privacy policy evaluator. Your task is to analyze privacy policies and classify them according to a detailed rubric item.
    **Rubric:**
        - **Slug:** {}
        - **Category:** {}
        - **Question:** {}
        - **Points:** {}
    **Available Options:**
        {}
    **Task:**
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
Be precise and evidence-based in your classification.
### Input:
{}
### Response:
{}"""

def format_alpaca_prompt_style(examples, tokenizer):
    q_slugs = examples["question_slug"]
    q_cats = examples["question_category"]
    q_texts = examples["question_text"]
    q_points = examples["question_points"]
    p_texts = examples["policy_text"]
    a_options = examples["available_options"]
    s_options = examples["selected_option"]
    citations = examples["citation"]

    EOS_TOKEN = tokenizer.eos_token
    texts = []

    for slug, cat, q_text, q_point, p_text, a_option, s_option, citation in zip(
            q_slugs, q_cats, q_texts, q_points, p_texts, a_options, s_options, citations
    ):
        # Parse the s_option if it's a string representation of a dict
        import json
        if isinstance(s_option, str):
            try:
                s_option_dict = json.loads(s_option)
            except:
                # If it fails to parse, create a new dict
                s_option_dict = {"option_key": s_option}
        elif isinstance(s_option, dict):
            s_option_dict = s_option.copy()  # Make a copy to avoid modifying original
        else:
            s_option_dict = {"option_key": str(s_option)}
        s_option_dict["citation"] = citation
        s_option_with_citation = json.dumps(s_option_dict, ensure_ascii=False)

        # Must add EOS_TOKEN, otherwise your generation will go on forever! BOS token will be added automatically
        text = (alpaca_prompt_style
                .format(slug, cat, q_text, q_point, a_option, p_text, s_option_with_citation)
                + EOS_TOKEN
                )
        texts.append(text)

    return {"text": texts}
