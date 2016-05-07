import numpy as np
import csv
import random
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from scipy.misc import imread
import re
from palettable.colorbrewer.diverging import Spectral_9
from matplotlib.colors import makeMappingArray

csv_path = "cnn_facebook_statuses.csv"
fa_path = "/Users/maxwoolf/Downloads/exported2048/"
font_path = "/Users/maxwoolf/Fonts/AmaticSC-Bold.ttf"

icon = "flag"
gradient_orientation = "h"

# http://stackoverflow.com/questions/7911451/pil-convert-png-or-gif-with-transparency-to-jpg-without
icon_path = fa_path + "%s.png" % icon
icon = Image.open(icon_path)
mask = Image.new("RGB", icon.size, (255,255,255))
mask.paste(icon,icon)
mask_wordcloud = np.array(mask)

# Create a linear gradient using the matplotlib color map

imgsize = icon.size

palette = makeMappingArray(imgsize[1], Spectral_9.mpl_colormap)   # interpolates colors

for y in range(imgsize[1]):
    for x in range(imgsize[0]):
    	if mask.getpixel((x,y)) != (255,255,255):   # Only change nonwhite pixels of icon
    	
    		color = palette[y] if gradient_orientation is "vertical" else palette[x]
    		
    		# matplotlib color maps are from range of (0,1). Convert to RGB.
    		r = int(color[0] * 255)
    		g = int(color[1] * 255)
    		b = int(color[2] * 255)
    		
    		mask.putpixel((x, y), (r, g, b))
			
# create coloring from image
mask.save('test2.jpg')
image_colors = ImageColorGenerator(np.array(mask))

pattern = re.compile("[^\w']")
tokens_dict = {}

with open(csv_path, 'rb') as csvfile:
		 reader = csv.DictReader(csvfile)
		 for row in reader:
			text = row['link_name'].lower()
			reactions = int(row['num_reactions'])
			
			# Map each reactions count to a word,
			# e.g.: {'futurist': [6599], 'ditch': [4667, 936, 298]}
			
			tokens = pattern.sub(' ', text).split()
			for token in tokens:
				if token not in tokens_dict.keys():
					tokens_dict[token] = [reactions]
				else:
					tokens_dict[token].append(reactions)
			
# Calculate the average amount of reactions for headlines containing word
words_dict = [(k, np.mean(np.array(v))) for k, v in tokens_dict.items() if len(v) >= 20]
print words_dict

wc = WordCloud(font_path=font_path, background_color="black", max_words=2000, mask=mask_wordcloud,
               max_font_size=400, random_state=42)
               
# generate word cloud
wc.generate_from_frequencies(words_dict)
wc.recolor(color_func=image_colors)
wc.to_file("cnn_wordcloud_reactions.png")