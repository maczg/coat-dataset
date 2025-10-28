#!/usr/bin/env python3
import csv
import sys
import glob
import os
from collections import defaultdict


def calculate_accuracy(csv_file):
    """Calculate accuracy from a CSV result file."""
    total = 0
    correct = 0
    citation_correct = 0
    
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            total += 1
            if row['label_match'].lower() in ['true', '1']:
                correct += 1
            if row['citation_match'].lower() in ['true', '1']:
                citation_correct += 1
    
    if total == 0:
        return 0, 0, 0
    
    accuracy = (correct / total) * 100
    citation_accuracy = (citation_correct / total) * 100
    
    return accuracy, citation_accuracy, total


def display_results(csv_files):
    """Display accuracy results for multiple CSV files."""
    
    if not csv_files:
        print("No CSV files found.")
        return
    
    print("\n" + "="*80)
    print("EXPERIMENT RESULTS - ACCURACY REPORT")
    print("="*80)
    
    all_results = []
    
    for csv_file in csv_files:
        accuracy, citation_accuracy, total = calculate_accuracy(csv_file)
        
        # Extract metadata from filename
        filename = os.path.basename(csv_file)
        dirname = os.path.dirname(csv_file)
        parts = dirname.split('/')
        
        rubric_item = parts[-2] if len(parts) >= 2 else "unknown"
        model = parts[-1] if len(parts) >= 1 else "unknown"
        
        # Parse hyperparameters from filename
        params = filename.replace('.csv', '').split('_')
        temp = top_k = min_p = "unknown"
        
        for param in params:
            if param.startswith('temp'):
                temp = param.replace('temp', '')
            elif param.startswith('topk'):
                top_k = param.replace('topk', '')
            elif param.startswith('minp'):
                min_p = param.replace('minp', '')
        
        all_results.append({
            'file': csv_file,
            'rubric': rubric_item,
            'model': model,
            'temp': temp,
            'top_k': top_k,
            'min_p': min_p,
            'accuracy': accuracy,
            'citation_acc': citation_accuracy,
            'total': total
        })
    
    # Sort by accuracy
    all_results.sort(key=lambda x: x['accuracy'], reverse=True)
    
    # Display results
    for result in all_results:
        print(f"\nFile: {result['file']}")
        print(f"Rubric Item: {result['rubric']}")
        print(f"Model: {result['model']}")
        print(f"Temperature: {result['temp']}, Top-K: {result['top_k']}, Min-P: {result['min_p']}")
        print(f"Samples: {result['total']}")
        print(f"Label Accuracy: {result['accuracy']:.2f}%")
        print(f"Citation Accuracy: {result['citation_acc']:.2f}%")
        print("-" * 80)
    
    # Summary statistics
    if len(all_results) > 1:
        avg_accuracy = sum(r['accuracy'] for r in all_results) / len(all_results)
        avg_citation_acc = sum(r['citation_acc'] for r in all_results) / len(all_results)
        best_result = all_results[0]
        
        print("\n" + "="*80)
        print("SUMMARY")
        print("="*80)
        print(f"Total experiments: {len(all_results)}")
        print(f"Average Label Accuracy: {avg_accuracy:.2f}%")
        print(f"Average Citation Accuracy: {avg_citation_acc:.2f}%")
        print(f"\nBest performing experiment:")
        print(f"  File: {best_result['file']}")
        print(f"  Accuracy: {best_result['accuracy']:.2f}%")


def main():
    if len(sys.argv) > 1:
        # Use provided CSV files
        csv_files = []
        for arg in sys.argv[1:]:
            if os.path.isfile(arg):
                csv_files.append(arg)
            else:
                # Try glob pattern
                csv_files.extend(glob.glob(arg))
    else:
        # Default: find all CSV files in logs directory
        csv_files = glob.glob("logs/**/*.csv", recursive=True)
    
    display_results(csv_files)


if __name__ == "__main__":
    main()