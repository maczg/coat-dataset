import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--rubric-item','-r', type=str, default='behavioral-marketing',
                        help='The rubric item to evaluate (default: behavioral-marketing)')
    parser.add_argument('--model', type=str, default='qwen3:30b-a3b',
                        help='The model to use for evaluation (default: qwen3:30b-a3b)')
    parser.add_argument('--temp', '-t', type=float, default=0.1,
                        help='Temperature setting for the model (default: 0.1)')
    parser.add_argument('--top_k', '-k', type=int, default=20,
                        help='Top-k setting for the model (default: 20)')
    parser.add_argument('--min-p', '-p', type=float, default=0.0,
                        help='Minimum probability setting for the model (default: 0.0)')
    return parser.parse_args()