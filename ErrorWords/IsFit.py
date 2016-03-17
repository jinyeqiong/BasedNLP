# -*- coding:utf-8 -*-
#判断一个字转换为另一个字是否合理
#先找出两个文件的错字对，放入一个文件中

import string
from GetMaxEntropy_pinyin import *

ErrPairFilePath=r"F:\Laboratory\NLPbase_holidays\ErrorWords\ErrPairFile.err"
ErrPairFile=openFile(ErrPairFilePath,"a+")

def ExtractErrPair(line1,line2):
	lineList1=line1.split(" ");
	lineList2=line2.split(" ");
	count=0
	for i in range(len(lineList1)):
		if lineList1[i]!=lineList2[i]:
			print lineList1[i],lineList2[i]
			ErrPairFile.write("%s %s \n"%(lineList1[i],lineList2[i]))
			count+=1
	return count

def GetErrPairFile(hanziPairFilePath):
	hanziPairFile=openFile(hanziPairFilePath,"r")
	line1=hanziPairFile.readline() #正确句子
	count=0
	while line1:
		line2=hanziPairFile.readline() #错字句子
		count+=ExtractErrPair(line1,line2)
		line1=hanziPairFile.readline()
	print "All errPairs:",count
	hanziPairFile.close()
	ErrPairFile.close()


def testfuntion_isfit():
	line1=u"面 向 中 国"
	line2=u"走 向 韩 国"
	print getPinyin(line1)
	ExtractErrPair(line1,line2)

def runfuntion_isfit():
	pass


def main():
	hanziPairFilePath=r"F:\Laboratory\NLPbase_holidays\ErrorWords\test_hanzi_pair.hz"
	ErrPair_pinyinPath=r"F:\Laboratory\NLPbase_holidays\ErrorWords\ErrPair_pinyin.pinyin"
	GetErrPairFile(hanziPairFilePath)
	runfunction(ErrPairFilePath,ErrPair_pinyinPath,2,0,1,0)
#	testfuntion_isfit()

	print "Well Done ^_^"
main()