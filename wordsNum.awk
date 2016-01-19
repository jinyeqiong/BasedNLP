#统计文件需要用utf8格式

#统计词、字的个数
#单行处理
#awk '{print $0} {print "The numbers of words:" NF } {print "The numbers of characters:" length-(NF-1)}' testexample.txt

#多行处理，末尾空格去掉
awk 'BEGIN {words=0;chars=0;} {sub(" *$","")}{words=words+NF;chars=chars+length-(NF-1);print $0;}\
 END {print "The numbers of words:" words } END {print "The numbers of characters:" chars} ' testexample.txt

#取出某些特定的字段
#？？？ 特定字段什么意思？？？
