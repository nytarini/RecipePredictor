from xml.etree import ElementTree
import requests
import csv
import re

no_full_article = "<!--The publisher of this article does not allow downloading of the full text in XML form.-->"


def get_paper_from_terms(ingredient, attribute_list):
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pmc&term=" + ingredient
    r = requests.get(url=url)
    root = ElementTree.fromstring(r.content)
    for ID in root[3]:
        r = requests.get(url="https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id=" + ID.text)
        text = r.text
        journal = (text[text.find("<journal-title>") + 15:text.find("</journal-title>")])
        res = any(substring in text for substring in attribute_list)
        if 'food' in journal.lower() or 'nutrition' in journal.lower() and no_full_article not in text and res:
            text = text[
                   text.find("<title>Introduction/Background</title>") + len("<title>Introduction/Background</title>"):]
            text = text[text.find("<title>Introduction</title>") + len("<title>Introduction</title>"):]
            text = text[text.find("<title>INTRODUCTION</title>") + len("<title>INTRODUCTION</title>"):]
            text = text[text.find("<title>Background</title>") + len("<title>Background</title>"):]
            text = text[text.find("<body>") + len("<body>"):]
            text = text[:text.find("<title>Acknowledgments</title>")]
            text = text[:text.find("<title>Acknowledgment</title>")]
            text = text[:text.find("<title>References</title>")]
            text = re.sub("<table-wrap*/table-wrap>", "", text)
            text = re.sub("<table*/table>", "", text)
            text = re.sub("<[^<]+>", "", text)
            text = re.sub(r'(\n\s*)+\n+', '\n\n', text)
            text = re.sub("^	\\*\n", "", text)
            file = open("../corpus/" + ID.text + '.txt', 'w+')
            file.write(text)
            print(ID.text)


with open('../vocabularies/ingredient_vocabulary.csv') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        ingredients = row
        break

with open('../vocabularies/attribute_vocabulary.csv') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        attributes = row
        break

for x in ingredients:
    get_paper_from_terms(x, attributes)
