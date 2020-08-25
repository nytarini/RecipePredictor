import sys
from xml.etree import ElementTree
import requests
import csv
import re
from tqdm import tqdm

no_full_article = "<!--The publisher of this article does not allow downloading of the full text in XML form.-->"
f = open("/corpus/articles.txt", "w+")
article_ID_list = []
reached_limit = False


def get_paper_from_terms(ingredient, attribute_list, limit_bool):
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pmc&term=" + ingredient
    r = requests.get(url=url)
    root = ElementTree.fromstring(r.content)
    try:
        for ID in root[3]:
            r = requests.get(url="https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id=" + ID.text)
            text = r.text
            journal = (text[text.find("<journal-title>") + 15:text.find("</journal-title>")])
            if not any(substring in text for substring in attribute_list):
                break
            if no_full_article in text:
                break
            if 'food' in journal.lower() or 'nutrition' in journal.lower():
                text = text[text.find("<body"):text.find("</body>")]  # only include body
                text = re.sub("(?s)<table-wrap(.*?)</table-wrap>", "", text)  # remove table wrap
                text = re.sub("(?s)<table(.*?)</table>", "", text)  # remove table
                text = re.sub("(?s)<figure(.*?)</figure>", "", text)  # remove figure
                text = re.sub("(?s)<title(.*?)</title>", "", text)  # remove title
                text = re.sub("<[^<]+>", "", text)  # remove tags
                text = re.sub("&#x2019;", "'", text)  # API doesn't download '
                text = re.sub("&#xB5;", "µ", text)  # API doesn't download italicized µ
                text = re.sub("&#x3BC;", "µ", text)  # API doesn't download µ
                text = re.sub("&#x2014;", "—", text)  # API doesn't download doesn't download —
                text = re.sub("&#x(.*);", "", text)  # other characters (impractical to find all)
                text = re.sub("\[(.*?)\]", "", text)  # remove references
                text = re.sub("^[\\\\].*", "", text)  # remove \usepackage
                text = re.sub("\n", " ", text)  # remove line brakes
                text = re.sub(" +", " ", text)  # remove duplicate spaces
                text = re.sub(" ([/.,])", "/1", text)  # API puts space before periods (probably bug??)
                text = re.sub(r"([\?\.!]) ([A-Z])", r"\1\n\2", text)  # add break after end of sentence
                f.write(text)
                f.write("\n\n")
                article_ID_list.append(ID.text)
                if len(sys.argv) > 1 and len(article_ID_list) == int(sys.argv[1]):
                    limit_bool = True
                return limit_bool
    except IndexError:
        #  this just means that the search term returned nothing - it is not a problem
        return limit_bool


with open('../vocabularies/ingredient_vocabulary.csv') as file:
    reader = csv.reader(file)
    for row in reader:
        ingredients = row
        break

with open('../vocabularies/attribute_vocabulary.csv') as file:
    reader = csv.reader(file)
    for row in reader:
        attributes = row
        break

for x in tqdm(ingredients):
    reached_limit = get_paper_from_terms(x, attributes, reached_limit)
    if reached_limit:
        break

print("The " + str(len(article_ID_list)) + " articles you have included in your corpus have the following IDs: ")
print(article_ID_list)
f.close()
