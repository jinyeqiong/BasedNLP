# -*- coding:utf-8 -*-
#将一个文件分成两个文件，奇数行一个文件，偶数行一个文件

import codecs

def openFile(filename,mode):
	try :
		file=codecs.open(filename,mode,encoding='utf-8')
	except IOError as e :
		print "Unable to open the file ",filename,"\n",e
	else:
		return file


def fileToFiles(rawFile,sourceFile,targetFile):
	rawline=rawFile.readline()
	count=1
	while rawline:
		if count%2==1: #奇数行
			sourceFile.write(rawline)
		if count%2==0: #偶数行
			targetFile.write(rawline)
		count+=1
		rawline=rawFile.readline()

#句子太短，将两行混为一行
def TwolinesToline(filePath,resultfile):
	file=openFile(filePath,"r")
	line=file.readline()
	count=1
	while line:
		if count%2==1:
			resultfile.write("%s "%line[:-2])
		if count%2==0:
			resultfile.write(line)
		count+=1
		line=file.readline()


def main():
	rawFilePath=r"F:\Laboratory\NLPbase_holidays\ErrorWords\test_hanzi_pair.hz"
	sourceFilePath=r"F:\Laboratory\NLPbase_holidays\ErrorWords\sourceSent.so"
	targetFilePath=r"F:\Laboratory\NLPbase_holidays\ErrorWords\targetSent.ta"
#	sFilePath=r"F:\Laboratory\NLPbase_holidays\ErrorWords\chinese.fr"
#	tFilePath=r"F:\Laboratory\NLPbase_holidays\ErrorWords\chinese.en"

	rawFile=openFile(rawFilePath,"r")
	sourceFile=openFile(sourceFilePath,"w")
	targetFile=openFile(targetFilePath,"w")
	fileToFiles(rawFile,sourceFile,targetFile)

#	sFile=openFile(sFilePath,"w")
#	tFile=openFile(tFilePath,"w")
#	TwolinesToline(sourceFilePath,sFile)
#	TwolinesToline(targetFilePath,tFile)
	
	print "Well Done ^_^"

main()
