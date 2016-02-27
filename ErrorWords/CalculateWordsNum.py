# -*- coding: utf-8 -*-
#计算一篇文章字的频率
# 将 拼音汉字表 进行升级，按字的常用频率进行重排

import codecs

handleFilePath=r"F:\Laboratory\NLPbase_holidays\ErrorWords\devset.e"
wordFrequencyFilePath=r"F:\Laboratory\NLPbase_holidays\ErrorWords\wordFrequency.txt"

def openFile(filename,mode):
    try :
        f=codecs.open(filename,mode,encoding='utf-8')
    except IOError as e :
        print "Unable to open the file ",filename,"\n",e
    else:
        return f


def is_chinese(uchar):
        """判断一个unicode是否是汉字"""
        if uchar >= u'\u4E00' and uchar <= u'\u9FA5':
            return True
        else:
            return False
 
def count_chinese_word(handleFilePath):
    handleFile=openFile(handleFilePath,"r")
    _dict = {}
    line=handleFile.readline()
#    print isinstance(line,unicode)
    while line:
#        print line
        for uchar in line :
#            print uchar
            if is_chinese(uchar):
                if _dict.has_key(uchar):
                    _dict[uchar] = _dict[uchar] + 1
                else:
                    _dict[uchar] = 1
        line=handleFile.readline()
    handleFile.close()
    return _dict
 
dic=count_chinese_word(handleFilePath)



#将一字符串按频率从大到小排序，去掉频率低（<10）的字，返回排序后的字符串
def orderStr(longwords):
    result=""
    fre_dict={}
    for char in longwords:
        if char in dic and dic[char]>=10: #常用字显示
            fre_dict[char]=dic[char]
        else:
            fre_dict[char]=0
    orderlist=sorted(fre_dict.items(), key=lambda d:d[1] ,reverse=True)
    for k in orderlist:
        if k[1]!=0:
            result=result+k[0]  # +str(k[1])
            print k[0]
#        else:
#            result=result+"---"+k[0]

    return result


def runfunction():
    wordFrequencyFile=openFile(wordFrequencyFilePath,"w")
    for k,v in dic.iteritems():
        print k," , ",v
        wordFrequencyFile.write("%s %d\n"%(k,v))
    wordFrequencyFile.close()

    pinHanFilePath=r"F:\Laboratory\NLPbase_holidays\ErrorWords\AllPinHan.txt"
    reorderPinHanFilePath=r"F:\Laboratory\NLPbase_holidays\ErrorWords\reorder_pinhan.txt"
    pinHanFile=openFile(pinHanFilePath,"r")
    reorder_PinHanFile=openFile(reorderPinHanFilePath,"w")
    line=pinHanFile.readline()
    while line:
        print line
        linelist=str.split(line[:-1].encode('gbk')," ")
        reorder_PinHanFile.write("%s %s\n"%(linelist[0].decode('gbk'),orderStr(linelist[1].decode('gbk'))))
        line=pinHanFile.readline()
    pinHanFile.close()
    reorder_PinHanFile.close()




def testfunction():
    s=u"被备背辈倍贝蓓惫悖狈焙邶钡孛碚褙鐾鞴"
    line=orderStr(s)
    print line


if __name__ == '__main__':
#    testfunction()
    runfunction()
    print "Well Done ^_^"