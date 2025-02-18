
# TextAtlas5M

<p align="center">
  <img src="https://github.com/user-attachments/assets/5e2c5c85-d38d-4a11-8872-e527c3ee8799" width="300">
</p>

<h3 align="center"> A Large-scale Dataset for Dense Text Image Generation</h3>

[**🌐 Homepage**](https://textatlas5m.github.io/) | [**🏆 Leaderboard**](https://textatlas5m.github.io/#leaderboard) | [**🤗 TextAtlas5M**](https://huggingface.co/datasets/CSU-JPG/TextAtlas5M) | [**🤗 TextAtlasEval**](https://huggingface.co/datasets/CSU-JPG/TextAtlasEval) | [**📖 TextAtlas arXiv**](https://arxiv.org/pdf/2502.07870)

This repo contains the evaluation code for the paper "[TextAtlas5M: A Large-scale Dataset for Dense Text Image Generation](https://arxiv.org/pdf/2502.07870)" 

## Updates

- released TextAtlasEval version 1.0 :fire:

## Table of Contents
- [Get dataset](#Accessing-TextAtlas)
- [Evaluation](#Evaluation)
- [Data Format](#Data-Format)


## Accessing TextAtlas

TextAtlas was meticulously designed to challenge and evaluate text-rich image generation. For more detailed information, please refer to our Hugging Face datasets:
- [**🤗 TextAtlas5M Dataset**](https://huggingface.co/datasets/CSU-JPG/TextAtlas5M) 
- [**🤗 TextAtlasEval Dataset**](https://huggingface.co/datasets/CSU-JPG/TextAtlasEval)

## Evaluation
Please refer to our evaluation folders for detailed information on evaluating with TextAtlas benchmark:

- [**TextAtlas Evaluation**](evaluation)


## Data Format

The TextAtlas annotation documentation is available in huggingface:

- **main version**: Contains image paths and pre-integrated prompts, making it suitable for direct training or evaluation.
- **Meta data**: Includes all the data from main version, along with additional intermediate results such as bounding boxes (bbox), font size, and other related information, which can be used for further data analysis or processing.

### Example
```json
{
  "image_path": "000004f933f14f65bfcd6ee1d54d4e69.png",
  "annotation": "	A 512x512 text image with the following settings: font_size 231 , font_type Winterday-jEqqO , font_color [77, 34, 70] displaying the text: the library."
}
```


| entry                 | description                                                                                                                                                                            |
|-----------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `image_path`          | `str`, The image name                                                                                                                                                                     |
| `annotatoin` | `str`, Full Description                                                                                                                                                                | 

### For Metadata
In addition to the data from main version, meta data includes intermediate results retained during the processing of different subsets. These results provide useful metadata for further analysis, such as bounding boxes (bbox), font size, and other processing details.

Please refer to the [**TextAtlas Detailed Annotation**](detialed_annotation) for more comprehensive details on the second version annotations.


## Data Level, Datasets, and Annotations Overview

| Data Split       | Dataset Name      | #Samples  | Annotations                  | Type             | Token Length | Contain Structured info|
|------------------|-------------------|-----------|------------------------------|------------------|--------------|--------------|
| Synthetic Images | CleanTextSynth    | 1,907,721 | Real Text                    | Pure Text        | 70.70        |       ❌       |
| Synthetic Images | TextVisionBlend   | 547,837   | Parsed json+BLIP Caption     | Pure Text        | 265.62       |       ✅       | 
| Synthetic Images | StyledTextSynth   | 426,755   | Human+ QWEN+Intern-VL        | Synthetic Image  | 90.00        |       ✅      |
| -                | -                 | -         | -                            | -                | -            | -            |
| Real Images      | PPT2Details       | 298565    | QWEN2-VL Caption             | Powerpoint Image | 121.97       |       ❌       |
| Real Images      | PPT2Structured    | 96457     | Parsed json+QWEN2-VL Caption | Powerpoint Image | 774.67       |       ✅       |
| Real Images      | LongWordsSubset-A | 266534    | Caption + OCR                | Real Image       | 38.57        |       ❌       |
| Real Images      | LongWordsSubset-M | 1299992   | Caption + OCR                | Real Image       | 34.07        |        ❌      |
| Real Images      | Cover Book        | 207566    | Name + Author + Category     | Real Image       | 28.01        |        ❌      |
| Real Images      | Paper2Text        | 356,658       | PyMuPdf phrased Text         | Pure Text        | 28.01        |      ❌        |
| Real Images      | TextScenesHQ      | 36,576     | Human+Llama+Qwen+GPT4o       | Real Image       | 120.81       |         ✅     |
| In Total         | TextAtlas5M 5M    | ～ 5M        | -                            | -                | 148.82       |              |


## Citation

If you found our work useful, please consider citing:
```
@inproceedings{wang2025large,
            title={A Large-scale Dataset for Dense Text Image Generation},
            author={Alex Jinpeng Wang and Dongxing Mao and  Jiawei Zhang and weiming Han and Zhuobai Dong and Linjie Li and Yiqi Lin and Zhengyuan Yang and Libo Qin and Fuwei Zhang and Lijuan Wang and Min Li},
            booktitle={arXiv preprint arXiv: 2502.07870},
            year={2025},
        }
```


