# -*- coding:utf-8 -*-

import codecs
import string

def openFile(filename,mode):
	try:
		file=open(filename,mode)
	except IOError as e:
		print "Unable to open the file ",filename,"\n",e
	else:
		return file

def fileToDict(file):
	dic={}
	line=file.readline()
	while line:
		lineList=str.split(line," ")
		dic[lineList[0]]=lineList[1]
#		print lineList[0]," ",lineList[1]
		line=file.readline()
	return dic

def matchDict(file,sourceDic,targetDic,filename):
	resultFile=openFile(filename,"w")
	line=file.readline()
	while line:
		lineList=str.split(line," ")
		resultFile.write("%d "% string.atoi(lineList[0]))
		if string.atoi(lineList[0])!=0:
			print sourceDic[lineList[0]]
			resultFile.write(sourceDic[lineList[0]])
		resultFile.write(" %d "% string.atoi(lineList[1]))
		resultFile.write(targetDic[lineList[1]])
		resultFile.write(" %f \n"%string.atof(lineList[2]))
		line=file.readline()


def main():
	sourceFilePath=r"/home/xuexin/workspace/Tsinghua/giza-pp/TEST/f2e.trn.src.vcb"
	targetFilePath=r"/home/xuexin/workspace/Tsinghua/giza-pp/TEST/f2e.trn.trg.vcb"
	finalFilePath=r"/home/xuexin/workspace/Tsinghua/giza-pp/TEST/f2e.t3.final"
	resultFilePath=r"/home/xuexin/workspace/Tsinghua/giza-pp/TEST/result.txt"
	sourceFile=openFile(sourceFilePath,"r")
	targetFile=openFile(targetFilePath,"r")
	finalFile=openFile(finalFilePath,"r")
	
	print "Import Succeed!\n"
	sourceDic=fileToDict(sourceFile)
	print "sourceDic succeed!\n"
	targetDic=fileToDict(targetFile)
	print "targetDic succeed!\n"

	matchDict(finalFile,sourceDic,targetDic,resultFilePath)

main()
