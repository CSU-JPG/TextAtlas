
# TextAtlas5M

<p align="center">
  <img src="https://github.com/user-attachments/assets/5e2c5c85-d38d-4a11-8872-e527c3ee8799" width="300">
</p>

<h3 align="center"> A Large-scale Dataset for Dense Text Image Generation</h3>

[**🌐 Homepage**](https://textatlas5m.github.io/) | [**🏆 Leaderboard**](https://textatlas5m.github.io/#leaderboard) | [**🤗 TextAtlas5M**](https://huggingface.co/datasets/CSU-JPG/TextAtlas5M) | [**🤗 TextAtlasEval**](https://huggingface.co/datasets/CSU-JPG/TextAtlasEval) | [**📖 TextAtlas arXiv**](https://arxiv.org/pdf/2502.07870)

This repo contains the evaluation code for the paper "[TextAtlas5M: A Large-scale Dataset for Dense Text Image Generation](https://arxiv.org/pdf/2502.07870)" 

## Updates
- [2025-2-18]: Our evaluation code is now availble! 🌟
- [2025-2-13]: released TextAtlasEval & TextAtlas5M version 1.0 :fire:

## Table of Contents
- [Setup](#Setup)
- [Accessing Datasets](#Accessing-TextAtlas)
- [Evaluation](#Evaluation)
- [Data Format](#Data-Format)


## Setup

```bash
conda create -n TextAtlasEval python=3.9 
conda activate TextAtlasEval

pip install -r requirements.txt
```

## Accessing Datasets

TextAtlas was meticulously designed to challenge and evaluate text-rich image generation. For more detailed information and accessing our dataset, please refer to our Huggingface page:
- [**🤗 TextAtlas5M**](https://huggingface.co/datasets/CSU-JPG/TextAtlas5M) 
- [**🤗 TextAtlasEval**](https://huggingface.co/datasets/CSU-JPG/TextAtlasEval)

## Evaluation
Please refer to our evaluation folders for detailed information on evaluating with TextAtlasEval benchmark:

- [**TextAtlas Evaluation**](evaluation)


## Data Format

The TextAtlas annotation documentation is available in huggingface:

- **main version**: Contains image paths and pre-integrated prompts, making it suitable for direct training or evaluation.
- **Meta data**: Includes all the data from main version, along with additional intermediate results such as bounding boxes (bbox), font size, and other related information, which can be used for further data analysis or processing.

### Example


```json
{
  "image_path": "0000089b-f1ce-41cf-9cd8-688856822244.png",
  "annotation": "In an opulent boutique, a sleek white digital display contrasts sharply with meticulously arranged merchandise and luxurious decor, creating a striking visual focal point. digital display with the text : ''Amidst the opulent ambiance of the upscale boutique, a sleek white digital display stands out as a striking contrast to the meticulously arranged merchandise and sumptuous luxury decor''"
}
```

| entry                 | description                                                                                                                                                                            |
|-----------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `image_path`          | `str`, The image name                                                                                                                                                                     |
| `annotatoin` | `str`, Full Description                                                                                                                                                                | 


More Examples with images can be founded in [**🤗 TextAtlas5M**](https://huggingface.co/datasets/CSU-JPG/TextAtlas5M) and [**🤗 TextAtlasEval**](https://huggingface.co/datasets/CSU-JPG/TextAtlasEval)


### For Metadata
In addition to the data from main version, meta data includes intermediate results retained during the processing of different subsets. These results provide useful metadata for further analysis, such as bounding boxes (bbox), font size, and other processing details.

Please refer to the [**TextAtlas Detailed Annotation**](detialed_annotation) for more comprehensive details on the meta annotations.


## Citation

If you found our work useful, please consider citing:
```
@article{wang2025textatlas5m,
  title={TextAtlas5M: A Large-scale Dataset for Dense Text Image Generation},
  author={Wang, Alex Jinpeng and Mao, Dongxing and Zhang, Jiawei and Han, Weiming and Dong, Zhuobai and Li, Linjie and Lin, Yiqi and Yang, Zhengyuan and Qin, Libo and Zhang, Fuwei and others},
  journal={arXiv preprint arXiv:2502.07870},
  year={2025}
}
```


