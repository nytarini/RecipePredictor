original = open("kaggle_corpus.csv", "r")
new = open("new_corpus.txt", "w")
next(original)
for line in original:
    if line.find('Ingredients,"') is not -1:
        line = line[line.index('Ingredients,"') + len('Ingredients,"'):]
    if line.find('"') is not -1:
        line = line[:line.index('"')]
    if line.find('Volume: 1') is not -1:
        line = line[:line.index('Volume: 1')]
    if line.find('Allergy Information:') is not -1:
        line = line[:line.index('Allergy Information:')]
    if line.find('Contains') is not -1:
        line = line[:line.index('Contains')]
    new.write(line + '\n')

new.close()
