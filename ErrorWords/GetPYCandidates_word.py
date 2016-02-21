# -*-coding:utf-8 -*-
# 一个字一个字处理，不是整个句子一起处理

import random
import string
import codecs
import re
from pypinyin import pinyin,lazy_pinyin,load_single_dict,TONE2
import pypinyin


ranseed=random.randint(0,1000)*1.0/10000  #随机数种子，相当于进行了两次随机
drop_out=0.1

DIGITAL=['0','1','2','3','4','5','6','7','8','9']

#语料库
yinSuPath=r"F:\Laboratory\NLPbase_holidays\ErrorWords\lex.f2e"
pyHanzipath=r"F:\Laboratory\NLPbase_holidays\ErrorWords\AllPinHan.txt"


#优化拼音工具 (运行一次即可)
def tunepypinyin():
	load_single_dict({ord(u'的'):u'de0,di2'})
	load_single_dict({ord(u'得'):u'de2,dei3,de0'})
	load_single_dict({ord(u'了'):u'le0,liao3'})



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
		if len(lineList[1])!=0:
			pyHanziDict[lineList[0]]=lineList[1]
		line=pyHanziFile.readline()
	return pyHanziDict


	
yinsuDic=getYinSuList()
pinhanDic=getPyHanzi()


#得到一句汉字的拼音
def getPinyin(word):
    pinyin =pypinyin.slug(word,style=pypinyin.TONE2) #多音字的没弄！
    pinyin=pinyin.replace("-"," ").replace("  "," ").replace("  "," ")
    return pinyin

#将拼音标注同一化！ a1ng=>ang1
#遇到数字将数字放在字符串末尾
def numToEnd(str ):
    strlist=list(str)
    k=-1
    for i in range(len(str)):
        if strlist[i].isdigit():
            k=i
    if k==-1: #如果没有拼音数字，说明是轻声
       result=str+"0"
        
    else:
        num =strlist[k]  
        while k!=len(str)-1:
            strlist[k]=strlist[k+1]
            k+=1
        strlist[k]=num
        result=('').join(strlist) #将list转为字符串
    return result

#对于一句汉语句子，去除标点
def delPunctuation(sentence):
	sentence=re.sub("[．·]".decode('utf-8'), "".decode('utf-8'),sentence)
	sentence_pun = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%‰……&*（）【】《》％：“”『』；‘’／]+".decode('utf-8'), " ".decode('utf-8'),sentence).replace("  "," ").replace("  "," ")
	if sentence_pun.startswith(" "):
		sentence_pun=sentence_pun[1:]
	return sentence_pun

#将list中连续的数字组合成一个数字
def combineNumbers(strlist):
	resultList=[]
	number=""
	for i in strlist:
		if i[0] in DIGITAL:
			number=number+i
		elif number!="":
			resultList.append(number)
			number=""
		if i[0] not in DIGITAL:
			resultList.append(i)
	return resultList
#
#输入：一个汉字句子 输出：汉字句子list，拼音句子list
def getHPSentList(cnSentence_punc):
#	print isinstance(chinsesSentence,unicode) #True
	print cnSentence_punc,isinstance(cnSentence_punc,unicode) #True
	#将汉字转为拼音
	pySent=getPinyin(cnSentence_punc)
	#将拼音、汉字空格，形成单独的字，放在list中
	#对于数字处理，12->1 2，这种是不要的

	cnList_temp=list(cnSentence_punc.replace(" ",""))
	cnSentList=combineNumbers(cnList_temp)
	pyList_temp=str.split(Encode(pySent[:-1],'gbk')," ")
#	print "=====:",pySent[:-1],'\n',Encode(pySent[:-1],'gbk')
	pySentList=combineNumbers(pyList_temp)
	print cnSentList
	print pySentList
	return cnSentList,pySentList



def getShengYun(pinyin):
	# 声母表
	_INITIALS = 'b,p,m,f,d,t,n,l,g,k,h,j,q,x,zh,ch,sh,r,z,c,s,y,w'.split(',')
	sheng=''
	yun=''
	for i in _INITIALS:
		if pinyin.startswith(i):
			sheng=i
			yun=str.replace(pinyin,i,"",1) #只替换一次
			return sheng,yun
	if yun=='':
		yun=pinyin
	return sheng,yun


#得到一个拼音的候选拼音
def getPYCandidates(pinyin):
	pinyinCanList=[]
	sheng,yun=getShengYun(pinyin)
#	print sheng ,yun 
	if sheng!='' and sheng in yinsuDic:
#		print yinsuDic[sheng]
		for s in yinsuDic[sheng]:
			if s!='NULL':
				if yun in yinsuDic:
					for y in yinsuDic[yun]:
						if (s+y) in pinhanDic:
	#						print s+y,"*",
							pinyinCanList.append(s+y)
				else:
					if (s+yun) in pinhanDic:
	#					print s+yun,"*",
						pinyinCanList.append(s+yun)
	if yun in yinsuDic:
		for y in yinsuDic[yun]:
			if y in pinhanDic:
				pinyinCanList.append(y)
	if len(pinyinCanList)==0: #没有拼音候选
		pinyinCanList.append(pinyin)

	pinyinCanList=list(set(pinyinCanList)) #去重
	pinyinCanList.insert(0,pinyin) #加入原拼音
#	print pinyinCanList
	return pinyinCanList

#随机得到list中的一个值的位置,list中开始位置begin
def getListRandom(llist,begin=0):
	length=len(llist)
	pos=random.randint(begin,length-1)
#	print "now the pos:",pos
	return pos

#filePath=r"F:\Laboratory\NLPbase_holidays\ErrorWords\probability.pro"
#file1=openFile(filePath,"a+")
#随机得到一个拼音的一个拼音候选
def getCanPy(pinyin):
	pyCandidate=getPYCandidates(pinyin)
	ra=random.uniform(0,1)
	print "pinyin random:",ra
#	file1.write("%s pinyin random:%f\n"%(pinyin,ra))
	if ra>=drop_out:
		return pinyin
	else:
		pyPos=getListRandom(pyCandidate)
#		print "PYCandidate:",pyCandidate[pyPos]
		return pyCandidate[pyPos]

#得到一个拼音的随机一个汉字候选
def getCanHz(pinyin):
#	print "++++++++++++++",isinstance(pinhanDic[pinyin],str)
	hanziCan=list(pinhanDic[pinyin].decode('gbk')) #得到候选汉字列表
#	print "HanZiCandidate:",hanziCan
	#得到原来的那个字

	ra=random.uniform(0,1)
	print "hanzi random:",ra
#	file1.write("%s hanzi random:%f\n"%(pinyin,ra))
	if ra>=drop_out:
		hzPos=0
	else:
		hzPos=getListRandom(hanziCan)
	return hanziCan[hzPos]

#处理一句拼音句，得到一个随机候选汉字句
#如果拼音没有对应的汉字，那就将原字复制过来，如：辞 ci0
def getHzSent(cnSentList,pySentList):
	hzSent=""
	for index, pinyin in enumerate(pySentList):
		if pinyin[0] in DIGITAL:
#			print pinyin
			hzSent=hzSent+cnSentList[index]+" "
		else:
			pinyin=numToEnd(pinyin)
			print "Now the pinyin :",pinyin
			pyCan=getCanPy(pinyin)
			print "Now the Candidate of PY:",pyCan
			if pyCan not in pinhanDic: #没有拼音候选
				hzSent=hzSent+cnSentList[index]+" "
			elif pyCan==pinyin: #随机得到的拼音候选和原拼音相同,得到原先的那个字
				hzSent=hzSent+cnSentList[index]+" "
			else:
				hzCan=getCanHz(pyCan)
#				print "Now the Candidate of HZ:",hzCan
				hzSent=hzSent+hzCan+" "
#	print "HZSentence:",hzSent
	return hzSent


#对于一句拼音，得到k句汉字句候选
def getKCanSents(cnSentList,pySentList,k=10):
	sentList=[]
	count=0
	while count<k:
		sentList.append(getHzSent(cnSentList,pySentList))
		global ranseed
		ranseed+=1
		count+=1
	return sentList

def runfunction():
	sourceFilePath=r"F:\Laboratory\NLPbase_holidays\ErrorWords\test.hz"
	HanZipath=r"F:\Laboratory\NLPbase_holidays\ErrorWords\test_hanzi.hz"
	HanZiPairPath=r"F:\Laboratory\NLPbase_holidays\ErrorWords\test_hanzi_pair.hz"


	sourceFile=openFile(sourceFilePath,"r")
	HanZi=openFile(HanZipath,"a+")
	HanZiPair=openFile(HanZiPairPath,"a+")

	cnsentence=sourceFile.readline()
	count=1
	while cnsentence:
		cnsentence=cnsentence[:-3]
		print "RawSentence:",cnsentence
		print isinstance(cnsentence,unicode) #True
		cnsent_nopunc=delPunctuation(cnsentence)

		cnSentList,pySentList=getHPSentList(cnsent_nopunc)
		candidate=getKCanSents(cnSentList,pySentList)
		print "------------------Results------------------"
		for s in candidate:
			HanZi.write("%s\n"%s)

			HanZiPair.write("%s\n"%cnsent_nopunc.replace(" ",""))
			HanZiPair.write("%s\n"%s.replace(" ",""))
			print s
		HanZi.write("=========================================\n")

		if count%100==0:
			print "Finished ",count," rows ^_^"
			HanZi.write("Finished %d rows ^_^ \n"%count)
			HanZi.write("=========================================\n")
		count+=1
		cnsentence=sourceFile.readline()









def testfunction():
#	print getShengYun("qvan2")
#	print getPYCandidates("qvan2")

	s=u"冷空气 前锋 过 后 上述 地区 的 气温 将 下降 6—12 摄氏度 ； "
	cnsent_nopunc=delPunctuation(s)
	c,p=getHPSentList(cnsent_nopunc)
	print "------------------Results------------------"
	for i in c:
		print i,
	print "\n"
	for j in p:
		print j,

def main():

#	print getPinyin(u"了")
	runfunction()

#	testfunction()

	print "Well Done!"


main()
