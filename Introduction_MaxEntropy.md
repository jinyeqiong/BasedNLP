# 最大熵

## 一. 简介

本程序实现了多层神经网络利用最大熵实现多分类的问题。

## 二. 操作步骤

环境：Linux系统，g++4.8以上，Eclipse平台

### 1. 需要的文件

a. MaxEntropy文件(特征抽取需要自己改)   https://github.com/jinyeqiong/MaxEntropy

b. LibN3L文件  https://github.com/jinyeqiong/LibN3L

c. mshadow文件   https://github.com/jinyeqiong/mshadow

d. OpenBLAS文件   https://github.com/jinyeqiong/OpenBLAS

### 2. 配置文件

a. 配置openblas:

【注：程序是C++ ，因此要安装C++编译环境，即g++】

```bash
#在home目录下(make clean 可以先清空一下)
sudo apt-get install g++

# 切换到openblas的目录下
cd openblas    #以读者实际路径为准
make USE_THREAD=0  #single thread version, one can use multi-thread version as well.
make install  #default path /opt/OpenBLAS

# 切换到第三方软件opt目录里的一个文件中
cd /opt/OpenBLAS/include/
cp * /usr/include       #将/opt/OpenBLAS/include/里的文件全部复制到/usr/include里

# 切换到/opt/OpenBLAS/lib/目录：
cd /opt/OpenBLAS/lib/
cp *.* /usr/lib    #将/opt/OpenBLAS/lib/里的带后缀名的文件全部复制到/usr/lib里
```

b. 配置mshadow

```bash
#切换到mshadow目录下
cd mshadow     #以读者实际路径为准
cp -r mshadow /opt    ##将mshadow里的文件按递归文件复制到opt中
```

### 3. 运行程序

a. 将文件导入Eclipse

```File -> Import -> C/C++ -> Existing Code as Makefile Project -> Linux GCC```，添加文件所在路径即可。

b. 添加LibN3L和mshadow路径

```
项目右键 -> Properties -> C/C++ General -> Paths and Symbols -> GNU C++
Add -> ../LibN3L
Add -> /opt/mshadow
```

c. 运行项目

```项目右键 -> Clean Project -> Build Project```

d. 命令行操作

```bash
# 切换到MaxEntropy目录下
cd MaxEntropy     #以读者实际路径为准

./cleanall.sh 清除多余的文件（去掉比原文件夹多出来的文件）【如果没有执行权限，添加权限设置，必要时去掉sudo试试】
cmake .
make

# 将训练语料，开发语料，测试语料放入一个文件夹xx中，并放入MaxEntSentiment文件夹下
# 切换到文件夹xx中
cd xx    #读者可以自行起名
#运行最大熵，结果存在xx1.log中
../MaxEntLabeler -l -train train.txt -dev dev.txt -test test.txt -option option.sparse >xx1.log 2>&1 &
```

## 三. 基本原理

通过y'=wx，利用梯度下降法不断更新w，从而得到最合适的标签y，进而判别分类类型。

### 1. 程序输入输出

**输入形式**：[标签 句子（分词后）] 

eg. 1 我 喜欢 读书

**特征向量x**：将句子中的词转为向量，若词在特征库中出现，则标记下标

eg. <1 3> ("我"，"读书"在特征库中出现，而"喜欢"未出现在特征库中)

**输出形式**：<标签向量>

eg. <1 0> (二分类举例，此为正向性)

### 2. 最大熵计算变量

x：输入向量，即特征向量，标记的是词的下标；假设有n个特征，则x为1×n维向量

y：输出向量，即标签向量，标记类别；假设二分类问题，则y为1*2维向量

w：中间向量，初始值随机给定，是n×2维向量

### 3. 最大熵计算过程

a. 前向算法：``` y'=x*w ```，通过随机给定的w，计算得到y'，y'仍是1*2维向量

b. softmax：``` ly=y-y' ```，计算y的损失

c. 后向算法：``` lw=ly*(y'(w)) ```，其中y'(w)是y对w求导，计算得到w的损失

d. 更新w：通过lw更新w

e. 迭代：得到新的w值，重复a的前向算法，以此类推，重复多次

## 四. 代码详解

主程序：MaxEntLabeler.cpp

所需文件：训练集、开发集、测试集，文件的格式见———第三部分程序的输入形式

#### A. 读入训练集、开发集、测试集，形式改为Instance  【readInstances()】

Instance格式：string vector<string> [标签 词向量]

#### B. 创建字母表：即通过训练集得到标签库和特征库 【createAlphabet()】

将所有训练集遍历一遍，将标签和特征分别存入m_labelAlphabet和m_featAlphabet中，表中的格式是map表{string，int}，即[标签/特征，下标数字]

**注意**：

 m_labelAlphabet的大小就是类别的个数；
 
【extractLinearFeatures()】是抽取特征，抽取出的特征并不全要，而是特征个数超过了给定的一个阈值featCutOff，才将特征存储到m_featAlphabet中。

#### C. 将Instance转为Example格式 

Example格式：vector<int> vector<int>

【convert2Example()】将Instance转为Example格式，标签中是哪类则哪类就是1，其余为0；对于特征，将该词在特征库中的下标存入特征向量中

【initialExamples()】将所有句子都从Instance转为Example格式

**注**：至此，已经得到我们要计算的输入特征向量x和输出向量y了。

#### D. 进行最大熵处理

(1) 对于训练集处理

a. 将Example形式的训练集打乱顺序

b. 【m_classifier.process()】
随机选择一句话的特征，进行前向算法，得到输出output，即得到1*2维向量

c. 计算损失，传入前向算法得到的结果output和正确的标签结果，得到输出的损失outputLoss

d. 进行后向算法，传入特征向量、output和损失outputLoss，得到w的损失

e. 【m_classifier.updateParams()】更新w

(2) 对于开发集处理

开发集的处理与训练集相似，但是只是进行前向算法，得到估计的输出向量output

(3) 对于测试集处理

与开发集相似

**总结**

训练集目的：迭代更新w

开发集目的：寻找开发集结果最好的情况下，对应的测试集的结果

测试集：输出结果





























