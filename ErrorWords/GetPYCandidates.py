# -*- coding:utf-8 -*-

import random
import string

yinSuPath=r"F:\Laboratory\ErrorWords\ErrorWords\lex.f2e"
pyHanzipath=r"F:\Laboratory\ErrorWords\ErrorWords\AllPinHan.txt"
drop_out=0.4


def openFile(filename,mode):
	try :
		file=open(filename,mode)
	except IOError as e :
		print "Unable to open the file ",filename,"\n",e
	else:
		return file


yinSuFile=openFile(yinSuPath,"r")
pyHanziFile=openFile(pyHanzipath,"r")



def getYinSuList():
#	yinSuResultFile=r"F:\Laboratory\ErrorWords\ErrorWords\yinSu.txt"
#	yinsu=openFile(yinSuResultFile,'a+')
	yinSuDict={}
	line =yinSuFile.readline()
	valuelist=[]
	while line:
		linelist=str.split(line," ") #去掉后缀\r\n
		key =linelist[1]
		value =linelist[0]
		#value_num=linelist[2]
		if yinSuDict.has_key(key): 
			#yinSuDict[key]是字符串，i4 会显示在 ai4 中，但是应该不在其中
			if value not in valuelist:
			    valuelist.append(value)
			    #valuelist.append(value_num)
		else:
			valuelist=[]
			valuelist.append(value)
			#valuelist.append(value_num)
		yinSuDict[key]=valuelist
	
		line =yinSuFile.readline()

#	#生成中间文件，音素表
#	for key,value in yinSuDict.iteritems():
#		yinsu.write(key)
#		print key,
#		for v in value:
#			yinsu.write(" %s" % v)
#			print v,
#		yinsu.write('\n')
#		print '\n'

	return yinSuDict


def getPyHanzi():
	pyHanziDict={}
	line=pyHanziFile.readline()
	while line:								
		lineList=str.split(line," ")
		pyHanziDict[lineList[0]]=lineList[1]
		line=pyHanziFile.readline()
	return pyHanziDict


	
yinsuDic=getYinSuList()
pinhanDic=getPyHanzi()




def getShengYun(pinyin):
	# 声母表
	_INITIALS = 'b,p,m,f,d,t,n,l,g,k,h,j,q,x,zh,ch,sh,r,z,c,s,y,w'.split(',')
	sheng=''
	yun=''
	for i in _INITIALS:
		if pinyin.startswith(i):
			sheng=i
			yun=str.replace(pinyin,i,"")
			return sheng,yun
	if yun=='':
		yun=pinyin
	return sheng,yun


def getPYCandidates(pinyin):
	pinyinCanList=[]
	sheng,yun=getShengYun(pinyin)
	print sheng ,yun 
	if sheng!='':
#		print yinsuDic[sheng]
		for s in yinsuDic[sheng]:
			if s!='NULL':
				for y in yinsuDic[yun]:
					if (s+y) in pinhanDic:
#						print s+y,"*",
						pinyinCanList.append(s+y)
	for y in yinsuDic[yun]:
		if y in pinhanDic:
#			print y,"*",
			pinyinCanList.append(y)
	for i in pinyinCanList:
		print i,
	print '\n'
	return pinyinCanList



def GenerateSentPair(pinyinSentence):
	pySentencePairPath=r"F:\Laboratory\ErrorWords\ErrorWords\pySentencePair.txt"
	pySentPair=openFile(pySentencePairPath,'a+')
	pySentList=str.split(pinyinSentence," ")
	for index,pinyin in enumerate(pySentList):
		print "now pinyin :",pinyin
		ran=random.uniform(0,10)*1.0/10
		print ran
		if ran > drop_out:
			dealSentList=pySentList
			pyCanList=getPYCandidates(pinyin)
			for py in pyCanList:
				dealSentList[index]=py
				pySentPair.write(pinyinSentence)
				pySentPair.write("\n%s\n" % (ListToStr_space(dealSentList)))
			pySentPair.write('-------------------------------\n')


def ListToStr_space(sentList):
	spaceSent=''
	for word in sentList:
		spaceSent = spaceSent+word+" "
	return spaceSent


def main():

#	getPYCandidates("ou3")
	GenerateSentPair('wo3 xi3 huan1 du2 shu1')
	
	
#	sheng,yun=getShengYun('hou')
#	print sheng,"**",yun





main()
