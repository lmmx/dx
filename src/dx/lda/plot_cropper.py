from pathlib import Path
from PIL import Image
import numpy as np

def crop_image(img_path, inplace=False):
    if not isinstance(img_path, Path):
        img_path = Path(img_path)
    image=Image.open(img_path)
    image.load()

    image_data = np.asarray(image)
    non_empty_columns = np.where(image_data.min(axis=0) < 255)[0]
    col_pad = 5 # pixels padding either side
    min_col = min(non_empty_columns)
    max_col = max(non_empty_columns)
    if min_col >= col_pad:
        min_col -= col_pad
    if max_col <= (image_data.shape[1] - col_pad):
        max_col += col_pad
    cropBox = (0, image_data.shape[0], min_col, max_col)

    image_data_new = image_data[cropBox[0]:cropBox[1]+1, cropBox[2]:cropBox[3]+1 , :]

    new_image = Image.fromarray(image_data_new)
    if inplace:
        img_out = img_path
    else:
        img_out = img_path.parent / (img_path.stem + "_cropped" + img_path.suffix)
    new_image.save(img_out)
