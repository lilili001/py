import pytesseract
from PIL import Image
import os
root_path = os.path.abspath('.')
print(root_path)

tessdata_dir_config = '--tessdata-dir "C:\\Program Files (x86)\\Tesseract-OCR\\tessdata"'
pic = Image.open(root_path+'/checkcode.png')
capture = pytesseract.image_to_string(pic)
print(capture)