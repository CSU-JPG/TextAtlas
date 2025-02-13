from fuzzywuzzy import fuzz
from collections import Counter
import json
import os
import argparse
from tqdm import tqdm
from paddleocr import PaddleOCR
import cv2

def compute_ocr_accuracy_fuzzy_threshold(original_texts, ocr_results, threshold=80):
    total_words = 0
    correct_words = 0
    total_predicted_words = 0  # For precision calculation
    
    for image_path, original_text in original_texts.items():
        ocr_text = ocr_results.get(image_path, "")
        
        # Split texts into words
        original_words = original_text.strip().lower().split()
        ocr_words = ocr_text.strip().lower().split()
        
        sample_total_words = len(original_words)
        sample_predicted_words = len(ocr_words)  # For precision calculation
        sample_correct_words = 0
        
        # Use a set to keep track of matched words in the ground truth
        matched_indices = set()
        
        # Fuzzy match each OCR word to ground truth words
        for ocr_word in ocr_words:
            for i, original_word in enumerate(original_words):
                if i not in matched_indices and fuzz.ratio(ocr_word, original_word) >= threshold:
                    sample_correct_words += 1
                    matched_indices.add(i)
                    break
        
        # Update global counts
        total_words += sample_total_words
        total_predicted_words += sample_predicted_words
        correct_words += sample_correct_words
        
        # Compute sample metrics
        sample_accuracy = sample_correct_words / sample_total_words * 100 if sample_total_words > 0 else 0
        sample_precision = sample_correct_words / sample_predicted_words * 100 if sample_predicted_words > 0 else 0
        sample_recall = sample_correct_words / sample_total_words * 100 if sample_total_words > 0 else 0
        sample_f1 = 2 * (sample_precision * sample_recall) / (sample_precision + sample_recall) if (sample_precision + sample_recall) > 0 else 0
        
        print(f"\nMetrics for {image_path}:")
        print(f"Accuracy: {sample_accuracy:.2f}% ({sample_correct_words}/{sample_total_words} words correct)")
        print(f"Precision: {sample_precision:.2f}%")
        print(f"Recall: {sample_recall:.2f}%")
        print(f"F1 Score: {sample_f1:.2f}%")
    
    # Compute overall metrics
    overall_accuracy = correct_words / total_words * 100 if total_words > 0 else 0
    overall_precision = correct_words / total_predicted_words * 100 if total_predicted_words > 0 else 0
    overall_recall = correct_words / total_words * 100 if total_words > 0 else 0
    overall_f1 = 2 * (overall_precision * overall_recall) / (overall_precision + overall_recall) if (overall_precision + overall_recall) > 0 else 0
    
    print(f"\nOverall Metrics:")
    print(f"Accuracy: {overall_accuracy:.2f}%")
    print(f"Precision: {overall_precision:.2f}%")
    print(f"Recall: {overall_recall:.2f}%")
    print(f"F1 Score: {overall_f1:.2f}%")
    
    return overall_accuracy, overall_precision, overall_recall, overall_f1

class OCREvaluatorFuzzy:
    def __init__(self, threshold=80):
        self.threshold = threshold
        # 设置为英文模式
        self.ocr = PaddleOCR(use_angle_cls=True, lang='en', show_log=False, use_gpu=True)

    def detect_text(self, image_path):
        """
        Detect text in image using PaddleOCR
        """
        try:
            result = self.ocr.ocr(image_path, cls=True)
            if not result or not result[0]:
                return ""
            
            # Extract text from OCR results and join with spaces
            texts = []
            for line in result[0]:
                if line[1][0]:  # Check if text exists
                    texts.append(line[1][0].strip())
            return " ".join(texts)
        except Exception as e:
            print(f"Error processing {image_path}: {str(e)}")
            return ""

    def compute_metrics(self, original_text, ocr_text):
        """
        Calculate metrics for a single image pair
        """
        # Split texts into words
        original_words = original_text.strip().lower().split()
        ocr_words = ocr_text.strip().lower().split()
        
        sample_total_words = len(original_words)
        sample_predicted_words = len(ocr_words)
        sample_correct_words = 0
        
        # Use a set to keep track of matched words
        matched_indices = set()
        
        # Fuzzy match each OCR word to ground truth words
        for ocr_word in ocr_words:
            for i, original_word in enumerate(original_words):
                if i not in matched_indices and fuzz.ratio(ocr_word, original_word) >= self.threshold:
                    sample_correct_words += 1
                    matched_indices.add(i)
                    break
        
        # Compute metrics
        accuracy = sample_correct_words / sample_total_words * 100 if sample_total_words > 0 else 0
        precision = sample_correct_words / sample_predicted_words * 100 if sample_predicted_words > 0 else 0
        recall = sample_correct_words / sample_total_words * 100 if sample_total_words > 0 else 0
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        
        return {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1': f1,
            'correct_words': sample_correct_words,
            'predicted_words': sample_predicted_words,
            'ground_truth_words': sample_total_words
        }

    def print_metrics(self, metrics, image_path=None):
        """Print metrics for a single image"""
        if image_path:
            print(f"\nMetrics for {image_path}:")
        print(f"Accuracy: {metrics['accuracy']:.2f}% ({metrics['correct_words']}/{metrics['ground_truth_words']} words correct)")
        print(f"Precision: {metrics['precision']:.2f}%")
        print(f"Recall: {metrics['recall']:.2f}%")
        print(f"F1 Score: {metrics['f1']:.2f}%")

def main(args):


    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)

    # Load ground truth data
    with open(args.json_file, 'r') as f:
        data = json.load(f)

    # Initialize OCR evaluator
    evaluator = OCREvaluatorFuzzy(threshold=args.threshold)
    
    # Store all results
    total_results = []
    result_data = []
    # Process each image
    for item in tqdm(data):

        image_path = item['image_path']


        ground_truth = item["raw_text"]

        # Perform OCR
        ocr_text = evaluator.detect_text(image_path)

        # Compute metrics for this image
        metrics = evaluator.compute_metrics(ground_truth, ocr_text)
        total_results.append(metrics)
        
        
        # # Save OCR results
        result_path = os.path.join(args.output_dir, 'ocr_data.json')
        result_data.append({
            'image_path': image_path,
            'ground_truth': ground_truth,
            'ocr_text': ocr_text
        })

    with open(result_path, 'w') as f:
        json.dump(result_data, f, indent=4)

    # Calculate and print overall metrics
    total_correct = sum(r['correct_words'] for r in total_results)
    total_predicted = sum(r['predicted_words'] for r in total_results)
    total_ground_truth = sum(r['ground_truth_words'] for r in total_results)

    overall_accuracy = total_correct / total_ground_truth * 100 if total_ground_truth > 0 else 0
    overall_precision = total_correct / total_predicted * 100 if total_predicted > 0 else 0
    overall_recall = total_correct / total_ground_truth * 100 if total_ground_truth > 0 else 0
    overall_f1 = 2 * (overall_precision * overall_recall) / (overall_precision + overall_recall) if (overall_precision + overall_recall) > 0 else 0

    print("\nOverall Metrics:")
    print(f"Accuracy: {overall_accuracy:.2f}%")
    print(f"Precision: {overall_precision:.2f}%")
    print(f"Recall: {overall_recall:.2f}%")
    print(f"F1 Score: {overall_f1:.2f}%")

    return overall_accuracy, overall_precision, overall_recall, overall_f1

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--json_file", type=str, default="")
    parser.add_argument("--output_dir", type=str, default="")
    parser.add_argument("--threshold", type=int, default=80, help="Fuzzy matching threshold")
    args = parser.parse_args()
    overall_accuracy, overall_precision, overall_recall, overall_f1 = main(args)
    save_path = os.path.join(args.output_dir, 'ocr_results.json')
    with open(save_path, 'w') as f:
        json.dump({
            'overall_accuracy': overall_accuracy,
            'overall_precision': overall_precision,
            'overall_recall': overall_recall,
            'overall_f1': overall_f1
        }, f, indent=4)