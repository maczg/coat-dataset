#!/usr/bin/env python3
"""
Split coat_dataset.csv into train/test sets by question_slug categories.
Creates the directory structure and CSV files as defined in README.md
"""

import os
import csv
import random
from pathlib import Path

# Set random seed for reproducibility
random.seed(42)

# Define the categories based on README.md configuration
CATEGORIES = [
    'behavioral-marketing',
    'security',
    'third-party-collection',
    'history',
    'data-deletion',
    'data-breaches',
    'third-party-access',
    'data-collection-reasoning',
    'noncritical-purposes',
    'law-enforcement',
    'list-collected',
    'revision-notify'
]

def read_dataset(filepath):
    """Read the dataset and group rows by question_slug."""
    data_by_category = {category: [] for category in CATEGORIES}
    
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            question_slug = row['question_slug']
            if question_slug in data_by_category:
                data_by_category[question_slug].append(row)
    
    return data_by_category

def split_data(data, train_ratio=0.8):
    """Split data into train and test sets."""
    # Shuffle the data
    shuffled_data = data.copy()
    random.shuffle(shuffled_data)
    
    # Calculate split point
    split_point = int(len(shuffled_data) * train_ratio)
    
    train_data = shuffled_data[:split_point]
    test_data = shuffled_data[split_point:]
    
    return train_data, test_data

def write_csv(filepath, data, fieldnames):
    """Write data to a CSV file."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

def main():
    """Main function to split the dataset."""
    print("Reading coat_dataset.csv...")
    
    # Get fieldnames from original file
    with open('coat_dataset.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
    
    # Read and group data
    data_by_category = read_dataset('coat_dataset.csv')
    
    # Process each category
    for category in CATEGORIES:
        data = data_by_category[category]
        
        if not data:
            print(f"Warning: No data found for category '{category}'")
            continue
        
        # Split the data
        train_data, test_data = split_data(data, train_ratio=0.8)
        
        # Define output paths
        train_path = f'data/{category}/train.csv'
        test_path = f'data/{category}/test.csv'
        
        # Write the files
        write_csv(train_path, train_data, fieldnames)
        write_csv(test_path, test_data, fieldnames)
        
        print(f"Category '{category}':")
        print(f"  - Total samples: {len(data)}")
        print(f"  - Train samples: {len(train_data)} -> {train_path}")
        print(f"  - Test samples: {len(test_data)} -> {test_path}")
        print()
    
    print("Dataset splitting completed!")

if __name__ == "__main__":
    main()