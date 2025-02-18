from datasets import load_dataset
from cal_ocr import cal_ocr_hf
from cal_clip_score import cal_clip_hf
from cal_fid import cal_fid_hf
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output_dir", type=str, default="results", help="The directory to save the evaluationresults")
    parser.add_argument("--image_save_dir", type=str, default="generated_images", help="The directory to save the generated images")
    parser.add_argument("--dataset_type", type=str, default="styledtextsynth", choices=["styledtextsynth", "textvisionblend", "textvision", "textsceneshq"])
    parser.add_argument("--cal_ocr", action="store_true", help="Whether to calculate the OCR metrics")
    parser.add_argument("--cal_clip", action="store_true", help="Whether to calculate the CLIP metrics")
    parser.add_argument("--cal_fid", action="store_true", help="Whether to calculate the FID metrics")
    args = parser.parse_args()

    ds = load_dataset("CSU-JPG/TextAtlasEval", args.dataset_type, split="train")

    if args.cal_fid:
        cal_fid_hf(ds, args.output_dir, args.image_save_dir)

    if args.cal_clip:
        cal_clip_hf(ds, args.output_dir, args.image_save_dir)

    if args.cal_ocr:
        cal_ocr_hf(ds, args.output_dir, args.image_save_dir)