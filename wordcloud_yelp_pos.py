import numpy as np
import csv
import random
from PIL import Image
from wordcloud import WordCloud, STOPWORDS
from palettable.colorbrewer.sequential import Greens_9

def color_func(word, font_size, position, orientation, random_state=None, **kwargs):
    return tuple(Greens_9.colors[random.randint(2,8)])

csv_path = "yelp_words_by_stars_1gram.csv"
fa_path = "/Users/maxwoolf/Downloads/exported2048/"
font_path = "/Users/maxwoolf/Fonts/OpenSans-CondBold.ttf"

icon = "smile-o"

words_array = []
with open(csv_path, 'rb') as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
			if row['stars'] is '5' and row['word'] not in STOPWORDS:
				words_array.append((row['word'].upper(), float(row['count'])))
		 		
# http://stackoverflow.com/questions/7911451/pil-convert-png-or-gif-with-transparency-to-jpg-without
icon_path = fa_path + "%s.png" % icon
icon = Image.open(icon_path)
mask = Image.new("RGB", icon.size, (255,255,255))
mask.paste(icon,icon)
mask = np.array(mask)

wc = WordCloud(font_path=font_path, background_color="white", max_words=2000, mask=mask,
               max_font_size=300, random_state=42)
               
# generate word cloud
wc.generate_from_frequencies(words_array)
wc.recolor(color_func=color_func, random_state=3)
wc.to_file("yelp_pos_wordcloud.png")