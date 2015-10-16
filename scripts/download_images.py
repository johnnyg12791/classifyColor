import requests
import pandas as pd
import shutil
from collections import Counter
import urllib

#Top 10 colors

def main():
	df = pd.read_csv("../data/nordstrom_data_val.csv", na_values = [], keep_default_na=False)
	#popular_colors = makeColorsCSV(df)
	popular_colors = colorsCSVToDict()
	getPhotoData(df, popular_colors)




#Given the nordstrom csv, I want to get the image and associate it with a color
def getPhotoData(df, popular_colors):
	#UPC is unique, download img, name it UPG.JPG
	f = open("../data/val.txt", "w+")
	for row_index, row in df.iterrows():
		colors = colorsForRow(row)
		#If this is a valid color
		for c in colors:
			#I either want to take the most common color
			#Or download the image multiple times for each common color
			if c in popular_colors.keys():
				img_url = row["large_image_URL"]
				UPC = row["UPC"]
				img_name = "{}.jpg".format(UPC)
				#Download Image to images/train/img_name
				try:
					urllib.urlretrieve(img_url, img_name)
					#Write image name *space* popular_colors[color]
					f.write("{} {}\n".format(img_name, popular_colors[c]))
					#Only take 1 of the colors for now
					print row_index, " ", c
				except:
					print "error with {}".format(img_url)
				break
	f.close()



#ColorsCSVtoDict
def colorsCSVToDict():
	popular_colors = {}
	df = pd.read_csv("popular_colors.csv")
	for row_index, row in df.iterrows():
		popular_colors[row["color"]] = row["index"]

	print popular_colors
	return popular_colors


#Makes a CSV of the most popular colors, and index
def makeColorsCSV(df):
	print "Writing Colors CSV"
	all_colors = set()
	all_colors = Counter()
	for row_index, row in df.iterrows():
		colors = colorsForRow(row)
		for c in colors:
			all_colors[c] += 1
		
	print all_colors
	f = open("../misc/popular_colors.csv", 'w+')
	f.write("color,index\n")
	index = 0
	popular_colors = {}
	for color in all_colors.most_common():
		color = color[0]
		if all_colors[color] > 200 and (color != "" and color != "no color"):
			f.write("{},{}\n".format(color, index))
			popular_colors[color] = index
			index += 1

	return popular_colors


#Returns a list of colors in the row
def colorsForRow(row):
	color_array = row["colors"].lower().split("/")
	return [c.strip() for c in color_array]


if __name__=="__main__":
	main()