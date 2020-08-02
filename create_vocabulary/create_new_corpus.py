original = open("kaggle_corpus.csv", "r")
new = open("new_corpus.txt", "w")
next(original)
for line in original:
    try:
        line = line[line.index('Ingredients,"')+len('Ingredients,"'):]
        line = line[:line.index('"')]
        new.write(line)
    except:
        continue
new.close()
