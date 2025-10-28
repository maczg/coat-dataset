import csv
import logging
import os
from datetime import datetime
from tqdm import tqdm

from datasets import load_dataset
from utils.args import parse_args
from utils.dataset import parse_str_to_dict
from utils.prompt import RubricResponse, build_prompt_value
from langchain_ollama import ChatOllama

if __name__ == "__main__":

    args = parse_args()
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    csv_filename = f"logs/{args.rubric_item}/{args.model}/temp{args.temp}_topk{args.top_k}_minp{args.min_p}_{timestamp}.csv"
    log_filename = f"logs/{args.rubric_item}/{args.model}/temp{args.temp}_topk{args.top_k}_minp{args.min_p}_{timestamp}.log"
    log_dir = "logs/{}/{}".format(args.rubric_item, args.model)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    logging.basicConfig(filename=log_filename, level=logging.INFO)

    logging.info("starting evaluation")

    results = {
        'model': args.model,
        'rubric_item': args.rubric_item,
        'temperature': args.temp,
        'top_k': args.top_k,
        'min_p': args.min_p,
    }

    try:
        train = load_dataset("maczg/coat-dataset", args.rubric_item, split="train")
        test = load_dataset("maczg/coat-dataset", args.rubric_item, split="test")
        train = train.map(parse_str_to_dict)
        test = test.map(parse_str_to_dict)
    except Exception as e:
        logging.error(f"error loading dataset: {e}")
        exit(1)

    ollama_host = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
    logging.info(f"host: {ollama_host}")

    try:
        ollama_kwargs = {
            'model': args.model,
            'base_url': ollama_host,
            'temperature': args.temp,
            'top_k': args.top_k,
            'min_p': args.min_p,
        }

        ollama = ChatOllama(**ollama_kwargs)
        ollama = ollama.with_structured_output(
            RubricResponse,
            include_raw=True,
        )
    except Exception as e:
        logging.error(f"error initializing Ollama model: {e}")
        exit(1)

    with open(csv_filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(
            [
                'model', 'temperature', 'top_k', 'min_p',
                'policy', 'question_text', 'policy_text',
                'label', 'label_citation', 'prediction', 'citation',
                'label_match', 'citation_match'
             ]
        )

        for idx, sample in tqdm(enumerate(test), desc="Evaluating samples"):
            policy_name = sample.get('policy_name')
            slug = sample.get('question_slug')
            category = sample.get('question_category')
            question_text = sample.get('question_text')
            available_options = sample.get('available_options')
            label = sample.get('selected_option', {}).get('option_key')
            label_citation = sample.get('citation', "")
            policy_text = sample.get('policy_text')
            logging.debug(f"policy {policy_name}, question {slug}, label {label}")

            partial_result = {
                'policy': policy_name,
                'question': slug,
                'question_category': category,
                'question_text': question_text
            }
            try:
                prompt = build_prompt_value(sample)
                result = ollama.invoke(prompt)
                response = RubricResponse.model_validate(result.get('parsed', None))

                prediction = response.option_key
                citation = response.citation
                is_correct = prediction == label
                csvwriter.writerow(
                    [
                        args.model, args.temp,args.top_k, args.min_p,
                        policy_name, question_text, policy_text, label,
                        label_citation, prediction, citation, is_correct,
                        citation == label_citation
                    ])
                logging.info(f"policy: {policy_name}, question: {slug}, label: {label}, prediction: {prediction}, correct: {is_correct}")
            except Exception as e:
                print(f"Error during query for policy '{policy_name}' and question '{slug}': {e}")
                logging.error(f"Error during query for policy '{policy_name}' and question '{slug}': {e}")
                continue