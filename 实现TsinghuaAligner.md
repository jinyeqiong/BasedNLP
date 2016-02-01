TsinghuaAligner简介：http://nlp.csai.tsinghua.edu.cn/~ly/systems/TsinghuaAligner/TsinghuaAligner.html

## 准备工作，安装一下软件

1. GIZA ：详情可见为知笔记
2. g++ version 4.6.3 or higher
3. Python version 2.7.3
4. JRE 1.6 or higher (用于可视化界面)

## 安装TsinghuaAligner

### 1. 将TsinghuaAligner.tar.gz解压

```bash
tar xvfz TsinghuaAligner.tar.gz
```

### 2. 编译TsinghuaAligner

在TsinghuaAligner目录下，有5个文件夹和一个脚本文件（install.sh）：
code：存储源代码
doc：包含文档
example：存储例子数据
GUI：包含可视化工具 Align Viz
scripts：包含训练系统的Python脚本文件

先将install.h可执行化，并执行install.sh脚本文件

```bash
chmod +x install.sh
./install.sh
```

此操作完成后，将产生bin文件夹。

### 3. 编译GIZA++

安装编译GIZA++（参考为知笔记：GIZA++实验），将GIZA++-v2目录下的GIZA++，plain2snt.out，snt2cooc.cout，和mkcls-v2目录下的mkcls，四个执行文件放入bin文件夹中，目前在bin 文件夹中一共有12个可执行文件。

### 4. 添加路径

训练TsinghuaAligner主要是通过Python脚本完成的（scripts 文件夹），我们需要使脚本追溯到科执行文件，通过下面的操作：

在scripts文件夹中，进入GIZA.py，将第7行的root_dir的路径改成TsinghuaAligner文件夹所在路径。

```bash
root_dir=''
改成
root_dir=‘/home/xuexin/workspace/Tsinghua/TsinghuaAligner’
```

注：可以通过`pwd`查看TsinghuaAligner路径全称

之后，将supervisedTraining.py和unsupervisedTraining.py文件中的root_dir也改成此路径。

## 执行TsinghuaAligner

### 快速开始

首先，在http://nlp.csai.tsinghua.edu.cn/~ly/systems/TsinghuaAligner/TsinghuaAligner.html ，下载model.ce.tar.gz（见附件），之后对其解压，它是可以直接被TsinghuaAligner使用的中英文模型。

```bash
tar xvfz model.ce.tar.gz
```

解压后，将model.ce文件移到quickstart目录下，quickstart原本目录下有chinese.txt（中文文本），english（英文文本），TsinghuaAligner.ini（系统配置文件）

```bash
#要将可执行文件TsinghuaAligner复制到quickstart目录下操作
./TsinghuaAligner --ini-file TsinghuaAligner.ini --src-file chinese.txt --trg-file english.txt --agt-file alignment.txt
```

得到的结果是 0-0 1-2……，0-0表示第一个中文词对应第一个英文词。

## 得到参数（所需的配置文件TsinghuaAligner.ini及对齐文件alignment.txt）

### 运行GIZA++

TsinghuaAligner是基于对数线性模型（log-linear models）的。

在训练log-linear 模型之前我们要先运行GIZA++，通过运行scripts目录下的GIZA++.py

GIZA++.py的输入是一堆平行语料：源文件--中文语料（example/trnset/trnset.f），目标文件--英文语料（example/trnset/trnset.e）

注：
1. 对于所有的训练，开发，测试集的中文，我们都要采用**UTF-8**编码
2. 每一行的句子不要超过100个词，因为GIZA++在训练之前都会缩短长句子以至于带来不便的问题
3. 英文要小写

```bash
#保证GIZA.py，trnset.f，trnset.e都在一个文件夹下运行
GIZA.py trnset.f trnset.e
nohup GIZA.py trnset.f trnset.e #当训练语料很大时，使用 nohup 可是在退出后仍然执行操作
```

当GIZA++训练完成后，会有四个文件生成：

source.vcb：源语言词汇库（单词编号 词 个数）
target.vcb：目标语言词汇库
source_target.tTable：源语言到目标语言的概率（源语言位置 目标语言位置 概率）
target_source.tTable：目标语言到源语言的概率

### 全监督训练（scripts文件夹中的supervisedTraining.py）

全监督训练需要依靠开发集去学习对数线性模型的参数。

开发集：example/devset
devset.f：源语言（汉语句子所对应的拼音，分词后）
devset.e：目标语言（英文句子）
devset.wa：源-标准文件（1:1/1表示第一个源词和第一个目标词，以及它们之间一个确定的联系；/0表示两词之间可能的联系）

全监督训练配置文件：TsinghuaAligner.ini

```bash
supervisedTraining.py --src-vcb-file source.vcb --trg-vcb-file target.vcb --s2t-ttable-file source_target.tTable --t2s-ttable-file target_source.tTable --dev-src-file dev.f --dev-trg-file dev.e --dev-agt-file dev.wa
```

### 无监督训练（scripts文件夹中的unsupervisedTraining.py）

无监督训练配置文件：TsinghuaAligner.ini

```bash
unsupervisedTraining.py --src-file trnset.f --trg-file trnset.e --src-vcb-file source.vcb --trg-vcb-file target.vcb --s2t-ttable-file source_target.tTable --t2s-ttable-file target_source.tTable
```

配置文件：
全监督：利用开发集训练配置文件（source.vcb，target.vcb，source_target.tTable，target_source.tTable，dev.f，dev.e，dev.wa）
无监督：利用源语言和目标语言训练配置文件（ trnset.f trnset.e source.vcb，target.vcb，source_target.tTable，target_source.tTable）

### 对齐隐藏的平行语料（汉语拼音-英文句子）

生成对齐语料(alignment.txt)

```bash
#source.txt存放分词后的拼音句子，target.txt 存放英文句子
TsinghuaAligner --ini-file TsinghuaAligner.ini --src-file source.txt --trg-file target.txt --agt-file alignment.txt
TsinghuaAligner --ini-file TsinghuaAligner.ini --src-file source.txt --trg-file target.txt --agt-file alignment.txt --posterior 1 #显示链接概率
```

注：最后要的alignment.txt是不加概率的文件。

### 可视化（GUI文件夹下的Align Viz可执行文件）

```bash
java -jar AlignViz.jar
```

得到界面后，点击`File`，填选源文件，目标文件，及相应的alignment.txt

### 评估

用到测试集（example/tstset），源文件tstset.f，目标文件tstset.e，联系（确定/可能）文件tstset.wa

```bash
./TsinghuaAligner --ini-file TsinghuaAligner.ini --src-file tstset.f --trg-file tstset.e --agt-file alignment.txt
```

这时得到测试用的对齐文件alignment.txt，与人工标注的tstset.wa进行对比。

```bash
./waEval tstset.wa alignment.txt
```

## 追加数据集

在TsinghuaAligner.tar.gz中，只提供了少量的训练集，开发集和测试集，在实际操作中，需要用到大量的训练集，人工标注的开发集和测试集（http://nlp.csai.tsinghua.edu.cn/~ly/systems/TsinghuaAligner/TsinghuaAligner.html 提供了，亦可见附件）

1. model.ce.tar.gz

由GIZA++通过上百万对中英文句子训练得到的模型。其中中文词都是半角符号，英文词都要小写。

2. Chinese-English training set 

训练集。其中包括来自United Nations website (UK) 43000对中英文句子，来自Hong Kong Government website (HK) 630000对中英文句子。

3. Chinese-English evaluation set

包括450句的开发集（.f .e .wa）和450句的测试集。

**注：对于中文文件和英文文件都要用UTF-8编码。**


























