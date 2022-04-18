import fitz
import os
import json
from PIL import Image
import pyperclip
import pytesseract

try:
    os.mkdir("white")
except:pass
try:
    os.mkdir("black")
except:pass

pdffile = "CAH.pdf"
doc = fitz.open(pdffile)
num = 1
cardNum = 1
cahJSON = {
  "name": "Cartas contra la Humanidad",
  "codeName": "cahESP",
  "whiteCards": [],
  "blackCards": [
    {
      "text": "Why did the chicken cross the road?",
      "pick": 1
    },
    {
      "text": "You like _? Well _&trade; is better!",
      "pick": 2
    }
  ]
}

for page in doc:
    if num < 22:
        prefix = "white"
    if num == 22:
        cardNum = 1
    if num >= 22:
        prefix = "black"
    if num != 1:
        print(page)
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        box = (19, 38, 593, 754)
        area = img.crop(box)

        for x in range(5):
            for y in range(4):
                cardarea = ((y*144), (x*144), ((y+1)*144), ((x+1)*144))
                card = area.crop(cardarea)
                card.save(prefix+"/"+prefix+"Card"+str(cardNum)+".png")
                cardNum += 1
                if prefix == "white":
                    cahJSON["whiteCards"].append(str(pytesseract.image_to_string(card.crop((0, 0, 144, 114)), config="-l spa")).replace("\n", " "))
                    
                elif prefix == "black":
                    cahJSON["blackCards"].append({"text": str(pytesseract.image_to_string(card.crop((0, 0, 144, 114)), config="-l spa")).replace("\n", " "), "pick": 1})
    num += 1

f = open("cahESP.json", "w+")
f.write(json.dumps(cahJSON))
f.close()
pyperclip.copy(json.dumps(cahJSON))

