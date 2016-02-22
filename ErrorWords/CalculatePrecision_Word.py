# -*- coding:utf-8 -*-
# 针对具体问题所写，知道平行语料和正确形式就可以得到准确率
# 得到错别字还原的格式，并与正确文件对比得到准确率


import codecs

def openFile(filename,mode):
	try:
		f=codecs.open(filename,mode,encoding="utf-8")
	except IOError as e:
		print "Unable to open the file ",filename,"\n",e
	else:
		return f


# 生成相应格式
def generateForm(rightFile,compareFile,genFile):
	rightline=rightFile.readline()
	compareline=compareFile.readline()
	sentnum=0
	while compareline and rightline:
		compareline=compareline[:-1].replace(" ","") #原句每个字用空格分割开了
		rightline=rightline[:-1].replace(" ","")
		sentnum+=1
		if compareline!=rightline:
			if len(compareline)!=len(rightline):
				print "There is an error that these sentences are different length."
				return 
			else:
				for i in range(len(compareline)):
					if rightline[i]!=compareline[i]:
						genFile.write("%d, %s, "%((i+1),compareline[i]))

		genFile.write("\n")
		
		rightline=rightFile.readline()
		compareline=compareFile.readline()

# 计算正确数量等(返回所有正词总数，识别改正的词数，识别对改错的词数，识别错了的词数)
def calAccur(rightForm,genFile):
	allright=0
	rego_fixright=0
	rego_fixwrong=0
	regowrong=0

	rightline=rightForm.readline()
	genline=genFile.readline()
	while rightline:
		rightlist=str.split(rightline[:-1].encode('gbk'),", ")
		genlist=str.split(genline[:-3].encode('gbk'),", ")

		allright+=(len(rightlist)-1)/2
		if len(genlist)!=0:
			for g in range(0,len(genlist),2):
				if genlist[g] in rightlist:
					pos=rightlist.index(genlist[g]) #出现的位置
					if rightlist[pos+1]==genlist[g+1]:
#						print rightline,"===",rightlist[pos+1]
						rego_fixright+=1
					else:
						rego_fixwrong+=1
				else:
					regowrong+=1
		rightline=rightForm.readline()
		genline=genFile.readline()

	return allright,rego_fixright,rego_fixwrong,regowrong


def run_genForm():
	rightFilePath=r"F:\Laboratory\NLPbase_holidays\FinalTest_SubTask2_space.t2s" #正确的文件
	compareFilePath=r"F:\Laboratory\NLPbase_holidays\rightwords.output" #得到的结果文件
	difwordFilePath=r"F:\Laboratory\NLPbase_holidays\test_True.txt" #生成格式文件
	rightFile=openFile(rightFilePath,"r")
	compareFile=openFile(compareFilePath,"r")
	difwordFile=openFile(difwordFilePath,"w")
	generateForm(rightFile,compareFile,difwordFile)
	difwordFile.close()
	compareFile.close()
	rightFile.close()

def run_calAccur():
	difwordFilePath=r"F:\Laboratory\NLPbase_holidays\test_True.txt" #生成格式文件
	rightFormFilePath=r"F:\Laboratory\NLPbase_holidays\FinalTest_SubTask2_Truth.t2s"

	rightFormFile=openFile(rightFormFilePath,"r")
	difwordFile=openFile(difwordFilePath,"r")

	allright,rego_fixright,rego_fixwrong,regowrong=calAccur(rightFormFile,difwordFile)

	print "All right words: ",allright
	print "Recogonize and fix right words: ",rego_fixright
	print "Recogonize and fix wrong words: ",rego_fixwrong
	print "Recogonize wrong words: ",regowrong
	print "Precision: ",rego_fixright*1.0/allright

	difwordFile.close()
	rightFormFile.close()


def main():
	run_genForm()
	run_calAccur()

	print "Well Done ^_^"

main()