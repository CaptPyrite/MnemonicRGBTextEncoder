from PIL import Image
import string
import hashlib
import random
from typing import Dict
import os

def mnemonic2rgb(m:str) -> Dict[str, tuple]:
    random.seed(hashlib.sha256(m.encode('utf-8')).hexdigest())
    ascii_chars = {}
    printable = list(string.printable) + ["NOTHING"]
    
    for index_, alph in enumerate(printable):
        RGB_values = (random.randint(0, 255),
                      random.randint(0, 255),
                      random.randint(0, 255))
        
        if RGB_values not in ascii_chars.values():
            ascii_chars[alph] = RGB_values 
     
    return ascii_chars

def encode_text(text: str, m_chars: Dict[str, tuple], X: int, Y: int) -> Image.Image:
    img = Image.new("RGB", 
                    (X, Y), 
                    color = m_chars["NOTHING"])
    cursor = [-1, 0]

    for i, char in enumerate(text):
        if cursor[0] >= (X - 1):
            cursor[0] = 0
            cursor[1] += 1
            if cursor[1] >= (Y - 1):
                raise OverflowError(f"Increase the resolution ({X}x{Y}). Index left off at: [{i}]")
                
        else:
            cursor[0] += 1
        img.putpixel(tuple(cursor), m_chars[char])
    return img

def decode_img(img: Image.open, m_chars: Dict[str, tuple]) -> str:
    x, y = img.size
    m_alpha = {val: key for key, val in m_chars.items()}
    pixel_rgbs = list(img.getdata())
    text = ""
    for rgb in pixel_rgbs:
        if rgb != m_chars["NOTHING"]:
            text += m_alpha[rgb]
            
    return text


if __name__ == "__main__":
    CWD = os.getcwd()
    mode = input("MnemonicRGBTextEncoder\n\n(1). Encode text\n(2). Decode an image\n\n[1-2]> ")
    mnemonic_P = input("The mnemonic phrase> ")
    mnemonic_alphabet = mnemonic2rgb(mnemonic_P)
    
    match mode:
       case "1":
          text = input("Text to encode> ")
          
          x = int(input("Output image X resolution (1920)> ") or 1920)
          y = int(input("Output image Y resolution (1080)> ") or 1080)
          dir_ = input(f"Ouput image Directory ({os.getcwd()}\MnemonicRGBTextEncoded.png)> ") or os.path.join(CWD, "MnemonicRGBTextEncoded.png")
          
          img = encode_text(text, mnemonic_alphabet, x, y)
          img.save(dir_)
          
       case "2":
           img_loc = input(f"Image directory ({CWD}\MnemonicRGBTextEncoded.png)> ") or os.path.join(CWD, "MnemonicRGBTextEncoded.png")
           decoded_frame = decode_img(Image.open(img_loc), mnemonic_alphabet)
           print(decoded_frame)
         
       case _:
         print("Not a valid mode.")
