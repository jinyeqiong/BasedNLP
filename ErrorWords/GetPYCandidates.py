# -*- coding:utf-8 -*-

import random
import string
import codecs
import copy 
from baidu import *

#语料库
yinSuPath=r"F:\Laboratory\NLPbase_holidays\ErrorWords\lex.f2e"
pyHanzipath=r"F:\Laboratory\NLPbase_holidays\ErrorWords\AllPinHan.txt"

#生成文件
pinyinPairfile=r"F:\Laboratory\NLPbase_holidays\ErrorWords\G_pySentencePair.txt" #生成拼音句对
pinHanfile=r"F:\Laboratory\NLPbase_holidays\ErrorWords\G_pinHanSentPair.txt" #生成拼音汉字句对
hanHanfile=r"F:\Laboratory\NLPbase_holidays\ErrorWords\G_hanHanSentPair.txt" #生成汉字汉字句对

#临时文件
hanzi_tempfile=r"F:\Laboratory\NLPbase_holidays\ErrorWords\GT_chineseFile.txt" #生成临时文件，存储一句拼音对应的所有汉字句
pinyinPair_tempfile=r"F:\Laboratory\NLPbase_holidays\ErrorWords\GT_pinYinPairFile.txt" #生成拼音对的临时文件（每一句原拼音得到的拼音对）
pinhanPair_tempfile=r"F:\Laboratory\NLPbase_holidays\ErrorWords\GT_pinHanPairFile.txt" #生成拼音汉字对的临时文件（每一句原拼音得到的拼音汉字对）
#hanhanPair_tempfile=r"F:\Laboratory\NLPbase_holidays\ErrorWords\GT_hanHanPairFile.txt" #生成汉字汉字对的临时文件

drop_out=0.4
ranseed=random.randint(0,1000)*1.0/10000  #随机数种子，相当于进行了两次随机



def openFile(filename,mode):
	try :
		file=codecs.open(filename,mode,encoding='utf-8')
	except IOError as e :
		print "Unable to open the file ",filename,"\n",e
	else:
		return file


#打开语料库
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
			pinyinCanList.append(y)
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
	pySentPair=openFile(pinyinPairfile,'a+') #生成拼音句对
	pySentPair_temp=openFile(pinyinPair_tempfile,'w') #生成临时文件
	global ranseed
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
				pySentPair_temp.write(pinyinSentence)
				pySentPair.write("\n%s\n" % (ListToStr_space(dealSentList)))
				pySentPair_temp.write("\n%s\n" % (ListToStr_space(dealSentList)))
			dealSentList=[]

	print "Generate Pin-Pin finished!"



def TwoListToOneList(list1,list2): #汉字
	resultlist=[]
	for hi in list1:
		for hj in list2:
			resultlist.append(hi+" "+hj)
	return resultlist


#一句拼音对应的所有汉语句子
def PyToChinese(pinyinSentence):
#	print isinstance(pinyinSentence,unicode)
	temp=openFile(hanzi_tempfile,"w") #生成临时文件，存储一句拼音对应的所有汉字句
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
#		print line 
#		print "Code: ",isinstance(line,unicode) #True

		#未连接百度接口
		temp.write(line)
		temp.write('\n')
		
		#连接百度接口，查询句子正常出现的个数
#		key=line.encode('gbk').replace(' ','')
#		baiduCount=search(key)
#		print "count:",baiduCount
#		if baiduCount>10:
#			print line
#			temp.write("%s\n"%line)
#			chineseSentWithBDu.append(line)
#	return chineseSentWithBDu

#一句拼音，得到多个候选拼音句，然后又得到每个候选拼音句的所有汉语句子
def GeneratePHanSentPair(pinyinSentence):
	pinHan=openFile(pinHanfile,"a+") #生成拼音汉字句对
	pinHan_temp=openFile(pinhanPair_tempfile,'w')
	GeneratePYSentPair(pinyinSentence)
	pinyinfile=openFile(pinyinPair_tempfile,'r')
	pinyin_current=pinyinfile.readline()
	count=1
	prePinyin=""
	while pinyin_current:
		pinyin_current=pinyin_current[:-1]
		if count%2==1: #奇数行
			prePinyin=pinyin_current
#			print "prePinyin:",prePinyin
		if count%2==0: #偶数行
#			print count,pinyinSent
			PyToChinese(pinyin_current)
			hanzifile=openFile(hanzi_tempfile,'r')
			hanzi=hanzifile.readline()
#			print "hanzi:",hanzi
			while hanzi:
				pinHan.write('%s\n'%prePinyin)
				pinHan_temp.write('%s\n'%prePinyin)
				pinHan.write('%s\n'%hanzi[:-1])
				pinHan_temp.write('%s\n'%hanzi[:-1])
				hanzi=hanzifile.readline()
		count+=1
		pinyin_current=pinyinfile.readline()
	print "Generate Pin-Han finished!"



def GenerateHHanSentPair(pinyinSentence):
	hanHan=openFile(hanHanfile,"a+") #生成汉字汉字句对
	GeneratePHanSentPair(pinyinSentence)
	pinhanPairFile=openFile(pinhanPair_tempfile,'r')
	pinhan=pinhanPairFile.readline()
	count=1
	nextHanzi=""
	while pinhan:
		pinhan=pinhan[:-1]
		if count%2==0: #偶数行
			nextHanzi=pinhan 
		if count%2==1: #奇数行
			PyToChinese(pinhan)
		if nextHanzi!="":
			allhanzifile=openFile(hanzi_tempfile,'r')
			allhanzi=allhanzifile.readline()
			while allhanzi:
				hanHan.write('%s\n'%allhanzi[:-1])
				print "hanzi:",allhanzi[:-1]
				hanHan.write('%s\n'%nextHanzi)
				print "nextHanzi:",nextHanzi
				allhanzi=allhanzifile.readline()
			nextHanzi=""
		count+=1
		pinhan=pinhanPairFile.readline()
		
	print "Generate Han-Han finished!"






def main():
	GenerateHHanSentPair('wo3 xi3 huan1 du2 shu1')

#	GeneratePHanSentPair('wo3 xi3 huan1 du2 shu1')
#	pinyinSent='wo3 xi3 huan1 du2 shu1'
#	PyToChinese(pinyinSent)
	
	#测试百度接口
#	s="我喜欢读书"
#	num=search(s.decode('utf-8').encode('gbk'))
#	print num
	print "Well Done!"






main()
