# -*- coding:utf-8 -*-

import string
import codecs

def openFile(filename,mode):
	try :
		file=codecs.open(filename,mode,encoding='utf-8')
	except IOError as e :
		print "Unable to open the file ",filename,"\n",e
	else:
		return file


def longToShort(sentence):
	shortFilePath=r"F:\Laboratory\NLPbase_holidays\ErrorWords\shorttest.en"
	shortfile=openFile(shortFilePath,'a+')
	strlist=str.split(sentence," ")
	print strlist
	if len(strlist)<=10:
		shortfile.write(sentence)
		print sentence
	elif len(strlist)>10:
		sa=""
		for i in range(10):
			sa=sa+strlist[i]+" "
		shortfile.write("%s\n"%sa)
		num=10
		sb=""
		while num<len(strlist):
			sb=sb+strlist[num]+" "
		shortfile.write("%s\n"%sb)

def main():

#	a="yi1 er4 yve4 san1 yi1 ri4 "
#	longToShort(a[:-1])


	filePath=r"F:\Laboratory\NLPbase_holidays\ErrorWords\test.en"
	pyfile=openFile(filePath,"r")

	line=pyfile.readline()
	while line:
		print line
		line=line[:-2].encode('gbk')
		longToShort(line)
		line=pyfile.readline()

	pyfile.close()



main()
