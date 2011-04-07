# coding=utf-8
from xml.dom import minidom
import codecs

g = codecs.open('list', 'at', 'utf-8')
f = codecs.open('../c5/dictionary.c5', 'at', 'utf-8')

#zamienia danego node'a na stringa ktory ma sie wypisac do pliku c5
def returnValue(node):
	if (len(node.childNodes) == 1) and (node.childNodes[0].nodeName == "quote"):
		node = node.childNodes[0]	
	return unicode(node.childNodes[0].nodeValue)


#znaczenie poszczegolnych funkcji:
#parseXxx(node) - parsuje noda z pliku xml o nazwie Xxx
#parseXxxYyy(node) - parsuje noda z pliku xml o nazwie Xxx i typie Yyy

def parseEntry(node):
	f.write("_____\n\n")
	parseForm(node.childNodes[0])
	start = 1
	if (node.childNodes[start].nodeName == "gramGrp"):
		parseGramgrp(node.childNodes[start])
		start = start + 1
	if (node.childNodes[start].nodeName == "usg"):
		f.write("(")
		parseUsg(node.childNodes[start])
		start = start + 1
		while node.childNodes[start].nodeName == "usg":
			f.write(", ")
			parseUsg(node.childNodes[start]) 
			start = start + 1 
		f.write(") ")	
	if node.childNodes[start].nodeName == "xr":
		f.write("(")
		parseXr(node.childNodes[start])
		start = start + 1 
		while node.childNodes[start].nodeName == "xr":
			f.write(", ")
			parseXr(node.childNodes[start]) 
			start = start + 1   
		f.write(")")
		
	f.write("\n")		
	idx = 1
	more = False
	if len(node.childNodes[start:]) > 1:
		more = True
	for node in node.childNodes[start:]:
		idx  = parseSense(node, idx, more)		
	f.write("\n")
			
def parseForm(node):
	g.write(returnValue(node.childNodes[0]) + "\n")
	f.write(returnValue(node.childNodes[0]) + "\n")
	f.write(returnValue(node.childNodes[0]) + " ")	
	start = 1  
	if (len(node.childNodes) > start) and (node.childNodes[start].nodeName == "orth"):
		f.write("(")
		orth = node.childNodes[start]
		start = start + 1
		if (len(node.childNodes) > start) and (node.childNodes[start].nodeName == "lang"):
			f.write(returnValue(node.childNodes[start]) + " ")
			start = start + 1
		f.write(returnValue(orth) + ") ")
	if (len(node.childNodes) > start):
		f.write("[" + returnValue(node.childNodes[start]))
		start = start + 1
		for n in node.childNodes[start:]:
			f.write(", " + returnValue(n))
		f.write("] ")
	
#idx mowi ktore z kolei znaczenie (sense) w danym hasle parsujemy
#more == True jesli w danym entry jest wiecej niz jedno sense
#idx bedzie wypisany do pliku c5 tylko jesli w danym hasle
#jest wiecej niz jedno sense, albo jesli jest jedno sense to zawiera
#w sobie przynajmniej dwa sense (w uproszczeniu idx wypisze sie jesli
#haslo ma przynajmniej dwa znaczenia)
def parseSense(node, idx, more):  
	start = 0
	while start < len(node.childNodes):
		f.write(" ")
		if ((len(node.childNodes) > 1) or more):
			f.write(str(idx) +". ") 
			idx = idx + 1 
	
		childNodes = node.childNodes	  
		if childNodes[start].nodeName == "gramGrp":
			parseGramgrp(childNodes[start])
			start = start + 1 
	
		if childNodes[start].nodeName == "form":
			f.write("(also ")
			form = childNodes[start]
			start = start + 1
			f.write(returnValue(form.childNodes[0]))
			if (len(form.childNodes) == 2):
				f.write(" [" + returnValue(form.childNodes[1]) + "]")
			f.write(") ")
	
		if (childNodes[start].nodeName == "xr"):
			parseXr(childNodes[start]) 
			start = start + 1
			while (childNodes[start].nodeName == "xr"): 
				f.write(", ")
				parseXr(childNodes[start])
				start = start + 1
			f.write(" = ")
		
		if (childNodes[start].nodeName == "usg"):
			f.write("(")
			parseUsg(childNodes[start])
			start = start + 1
			while (childNodes[start].nodeName == "usg"): 
				f.write(", ")
				parseUsg(childNodes[start])
				start = start + 1
			f.write(") ")

		parseInsideSense(childNodes[start])
		start = start + 1
		f.write("\n")

	return idx	   

def parseUsg(node):
	rest = ""
	if (node.childNodes[0].nodeName == "lang"):   
		if (len(node.childNodes) == 2):
			rest = unicode(node.childNodes[1].nodeValue)
		node = node.childNodes[0]
	f.write(returnValue(node) + rest)

#parsuje sense w srodku innego sense				
def parseInsideSense(node):
	start = 0
	if node.childNodes[start].nodeName == "form":
		f.write("(also ")
		form = node.childNodes[start]
		start = start + 1
		f.write(returnValue(form.childNodes[0]))
		f.write(") ")  
	
	if node.childNodes[start].nodeName == "usg":
		f.write("(")
		parseUsg(node.childNodes[start])
		start = start + 1
		if node.childNodes[start].nodeName == "usg":
			f.write(", ")
			parseUsg(node.childNodes[start])
			start = start + 1
		f.write(") ")
		
	while start < len(node.childNodes):
		childSense = node.childNodes[start]
		cit = childSense.childNodes[0]	
		parseCit(cit)
		child = cit.nextSibling		
		while child:
			f.write(", ")
			parseCit(child)
			child = child.nextSibling
		start = start + 1

def parseCitIdiom(node):
	f.write("idiom: ")
	f.write(returnValue(node.childNodes[0]))
	f.write( " = ");
	parseCitTrans(node.childNodes[2])
	start = 3
	while start < len(node.childNodes):
		f.write(", ")
		parseCitTrans(node.childNodes[start])
		start = start + 1	
	
#parsuje noda o nazwie cit i typie colloc lub noda o nazwie usg
def parseCitCollocOrUsg(node):	
	if (node.attributes["type"].value == "colloc"):
		cit = node
		quote = cit.childNodes[0]	
		f.write(returnValue(quote))	
		if (len(cit.childNodes) == 1):
			return		
		insideCit = cit.childNodes[1]	 					
		f.write(" = " + returnValue(insideCit))  	
		insideCit = insideCit.nextSibling
		while insideCit:
			f.write(", " + returnValue(insideCit))
			insideCit = insideCit.nextSibling
			
	else:
		usg = node
		f.write(returnValue(usg))		
	
def parseCitTrans(node):
	f.write(returnValue(node.childNodes[0]))
	if (len(node.childNodes) > 1):
		start = 1
		f.write(" (")
		while start < len(node.childNodes):
			parseCitCollocOrUsg(node.childNodes[start])
			if (node.childNodes[start].nextSibling):
				f.write(", ")
			start = start + 1
		f.write(")")

def parseCitExample(node):
	f.write(" (" + returnValue(node.childNodes[0]) + " = ")
	parseCitTrans(node.childNodes[1]) 
	sibling = node.childNodes[1].nextSibling
	while sibling:
		f.write(", ")
		parseCitTrans(sibling)
		sibling = sibling.nextSibling	
	f.write(")")

def parseCit(node):
	if (node.nodeName == "note"):
		f.write(returnValue(node))
		return
	elif (node.hasAttribute("type")) and (node.attributes["type"].value == "example"): 
		parseCitExample(node)   
	elif (node.hasAttribute("type")) and (node.attributes["type"].value == "trans"):
		parseCitTrans(node)
	elif (node.hasAttribute("type") and (node.attributes["type"].value == "idiom")):
		parseCitIdiom(node)
				
def parseXr(node):
	f.write(returnValue(node.childNodes[0]))

def parseGramgrp(node):
	if (not node.childNodes[0].hasChildNodes()) and (len(node.childNodes) == 1) :
		return;
	f.write("<")
	f.write(returnValue(node.childNodes[0]))
	for n in node.childNodes[1:]:
		f.write(", ")
		f.write(returnValue(n)) 
	f.write("> ")
					
dom = minidom.parse('dictionary.xml')
div = dom.getElementsByTagName("div")[0]
print "number of entries " + str(len(div.childNodes))
for entry in div.childNodes:
	parseEntry(entry)
