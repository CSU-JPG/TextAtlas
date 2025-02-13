import numpy as np
import torch
from torchvision import models, transforms
from torch.utils.data import Dataset, DataLoader
from torchvision.datasets import ImageFolder
from scipy.linalg import sqrtm
from PIL import Image
import os
import json
from tqdm import tqdm
import argparse

class ImagePairDataset(Dataset):
    def __init__(self, json_data):
        self.data = json_data
        self.transform = transforms.Compose([
            transforms.Resize(299),
            transforms.CenterCrop(299),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        item = self.data[idx]
        real_image = Image.open(item["original_image_path"]).convert('RGB')
        gen_image = Image.open(item['image_path']).convert('RGB')
        
        return self.transform(real_image), self.transform(gen_image)

def get_inception_model():
    model = models.inception_v3(weights='IMAGENET1K_V1')
    model.fc = torch.nn.Identity() 
    model.eval()
    if torch.cuda.is_available():
        model = model.cuda()
    return model

def save_json(json_path, data):
    with open(json_path, 'w') as f:
        json.dump(data, f, indent=4)

def calculate_fid(real_features, fake_features):
    mu_r, sigma_r = real_features.mean(axis=0), np.cov(real_features, rowvar=False)
    mu_f, sigma_f = fake_features.mean(axis=0), np.cov(fake_features, rowvar=False)
    
    diff = mu_r - mu_f
    covmean = sqrtm(sigma_r.dot(sigma_f))
    
    if np.iscomplexobj(covmean):
        covmean = covmean.real
    
    fid = np.linalg.norm(diff) ** 2 + np.trace(sigma_r + sigma_f - 2 * covmean)
    return fid


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--json_file", type=str, default="")
    parser.add_argument("--save_path", type=str, default="")
    args = parser.parse_args()
    json_file = args.json_file
    save_path = args.save_path
    os.makedirs(save_path, exist_ok=True)
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    dataset = ImagePairDataset(data)
    dataloader = DataLoader(dataset, batch_size=32, shuffle=False, num_workers=4)
    
    model = get_inception_model()
    
    real_features = []
    fake_features = []
    
    with torch.no_grad():
        for real_images, fake_images in tqdm(dataloader):
            if torch.cuda.is_available():
                real_images = real_images.cuda()
                fake_images = fake_images.cuda()
            
            real_feat = model(real_images).cpu().numpy()
            fake_feat = model(fake_images).cpu().numpy()
            
            real_features.append(real_feat)
            fake_features.append(fake_feat)
    
    real_features = np.concatenate(real_features, axis=0)
    fake_features = np.concatenate(fake_features, axis=0)
    
    fid_score = calculate_fid(real_features, fake_features)
    
    tmp_data = {
        "json_file": json_file,
        "fid_score": fid_score
    }
    print(f"FID Score: {fid_score} for {json_file}")
    save_json(os.path.join(save_path, "fid_score.json"), tmp_data)
if __name__ == "__main__":
    main()