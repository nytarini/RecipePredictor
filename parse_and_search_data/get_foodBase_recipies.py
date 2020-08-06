import xml.etree.ElementTree as ET
import csv

ingredient_array = []
tree = ET.parse('../FoodBase_uncurated.xml')
root = tree.getroot()
f = open("../corpus/FoodBase_recipies.txt", "w+")

for child in root:
    for document in child.iter('infon'):
        if 'full_text' in document.attrib['key'] :
            f.write(document.text.strip()+'\n')

f.close()