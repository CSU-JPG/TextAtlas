# Get Evaluation Data
You can access our TextAtlasEval data and get detailed information about the data at the following address: [**🤗 TextAtlasEval Dataset**](https://huggingface.co/datasets/CSU-JPG/TextAtlasEval)


## Dataset Features

* `image (img)`: The GT image.
* `annotation (string)`: The input prompt used to generate the text.
* `image_path (string)`: The image name.
* `raw_text (string)`: The text that appears in the image.



# Evaluation Guidelines

We provide detailed evaluation instructions.

**The evaluation should be conducted after you generate the images using your model.**

We offer two evaluation methods: one is through calling the Huggingface dataset loader, and the other is by building your own JSON for testing.

## Using Huggingface Dataset
When using this method, please ensure that the generated image names match the `image_path` in the data.

### Calculate FID score

```
python eval_script.py \
    --dataset_type <choose from "styledtextsynth", "textvisionblend", "textsceneshq"> \
    --output_dir <Path you want to save the evaluation result> \
    --image_save_dir <folder that you save the generated images> \
    --cal_fid
```


### Calculate CLIP score

```
python eval_script.py \
    --dataset_type <choose from "styledtextsynth", "textvisionblend", "textsceneshq"> \
    --output_dir <Path you want to save the evaluation result> \
    --image_save_dir <folder that you save the generated images> \
    --cal_clip
```


### Calculate OCR score

```
python eval_script.py \
    --dataset_type <choose from "styledtextsynth", "textvisionblend", "textsceneshq"> \
    --output_dir <Path you want to save the evaluation result> \
    --image_save_dir <folder that you save the generated images> \
    --cal_ocr
```



## Using Self-builded Json
When using this method, make sure that the structure of the JSON output you save is the same as ours.
### Json format
If you want to get the evaluation score of your generation result.

You can provide all the outputs in *one file* in the following format:

```
{
    "image_path": " ", # path to your generation image
    "original_image_path": " ", # path to the GT image
    "prompt": " ", #  prompt to generate the image
    "raw_text": " ", # GT text show in the image (used for OCR score)
},
....
```
## calculate FID score

```
python cal_fid.py --json_file <json_path> --save_path <sava path>
```
## calculate CLIP score

```
python cal_clip_score.py --json_file <json_path> --save_path <sava path>
```

## calculate OCR related score

To get OCR Accuracy and OCR F1 score, run:
```
python cal_ocr.py --json_file <json_path> --save_path <sava path>
```
After finishing the above command, you can get OCR CER score by runging:
```
python cal_ocr_cer.py --ocr_result_path <sava path in the above command>
```
