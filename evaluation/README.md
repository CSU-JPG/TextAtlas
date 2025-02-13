# Evaluation Guidelines
We provide detailed instructions for evaluation. 
To execute our evaluation script, please ensure that the structure of your model outputs is the same as ours.

## Json format
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
