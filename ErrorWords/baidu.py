# coding=utf8
import urllib2
import string
import urllib
import re
import random
 
#设置多个user_agents，防止百度限制IP
user_agents = ['Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20130406 Firefox/23.0', \
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:18.0) Gecko/20100101 Firefox/18.0', \
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533+ \
        (KHTML, like Gecko) Element Browser 5.0', \
        'IBM WebExplorer /v0.94', 'Galaxy/1.0 [en] (Mac OS X 10.5.6; U; en)', \
        'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)', \
        'Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14', \
        'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) \
        Version/6.0 Mobile/10A5355d Safari/8536.25', \
        'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) \
        Chrome/28.0.1468.0 Safari/537.36', \
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0; TheWorld)']
 
def baidu_search(keyword,pn):
    p= {'wd': keyword} 
    res=urllib2.urlopen(("http://www.baidu.com/s?"+urllib.urlencode(p)+"&pn={0}&cl=3&rn=100").format(pn))
    html=res.read()
    return html
def getList(regex,text):
    arr = []
    res = re.findall(regex, text)
    if res:
        for r in res:
            arr.append(r)
    return arr
def getMatch(regex,text):
    res = re.findall(regex, text)
    if res:
        return res[0]
    return ""
def clearTag(text):
    p = re.compile(u'<[^>]+>')
    retval = p.sub("",text)
    return retval
 
def geturl(keyword):
    for page in range(10):
        pn=page*100+1
        html = baidu_search(keyword,pn)
        
        content = unicode(html, 'utf-8','ignore')
        arrList = getList(u"<table.*?class=\"result\".*?>.*?<\/a>", content)
        for item in arrList:
            regex = u"<h3.*?class=\"t\".*?><a.*?href=\"(.*?)\".*?>(.*?)<\/a>"
            link = getMatch(regex,item)
            url = link[0]
            #获取标题
            #title = clearTag(link[1]).encode('utf8')
 
            try:
                domain=urllib2.Request(url)
                r=random.randint(0,11)
                domain.add_header('User-agent', user_agents[r])
                domain.add_header('connection','keep-alive')
                response=urllib2.urlopen(domain)
                uri=response.geturl()
                print uri
            except:
                continue
 
if __name__=='__main__':
    geturl('python')