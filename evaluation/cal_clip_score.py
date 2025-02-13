import torch
from PIL import Image
from transformers import CLIPProcessor, CLIPModel, AutoTokenizer
import json
from tqdm import tqdm

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(device)
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
tokenizer = AutoTokenizer.from_pretrained("openai/clip-vit-base-patch32")

def read_json(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)
    return data
def preprocess_image(image_path):
    try:
        image = Image.open(image_path).convert("RGB")  # 确保是RGB图像
        return image
    except Exception as e:
        print(f"Error processing image {image_path}: {str(e)}")
        return None

def calculate_clip_score(image_path, text):
    image = preprocess_image(image_path)
    
    if image is None:
        print(f"Skipping comparison due to image loading error")
        return 0.0

    inputs = processor(
        text=[text],
        images=image,
        return_tensors="pt",
        padding=True
    )
    # 将输入移到 GPU
    inputs = {key: val.to(device) for key, val in inputs.items()}
    if inputs['input_ids'].shape[1] > 77:
        inputs['input_ids'] = inputs['input_ids'][:, :77]
        inputs['attention_mask'] = inputs['attention_mask'][:, :77]

    inputs = {key: val.to(device) for key, val in inputs.items()}

    with torch.no_grad():
        image_features = model.get_image_features(pixel_values=inputs['pixel_values'])
        text_features = model.get_text_features(input_ids=inputs['input_ids'], 
                                              attention_mask=inputs['attention_mask'])
        
        image_features = image_features / image_features.norm(dim=-1, keepdim=True)
        text_features = text_features / text_features.norm(dim=-1, keepdim=True)
        
        similarity = (image_features @ text_features.T)[0][0]
    
    return similarity.item()

def calculate_clip_scores_batch(image_paths, texts, batch_size=32):
    scores = []
    for i in tqdm(range(0, len(image_paths), batch_size)):
        batch_images = []
        batch_valid_indices = []
        batch_texts = []
        
        for j, (img_path, text) in enumerate(zip(image_paths[i:i+batch_size], texts[i:i+batch_size])):
            image = preprocess_image(img_path)
            if image is not None:
                batch_images.append(image)
                batch_texts.append(text)
                batch_valid_indices.append(i + j)
        
        if not batch_images: 
            continue
            

        inputs = processor(
            text=batch_texts,
            images=batch_images,
            return_tensors="pt",
            padding=True
        )

        inputs = {key: val.to(device) for key, val in inputs.items()}
        if inputs['input_ids'].shape[1] > 77:
            inputs['input_ids'] = inputs['input_ids'][:, :77]
            inputs['attention_mask'] = inputs['attention_mask'][:, :77]
        with torch.no_grad():

            image_features = model.get_image_features(pixel_values=inputs['pixel_values'])

            text_features = model.get_text_features(input_ids=inputs['input_ids'], 
                                                    attention_mask=inputs['attention_mask'])
            
            image_features = image_features / image_features.norm(dim=-1, keepdim=True)
            text_features = text_features / text_features.norm(dim=-1, keepdim=True)
            
            similarities = (image_features @ text_features.T).diagonal()
        
        for idx, score in zip(batch_valid_indices, similarities.cpu().tolist()):
            scores.append((idx, score))
                
            
    return scores

def write_json(save_path, data):
    with open(save_path, 'w') as f:
        json.dump(data, f)

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--json_file", type=str, default="")
parser.add_argument("--save_path", type=str, default="")
args = parser.parse_args()

json_file = args.json_file
save_path = args.save_path

data = read_json(json_file)
image_paths = []
texts = []

for item in data:
    try:
        generated_image_path = item['image_path']
        text = item["prompt"]

        image_paths.append(generated_image_path)
        texts.append(text)
    except Exception as e:
        print(f"Error collecting item: {str(e)}")
        continue

batch_size = 32 


clip_scores = calculate_clip_scores_batch(image_paths, texts, batch_size)

total_clip_score = sum(score for _, score in clip_scores)
valid_comparisons = len(clip_scores)

if valid_comparisons > 0:
    print(f"CLIP score: {total_clip_score / valid_comparisons} (based on {valid_comparisons} valid comparisons)")
    write_json(os.path.join(save_path, "clip_scores.json"), clip_scores)
else:
    print("No valid comparisons were made")