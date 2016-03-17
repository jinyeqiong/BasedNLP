# -*-coding:utf-8 -*-
# 通过训练语料得到拼音句子，声母、韵母分开的
# 原文件格式 1 张 场 例句
# eg. 1 zh ang ch ang （张-场）

import codecs
import string
from pypinyin import pinyin,lazy_pinyin,load_single_dict,TONE2
import pypinyin

def openFile(filename,mode):
	try:
		fi=codecs.open(filename,mode,encoding="utf-8")
	except IOError as e:
		print "Unable to open the file ",filename,"\n",e
	else:
		return fi

#将一行字符串的形式改变，只得到前n列
def deleteSentence(line,n):
	resultList=[]
	lineList=line.split(" ")
	i=0
	while i<n:
		resultList.append(lineList[i])
		i+=1
	return resultList

#得到一句汉字的拼音
def getPinyin(word):
    pinyin =pypinyin.slug(word,style=pypinyin.TONE2) #多音字的没弄！
    pinyin=pinyin.replace("-"," ").replace("  "," ").replace("  "," ")
#    print pinyin
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
		sheng="Null"
		yun=pinyin
	return sheng,yun

#将汉字转为拼音，并且声韵母分开
#列数从0开始
def hanziToPinyin(sentList,begincol,endcol,isFlag): #sentList 的二三列是字 begincol=1,endcol=2 (0、1、2)
	resultList=[]
	if isFlag:#是否有标记，即是否写第一列（标签）
		resultList.append(sentList[0])
	i=begincol
	while i<=endcol:
		pinyin=numToEnd(getPinyin(sentList[i]))
		sheng,yun=getShengYun(pinyin.encode("gbk"))
		resultList.append(sheng)
		print "sheng:",sheng
		resultList.append(yun)
		print "yun:",yun
		i+=1
	result=""
	for r in resultList:
		result=result+r+" "
	#return result[:-1] #去掉最后一个空格
	return result

def runfunction(rawFileName,maxEnFilePath,fircols,begincol,endcol,isFlag):
	sentFile=openFile(rawFileName,"r")
	maxEnFile=openFile(maxEnFilePath,"w")
	line=sentFile.readline()
	print line
	while line:
		#去掉例句列
		sentenceList=deleteSentence(line,fircols)
		#将汉字变为拼音(声韵母分开)
		pinyinSent=hanziToPinyin(sentenceList,begincol,endcol,isFlag)
		print pinyinSent
		maxEnFile.write("%s\n" % pinyinSent)
		line=sentFile.readline()

def testfunction():
	s=u"我喜欢读书"
	a=getPinyin(s)
	print a


if __name__=='__main__':
	filePath=r"F:\Laboratory\NLPbase_holidays\ErrorWords\2.txt"
	maxEnFilePath=r"F:\Laboratory\NLPbase_holidays\ErrorWords\maxEn_pinyin2.txt"
	
#	filePath=r"/home/xuexin/workspace/Laboratory/MaxEntSentiment_ErrorWords/xx/2.txt"
#	maxEnFilePath=r"/home/xuexin/workspace/Laboratory/MaxEntSentiment_ErrorWords/xx/dev.txt"
	
	fircols=3 #截取前几列
	begincol=1 #从第begincol列开始，汉字转为拼音
	endcol=2 #到第endcol列结束，转换结束
	isFlag=1 #不写标签（0）；写（1）

	runfunction(filePath,maxEnFilePath,fircols,begincol,endcol,isFlag)
#	testfunction()

	print "Well Done ^_^"
