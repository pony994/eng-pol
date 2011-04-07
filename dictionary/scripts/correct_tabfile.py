oldTabfile = open("../stardict/dictd_www.dict.org_eng-pol.txt")
newTabfile = open("../stardict/eng-pol.txt", "w")
list = open("list")

#poprawia bledy programu dictd2dic

#przeczytanie poczatkowego naglowka i pominiecie go
for i in range(4):
	oldTabfile.readline()

words = {}

middles = {}

for line in oldTabfile:
	word = None
	rest = None
	#obliczenie dlugosci slowa 
	wordlen = len(line.split("\t")[0].split(" "))
	l = line.split("\t")[1].split("\\n\\n")[0]
	w = l.split(" ")[:wordlen]
	word = " ".join(w)
	r = l.split(" ")[wordlen:]
	rest = " ".join(r)
	middle = " "
	if not word:
		middle = "\\n"
		word = line.split("\t")[0]
		
	words[word] = rest
	middles[word] = middle		
		
	s = line.split("\t")[1].split("\\n\\n")
	for i in s[1:]:
		word = i.split(" ")[0].split("\\n")[0]
		words[word] = i
	

last = ""	
for line in list:
	#pozbycie sie \n z konca slowa
	word = line.split("\n")[0]
	wordCopy = word
	if not word in words:
		wordCopy = word + "\\n" 
		
	if wordCopy in middles:
		newTabfile.write(last + word + "\t" + wordCopy + middles[wordCopy] + words[wordCopy])
	else:
		newTabfile.write(last + word + "\t" + words[wordCopy])
		
	if words[wordCopy][len(words[wordCopy]) - 1] == "\n":
		last = ""
	else:
		last = "\n"
	
	

