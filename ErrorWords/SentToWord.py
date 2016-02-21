# -*-coding:utf-8 -*-
# 将一句话中的每个字分开

import codecs

def openFile(filename,mode):
	try:
		file=codecs.open(filename,mode,encoding="utf-8")
	except IOError as e:
		print "Unable to open the file ",filename,"\n",e
	else:
		return file



#将一句话的每个字分开
def sepOneSent(sentence):
	resultSent=""
#	sentence=sentence[:-1] #结尾只有一个换行符（LF）或一个回车符（CR）
	sentence=sentence[:-2] #结尾既有一个换行符（LF），又有一个回车符（CR）
	sentlist=list(sentence)
	for s in sentlist:
		resultSent=resultSent+s+" "
	resultSent=resultSent.replace("  "," ").replace("  "," ")

	return resultSent


def runFuntion():
	sourceFilePath=r"F:\Laboratory\NLPbase_holidays\ErrorWords\merge_all_sentence.t2s"
	targetFilePath=r"F:\Laboratory\NLPbase_holidays\ErrorWords\merge_all_sentence_sep.t2s"
	sourcefile =openFile(sourceFilePath,"r")
	targetfile =openFile(targetFilePath,"w")
	line =sourcefile.readline()
	count=0
	while line:
		count+=1
		sepline=sepOneSent(line)
		targetfile.write("%s\n"%sepline.lstrip())
		if count%100==0:
			print "-----------------Have Finished ",count ," rows!-----------------"
		line=sourcefile.readline()
	print "All rows are ",count


def main():
	runFuntion()

	print "Well Done ^_^"

main()