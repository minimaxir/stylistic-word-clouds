import numpy as np
import csv
import random
from PIL import Image
from wordcloud import WordCloud, STOPWORDS
from palettable.colorbrewer.qualitative import Dark2_8

def color_func(word, font_size, position, orientation, random_state=None, **kwargs):
    return tuple(Dark2_8.colors[random.randint(0,7)])

csv_path = "cnn_facebook_statuses.csv"
fa_path = "/Users/maxwoolf/Downloads/exported2048/"
font_path = "/Users/maxwoolf/Fonts/AmaticSC-Bold.ttf"

icon = "flag"

message = ''
with open(csv_path, 'rb') as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
		message += " " + row['link_name']
		 		
# http://stackoverflow.com/questions/7911451/pil-convert-png-or-gif-with-transparency-to-jpg-without
icon_path = fa_path + "%s.png" % icon
icon = Image.open(icon_path)
mask = Image.new("RGB", icon.size, (255,255,255))
mask.paste(icon,icon)
mask = np.array(mask)

wc = WordCloud(font_path=font_path, background_color="white", max_words=2000, mask=mask,
               max_font_size=300, random_state=42)
               
# generate word cloud
wc.generate_from_text(message)
wc.recolor(color_func=color_func, random_state=3)
wc.to_file("cnn_wordcloud.png")