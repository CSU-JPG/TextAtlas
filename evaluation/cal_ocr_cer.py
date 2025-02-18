
import json
from typing import List, Dict, Tuple
import Levenshtein
from tqdm import tqdm
import os
import argparse

def calculate_metrics(gt_text: str, ocr_text: str) -> Tuple[int, float]:
    """
    Calculate Levenshtein distance and CER between ground truth and OCR text.
    
    Args:
        gt_text: Ground truth text
        ocr_text: OCR detected text
        
    Returns:
        Tuple of (levenshtein_distance, character_error_rate)
    """
    if not gt_text:  # Handle empty ground truth
        return 0, 0.0
        
    ocr_text = ocr_text if ocr_text else ""  # Handle empty OCR text
    
    # Calculate Levenshtein distance
    distance = Levenshtein.distance(gt_text, ocr_text)
    
    # Calculate CER
    cer = distance / max(len(gt_text), len(ocr_text))
    
    # cer = min(cer, 1.0)

    return distance, cer

def process_data(data: List[Dict]) -> List[Dict]:
    """
    Process OCR data and calculate metrics for each entry.
    
    Args:
        data: List of dictionaries containing image_path, ground_truth and ocr_text
        
    Returns:
        List of dictionaries with added metrics
    """
    results = []
    total_distance = 0
    total_cer = 0
    valid_entries = 0

    for entry in data:
        gt_text = entry['ground_truth']
        ocr_text = entry['ocr_text']
        
        # Calculate metrics
        distance, cer = calculate_metrics(gt_text, ocr_text)
        
        # Add metrics to entry
        entry_with_metrics = entry.copy()
        entry_with_metrics.update({
            'levenshtein_distance': distance,
            'cer': cer
        })
        results.append(entry_with_metrics)
        
        # Update totals
        if gt_text:  # Only count entries with non-empty ground truth
            total_distance += distance
            total_cer += cer
            valid_entries += 1
    
    # Calculate averages
    avg_distance = total_distance / valid_entries if valid_entries > 0 else 0
    avg_cer = total_cer / valid_entries if valid_entries > 0 else 0
    
    return results, avg_distance, avg_cer

def main(args):
    ocr_result_path = args.ocr_result_path
    total_json_list = []
    for root, dirs, files in os.walk(ocr_result_path):
        for file in files:
            if file.endswith('ocr_data.json'):
                # Read JSON file
                total_json_list.append(os.path.join(root, file))
    
    for json_file in total_json_list:
        with open(json_file, 'r') as f:
            data = json.load(f)
        
        # Process data and calculate metrics
        results, avg_distance, avg_cer = process_data(data)
        
        # Print summary
        print(f"Total entries processed: {len(results)}")
        print(f"Average Levenshtein distance: {avg_distance:.2f}")
        print(f"Average Character Error Rate (CER): {avg_cer:.2%}")
        
        # Save results to new JSON file
        output_file = json_file.replace('ocr_data.json', 'ocr_results_with_metrics.json')
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=4)
        output_file = json_file.replace('ocr_data.json', 'ocr_results_with_metrics_avg.json')
        avg_result = {
            'avg_distance': avg_distance,
            'avg_cer': avg_cer
        }
        with open(output_file, 'w') as f:
            json.dump(avg_result, f, indent=4)

        print(f"AVERAGE CER: {avg_cer}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ocr_result_path", type=str, default="")
    args = parser.parse_args()
    main(args)