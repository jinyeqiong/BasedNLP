# -*- coding:utf-8 -*-

import random
import string
import codecs
import copy 
from baidu import *

yinSuPath=r"F:\Laboratory\NLPbase_holidays\ErrorWords\lex.f2e"
pyHanzipath=r"F:\Laboratory\NLPbase_holidays\ErrorWords\AllPinHan.txt"
drop_out=0.4

ranseed=random.randint(0,1000)*1.0/10000  #随机数种子，相当于进行了两次随机



def openFile(filename,mode):
	try :
		file=codecs.open(filename,mode,encoding='utf-8')
	except IOError as e :
		print "Unable to open the file ",filename,"\n",e
	else:
		return file


yinSuFile=openFile(yinSuPath,"r")
pyHanziFile=openFile(pyHanzipath,"r")

def Encode(sent,code): #原句的编码也改变了
	return sent.encode(code)

def Decode(sent,code): #原句的编码也改变了
	return sent.decode(code)


#得到语料库
def getYinSuList():
#	yinSuResultFile=r"F:\Laboratory\ErrorWords\ErrorWords\yinSu.txt"
#	yinsu=openFile(yinSuResultFile,'a+')
	yinSuDict={}
	line =yinSuFile.readline()
	valuelist=[]
	while line:
		linelist=str.split(Encode(line[:-1],'gbk')," ") #去掉后缀\r\n
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
		lineList=str.split(Encode(line[:-1],'gbk')," ")
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

#得到一个拼音的候选拼音
def getPYCandidates(pinyin):
	pinyinCanList=[]
	sheng,yun=getShengYun(pinyin)
#	print sheng ,yun 
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
#	for i in pinyinCanList:
#		print i,
#	print '\n'
	print pinyin,""
	return pinyinCanList

def ListToStr_space(sentList):
	spaceSent=''
	for word in sentList:
		spaceSent = spaceSent+word+" "
	spaceSent=spaceSent.rstrip()
	return spaceSent

#得到拼音句对
def GeneratePYSentPair(pinyinSentence):
	pySentencePairPath=r"F:\Laboratory\NLPbase_holidays\ErrorWords\pySentencePair.txt"
	pySentPair=openFile(pySentencePairPath,'a+')

	global ranseed
	PinyinPairList=[]
	pySentList=str.split(Encode(pinyinSentence,'gbk')," ")
	for index,pinyin in enumerate(pySentList):
		print "now pinyin :",pinyin
		ranseed+=1
		random.seed(ranseed)
		ran=random.uniform(0,10000)*1.0/10000
		print ran
		if ran > drop_out:
			dealSentList=copy.deepcopy(pySentList) #保证更改一个list，另一个list不变
			pyCanList=getPYCandidates(pinyin)
			for py in pyCanList:
				dealSentList[index]=py
				pySentPair.write(pinyinSentence)
				PinyinPairList.append(pinyinSentence)
				pySentPair.write("\n%s\n" % (ListToStr_space(dealSentList)))
				PinyinPairList.append(ListToStr_space(dealSentList))
			dealSentList=[]
			pySentPair.write('-------------------------------\n')
	print "Generate Pin-Pin finished!"
	return PinyinPairList


def TwoListToOneList(list1,list2): #汉字
	resultlist=[]
	for hi in list1:
		for hj in list2:
			resultlist.append(hi+" "+hj)
	return resultlist


#一句拼音对应的所有汉语句子
def PyToChinese(pinyinSentence):
	tempfile=r"F:\Laboratory\NLPbase_holidays\ErrorWords\tempFile.txt"
	temp=openFile(tempfile,"a+")
	chineseSentWithBDu=[]

	pySentList=str.split(Encode(pinyinSentence,'gbk')," ")
	pinyin=pySentList[0]
	nextpinyin=pySentList[1]
	#注：pinhanDic[pinyin] 是当只有一个拼音时
	groupList=TwoListToOneList(list(Decode(pinhanDic[pinyin],'gbk')),list(Decode(pinhanDic[nextpinyin],'gbk')))

	index=2
	while index<len(pySentList):
		nextpinyin=pySentList[index]
		groupList=TwoListToOneList(groupList,list(Decode(pinhanDic[nextpinyin],'gbk'))) 
		index+=1
	for line in groupList:
		print line 
#		print "Code: ",isinstance(line,unicode) #True
		
		#连接百度接口，查询句子正常出现的个数
		key=line.encode('gbk').replace(' ','')
		baiduCount=search(key)
		print "count:",baiduCount
		if baiduCount>10:
			print line
			temp.write("%s\n"%line)
			chineseSentWithBDu.append(line)
	return chineseSentWithBDu

#一句拼音，得到多个候选拼音句，然后又得到每个候选拼音句的所有汉语句子
def GeneratePHanSentPair(pinyinSentence):
	pinHanfile=r"F:\Laboratory\NLPbase_holidays\ErrorWords\pinHanSentPair.txt"
	pinHan=openFile(pinHanfile,"a+")

	pHanSentPair=[]

	pinyinPair=GeneratePYSentPair(pinyinSentence)
#	for i in pinyinPair:
#		print i

	count=1
	for pinyinSent in pinyinPair:
		if count%2==0: #偶数行
#			print count,pinyinSent
			chSentList=PyToChinese(pinyinSent)
			for chSent in chSentList:
#				print "Sentence:",chSent
				pinHan.write(pinyinPair[count-2])
				pHanSentPair.append(pinyinPair[count-2])
				pinHan.write("\n%s\n"%chSent)
				pHanSentPair.append(chSent)
			pinHan.write('-------------------------------\n')
		count+=1
	print "Generate Pin-Han finished!"
	return pHanSentPair


def GenerateHHanSentPair(pinyinSentence):
	hanHanfile=r"F:\Laboratory\NLPbase_holidays\ErrorWords\hanHanSentPair.txt"
	hanHan=openFile(hanHanfile,"a+")

	hHanSentPair=[]
	pinhanPair=GeneratePHanSentPair(pinyinSentence)
	count=1
	for pinhan in pinhanPair:
		if count%2==1: #奇数行
			chSentList=PyToChinese(pinhan) #得到原拼音的所有汉字候选
			for chSent in chSentList:
#				print chSent
				hanHan.write("%s\n" % chSent)
				hHanSentPair.append(chSent)
				hanHan.write("%s\n" % pinhanPair[count])
				hHanSentPair.append(pinhanPair[count])
			hanHan.write('-------------------------------\n')
		count+=1
	print "Generate Han-Han finished!"
	return hHanSentPair





def main():
#	GenerateHHanSentPair('wo3 xi3 huan1 du2 shu1')

#	GeneratePHanSentPair('wo3 xi3 huan1 du2 shu1')
	pinyinSent='wo3 xi3 huan1 du2 shu1'
	PyToChinese(pinyinSent)
	
#	s="我喜欢读书"
#	num=search(s.decode('utf-8').encode('gbk'))
#	print num
	print "Well Done!"






main()
