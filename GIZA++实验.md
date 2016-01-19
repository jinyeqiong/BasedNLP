GIZA++是词对齐的工具，是很多机器翻译系统的基础。

## 目标

- 下载并编译 GIZA++ 和 mkcls，获得所需的可执行文件。

- 利用平行双语语料库，通过 mkcls 构建 word classes。

- 利用平行双语语料库，通过 GIZA++ 进行 IBM Model 的训练。
​
## 前期准备

- GIZA++

  见 附件

- 平行双语语料库

  中文语料：存储**分词后**的汉语句子。文件命名为chinese
  英文语料：存储**分词后**的英文句子。文件命名为english

- 实验环境

  Ubuntu 10.10 x86
  gcc 4.4.5+

## 实验

### 编译GIZA++

下载GIZA++（giza-pp-v1.0.7.tar.gz），并解压，下载附件即可。
http://code.google.com/p/giza-pp/downloads/list

> 老版本段 GIZA++ 不能被 gcc 4.3 或更高版本编译，属于一个 bug，而 Ubutu 10.10 默认安装的 gcc 4.4，有两种方法可以成功编译。
新版本的已经没有这个问题来，可以直接编译
　　　（一）安装 g++-4.1： sudo apt-get install g++-4.1，修改 GIZA++-v2 里的 Makefile，将第5行 CXX=g++，替换为 CXX=g++-4.1
　　　（二）修改 GIZA++-v2 中的 file_spec.h 的 37-49 行（仅针对1.0.4版本）
　　　　struct tm *local;
　　　　time_t t;
　　　　char *user;　　　　
　　　　char time_stmp[19];　//修正
　　　　char *file_spec = 0;
　　　　t = time(NULL);
　　　　local = localtime(&t);
　　　　sprintf(time_stmp, “%04d-%02d-%02d.%02d%02d%02d.”, 1900 + local->tm_year,  (local->tm_mon + 1), local->tm_mday, local->tm_hour, local->tm_min, local->tm_sec); //修正
　　　　user = getenv(“USER”);

```bash
#在giza-pp目录下运行
make
```

编译成功后，在 GIZA++-v2 和 mkcls-v2 目录下各生成了一些可执行文件。

### 构建GIZA++所需文件

#### 1. 将普通文件转化为GIZA++格式

```bash
#将文件chinese和english放在GIZA++-v2目录下
#并在GIZA++-v2目录下运行
./plain2snt.out chinese english
```

**生成的文件**

**chinese.vcb（english.vcb）**

* 单词编号

* 汉语句子中的单词

* 单词的出现次数

**chinese_english.snt（english_chinese.snt）**

* 每个句子对出现的次数

* 汉语句子中的单词编号

* 英语句子中的token编号

**注： 0是保留给特殊的“空”token。**

### 生成共线文件

```bash
#在GIZA++-v2目录下运行
./snt2cooc.out chinese.vcb english.vcb chinese_english.snt > chn_eng.cooc
./snt2cooc.out english.vcb chinese.vcb english_chinese.snt > eng_chn.cooc
```

### 生成word classes（构建GIZA++所需的mkcls文件）

```bash
#将文件chinese和english放在mkcls-v2目录下
#在 mkcls-v2目录下运行
./mkcls -pchinese -Vchinese.vcb.classes opt
./mkcls -penglish -Venglish.vcb.classes opt
```

参数设置

* -n：表示训练迭代次数，默认1次

* -p：需要聚类的已分词文本

* -V：输出信息

* opt：优化运行

**生成的文件**

**chinese.vcb.classes（english.vcb.classes）**

* 按字母表序的单词

* 单词词类

** chinese.vcb.classes.cats（english.vcb.classes.cats）**

* 单词词类

* 对应词类的一组单词

### 运行GIZA++

```bash
#将上一步生成的文件全放在GIZA++-v2目录下
#并在GIZA++-v2目录下运行
./GIZA++ -S chinese.vcb -T english.vcb -C chinese_english.snt -CoocurrenceFile chn_eng.cooc -O c2e
./GIZA++ -S english.vcb -T chinese.vcb -C english_chinese.snt -CoocurrenceFile eng_chn.cooc -O e2c
```

**生成文件（以汉-英为例）**

*注：生成文件都以c2e.或e2c.开始*

**Decoder.config**

* 用于ISI Rewrite Decoder解码器

**trn.src.vcb，trn.trg.vcb**

* 类似于chinese.vcb和english.vcb文件

** tst.src.vcb，tst.trg.vcb**

* 空文件

**ti.final**

* 从英文到中文的词语对齐 

* 词语对齐通过token编号表示，并在每组数字后给出相应的对齐概率

> 例如：
　　　3 0 0.237882
　　　11 0 0.900132

**actual.ti.final**

* 从英文到中文的词语对齐

* 词语对齐通过实际 token 表示，并在每组 token 后给出相应的对齐概率

> 例如：
　　　 polished 闪闪 1
　　　 pain 割 0.0173626

**注意：如果需要生成该文件(ti.final)，需要删除GIZA++v2/Makefile中的-DBINARY_SEARCH_FOR_TTABLE选项，再重新编译即可，否则默认使用id的方式进行加载，不会生成该文件**

**A3.final**

* 记录了在 IBM Model 3迭代训练后，每个句对的一个最佳对齐 (Viterbi Alignment)。

* 第一行是一个可用于作为对齐可视化工具的标题的一个标签，包含训练的语料库中的有关该句编号的信息在训练语料，句子长度和对齐概率。

* 第二行是目标语言，第三行是源语言，源语言中的每个记号之后是一个零或多个数字的集合，这些数字代表的与源语言记号连接的目标语言记号位置。

**perp**

* 在训练的最后生成，提出了每次训练迭代的困惑度值的列表

**a3.final**

* 包含的形式如下的表

* i j l m p ( i / j, l, m)
* j = position of target sentence
* i = position of source sentence
* l = length of the source sentence
* m = length of the target sentence
* p( i | j, l, m) = is the probability that a source word in position i is moved to position j in a pair of sentences of length l and m   

** d3.final**

* 类似于a3.final文件，只是 交换了i 和 j 的位置

**n3.final**

* 源语言 token 的 fertility 分别为 0，1，…，n 时的概率表，形式如下：
　　　　　　source__id p0 p1 p2 …. pn，p0 是fertility为0时的概率

>例如：
　　　1 0.475861 0.282418 0.133455 0.0653083 0.0329326 0.00844979 0.0014008
　　　10 0.249747 0.000107778 0.307767 0.192208 0.0641439 0.15016 0.0358886
　　　11 0.397111 0.390421 0.19925 0.013382 2.21286e-05 0 0
　　　12 0.0163432 0.560621 0.374745 0.00231588 0 0 0

** t3.final**

* IBM Model 3训练后的翻译表，形式如下：
　　　　s_id t_id P(t_id/s_id)
　　　　s_id：源语言token编号
　　　　t_id：目标语言token编号
　　　　P(t_id / s_id)：源语言token翻译为目标语言token的概率

**D4.final**

* IBM Model 4的distortion表

** gizacfg**

* 包含训练当中所用的所用参数设置

* 训练可以精确复制














