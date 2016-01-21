# -*- coding: utf-8 -*-  
#!/usr/bin/env python  
#抓取百度搜索结果  
import sys  
import re   
import urllib2  
  
from bs4 import BeautifulSoup  

#注意：key要是gbk编码
def search(key):  
    search_url='http://www.baidu.com/s?wd=key&rsv_bp=0&rsv_spt=3&rsv_n=2&inputT=6391'   
    req=urllib2.urlopen(search_url.replace('key',key))   
    result=[]    
    num_em=0
    #循环抓取10页结果进行解析  
#    for count in range(10):  
    html=req.read()  
    soup=BeautifulSoup(html,'lxml')  

    file = open("result.txt",'a')  
      
    content  = soup.findAll('h3',attrs={"class":"t"})

    print content
    num = len(content)  
#        print "num:",num
    
    for i in range(num):  
        emContent=content[i].findAll('em')
        for e in emContent:
            print "==========text:",e.string
            print "==========len(e.string)",len(e.string)
            if e.string.encode('gbk') in key and len(e.string)!=1:
                file.write(e.string.encode('utf-8'))
                file.write('\n')
#                    print "e in key , OK!!!"
                num_em+=1
#            else: #过滤的太暴力啦~
#                return 0
#            print '------------------------------------'
#        print "num_em:",num_em

       #file.close()  
        #解析下一页  
#        next_page='http://www.baidu.com'+soup('a',{'href':True,'class':'n'})[0]['href'] # search for the next page  
#        header='www.baidu.com'
#        req=urllib2.urlopen(next_page,header)  
    return num_em   
        
if __name__=='__main__':  
    key=raw_input('input key word:')  
    search(key)  