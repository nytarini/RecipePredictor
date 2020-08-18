import xml.etree.ElementTree as ET
import csv

ingredient_array = []
tree = ET.parse('/Users/mirawelner/Documents/RecipePredictor/FoodBase_uncurated.xml')
root = tree.getroot()
for child in root:
    for document in child.iter('annotation'):
        for text in document.iter('text'):
            duplicate = any(text.text.lower() in string for string in ingredient_array)
            if duplicate is False:
                ingredient_array.append(text.text)

with open("/Users/mirawelner/Documents/RecipePredictor/vocabularies/ingredient_vocabulary.csv", 'w+',
          newline='') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerow(ingredient_array)
