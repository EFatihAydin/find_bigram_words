#import library
from functools import reduce
from collections import Counter
import re
import numpy as np
from TurkishStemmer import TurkishStemmer
stemmer = TurkishStemmer()

def clean(text):
	d = { "Ş":"ş", "İ":"i", "Ü":"ü", "Ç":"ç", "Ö":"ö", "Ğ":"ğ",  "I":"ı", "Î":"ı", "Û":"u", "Â":"a" , "â":"a" , "î":"ı" , "û":"u" }
	text = reduce( lambda x, y: x.replace( y,d[y] ),d,text )
	text = text.lower()
	text = re.sub('[^a-z0-9\sçışöğü]+', '', text)
	text = text.strip()
	return text

#req: convert text to nlp(TrukishStemmer is so bad)
def req(text):
    res = stemmer.stem(text)
    return res

def group_list(lst): 
    return list(zip(Counter(lst).keys(), Counter(lst).values()))

sw = open('stop_words.txt' , encoding = 'utf-8')
swliste = sw.readlines()
swliste = list(map(lambda x:x.strip(),swliste))

#create null list
words = []
liste = []
twwords = []

#create numbers list
numbers = ["0","1","2","3","4","5","6","7","8","9"]

#read all data and search keywords in every line 
for line in open("data.txt", encoding='utf-8'):
    text = clean(line)
    #text = req(text)
    text = text.replace("\n","")
    for word in text.split(" "):
        word = word.replace("\n","")
        if word not in liste: liste.append(word)
        for i in range(len(numbers)):
            if numbers[i] in word:
                word = "Not Word"
                break
        if word == "Not Word":continue
        if word in swliste:continue
        words.append(word)

#create a matrix
mrowname = dict([(k,v) for v,k in enumerate(liste)])
mcolname = dict([(k,v) for v,k in enumerate(liste)])

matris = [ [ 0 for mrow in range(len(liste)) ] for mcol in range(len(liste)) ]
matris_sentence = [ [ 0 for mrow in range(len(liste)) ] for mcol in range(len(liste)) ]

for line in open("data.txt", encoding='utf-8'):
    line = clean(line)
    line = line.split()
    for w in range(len(line)-1):
        matris[mrowname[line[w]]][mcolname[line[w+1]]] += 1
        for y in range(w+1,len(line)):
            matris_sentence[mrowname[line[w]]][mcolname[line[y]]] += 1

for i in range(len(liste)):
    for j in range(len(liste)):
        if matris_sentence[i][j] == 0:
            matris[i][j] = 0
        else:
            matris[i][j] = matris[i][j] / matris_sentence[i][j]

b = np.max(matris_sentence)
ortaliste = []
for i in range(len(liste)):
    for j in range(len(liste)):
    	matris_sentence[i][j] = matris_sentence[i][j]/b
    	if matris_sentence[i][j] != 0:
    		ortaliste.append(matris_sentence[i][j])
    	
orta = float(np.mean(ortaliste))

print("Writing bigram file...")
with open("bigram.txt", "w",encoding='utf-8') as fl:
	mylist = list(dict.fromkeys(words))
	for i in mylist:
		for j in mylist:
			twwords =  i + "_" + j
			oran = float(matris[mrowname[i]][mcolname[j]])
			total = float(matris_sentence[mrowname[i]][mcolname[j]])
			if oran > 0.8 and total>orta:fl.write(twwords+":"+str(oran)+":"+str(total)+"\n")
fl.close()