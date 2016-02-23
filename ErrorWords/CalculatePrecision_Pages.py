# -*- coding:utf-8 -*-
# 计算一个文件与另一个文件相比，得到准确率
# 两个文件的句子长度相同，找出区别

import codecs

def openFile(filename,mode):
	try:
		f=codecs.open(filename,mode,encoding="utf-8")
	except IOError as e:
		print "Unable to open the file ",filename,"\n",e
	else:
		return f



#比较两句话(tSent与sSent比较)，相同字的个数
def getSameWordNUM(sSent,tSent):
	difwordFilePath=r"F:\Laboratory\NLPbase_holidays\test_True.txt"
	difwordFile=openFile(difwordFilePath,"a+")
	if sSent!="":
		if tSent=="":
			print "Generation Sentence is empty"
			return 0
		elif len(sSent)!=len(tSent):
			print "There is an error that these sentences are different length."
			return 
		else:
			sameNum=0

			for i in range(len(tSent)):
				if sSent[i]==tSent[i]:
					sameNum+=1
				else:
					difwordFile.write("%d, %s,"%((i+1),tSent[i]))
			difwordFile.write("\n")
			print "All words: ",len(tSent)," The same words: ",sameNum," The different words: ",(len(tSent)-sameNum)
			return sameNum
	print "Raw sentence is empty!"
	return


def main():
	rightFilePath=r"F:\Laboratory\NLPbase_holidays\FinalTest_SubTask2_space.t2s"
	compareFilePath=r"F:\Laboratory\NLPbase_holidays\rightwords.output"
	rightFile=openFile(rightFilePath,"r")
	compareFile=openFile(compareFilePath,"r")

	rightline=rightFile.readline()
	compareline=compareFile.readline()
	sentAccur=0
	wordAccur=0
	allSent=0
	allWords=0
	while compareline and rightline:
		compareline=compareline[:-1].replace(" ","") #原句每个字用空格分割开了
		rightline=rightline[:-1].replace(" ","")
		allSent+=1
		if compareline==rightline:
			sentAccur+=1
		wordAccur+=getSameWordNUM(rightline,compareline)
		allWords+=len(rightline)
		rightline=rightFile.readline()
		compareline=compareFile.readline()

	sentPro=sentAccur*1.0/allSent
	wordPro=wordAccur*1.0/allWords

	print "Right sentences: ",sentAccur," --- All sentences: ",allSent
	print "Sentences are accurate: ",sentPro
	print "Right words: ",wordAccur," --- All words: ",allWords
	print "Words are accurate: ",wordPro


main()