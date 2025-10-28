import ast
import re

def parse_str_to_dict(example):
    """Parse all string representations to their proper types"""

    # Parse available_options (list of dicts)
    if isinstance(example['available_options'], str):
        fixed_string = example['available_options'].replace('}\n {', '}, {')
        try:
            example['available_options'] = ast.literal_eval(fixed_string)
        except (ValueError, SyntaxError) as e:
            fixed_string = re.sub(r'}\s+{', '}, {', example['available_options'])
            try:
                example['available_options'] = ast.literal_eval(fixed_string)
            except:
                print(f"Error parsing available_options: {e}")
                example['available_options'] = []

    # Parse selected_option (single dict)
    if isinstance(example['selected_option'], str):
        try:
            example['selected_option'] = ast.literal_eval(example['selected_option'])
        except (ValueError, SyntaxError) as e:
            print(f"Error parsing selected_option: {e}")
            # Try to fix common issues
            fixed_string = example['selected_option'].strip()
            try:
                example['selected_option'] = ast.literal_eval(fixed_string)
            except:
                example['selected_option'] = None
    return example