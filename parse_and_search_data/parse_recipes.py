import xml.etree.ElementTree as ET
import json

ingredient_array = []
tree = ET.parse('../FoodBase_uncurated.xml')
root = tree.getroot()
f = open("../corpus/recipes.txt", "w+")

for child in root:
    for document in child.iter('infon'):
        if 'full_text' in document.attrib['key']:
            f.write(document.text.strip()+'\n')

im2 = open('../im2Recipie_database.json', 'r')
data = json.loads(str(im2.read()))
for v in data:
    for key, value in v.items():
        if key == 'instructions':
            instructions = ''
            for phrase in value:
                instructions += list(phrase.values())[0] + " "
            f.write(instructions)

f.close()
im2.close()
