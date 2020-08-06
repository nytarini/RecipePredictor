import os
import shutil

location = "/Users/mirawelner/Documents/pubmed.txt"  # change to where you put the pubmed folder
ingredients = open('/Users/mirawelner/Documents/RecipePredictor/vocabularies/ingredient_vocabulary.csv')
# words = ingredients.readline().split(',')
# words = [i.replace('"', '') for i in words]
words = ["food", "nutrition"]

for folder in os.listdir(location):
    for filename in os.listdir(location + '/' + folder):
        f = open(location + '/' + folder + '/' + filename, 'r')
        f.readline()
        f.readline()
        f.readline()
        f.readline()
        metadata = f.readline()
        for word in words:
            try:
                metadata.index(word)
            except ValueError:
                continue
            else:
                if not os.path.isfile("/Users/mirawelner/Documents/RecipePredictor/corpus/" + filename):
                    shutil.move(location + '/' + folder + '/' + filename,
                                "/Users/mirawelner/Documents/RecipePredictor/corpus")
                    print(word)
                continue
