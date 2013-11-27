expert_finding
==============

advanced machine learning prj

using svmlight 0.4


### 运行 ###
1. 模型训练:可以在zmode.py中修改模型的训练集
        python zmode.py

1. 运行finding expert 服务
        python app.py 

### 实现 ###

#### 特征选取 ####
直观来说，每个topic下都有若干相关联的会议列表，每个会议都有一个score来表示这个会议的难易程度。一个人如果在score比较高的会议上发表的论文比较多，或者发表的论文引用比较多，那么可以认为这个人在这个领域是比较顶尖的。
在feature.py中定义参数RANK_SIZE表示把会议按照score的大小分为几类，如RANK_SIZE = 5,那么按照score大小为0-0.5, 0.5-1, 1-1.5, ...., 分为5类。
每个人的特征向量是一个RANK_SIZE * 2 的向量，前RANK_SIZE 个值表示在对应score类上的会议发表的文章个数，后RANK_SIZE个值表示在对应的score类上发表文章引用的次数的和。

如，在RANK_SIZE = 3的情况下，某个人对应的特征向量是[3,2,1, 300, 200, 100]，表示这个人在score范围在[0-0.5] 的会议上发表的文章个数是3，这3篇文章的引用次数为300次，以此类推。

#### 模型 ####
采用pairewise svm ranking，具体实现的时候用的是开源的pysvmlight库。

#### 具体实现 ####
1. 当输入一个topic之后，首先找到这个topic相关的会议列表 topic_confs 和 每个会议对应的score
1. 通过arnetminer提供的search借口，搜索得到前500个这个topic下面的人 auothers, 对这些人根据模型rerank
1. 得到auothers 中的每个人发表的文章所在的会议列表 auothers_publish_confs，和对应文章的引用次数
1. 求topic_confs和auothers_publish_confs的交集得到这个人的特征向量
1. 输入到模型中求解，返回结果

#### 一些优化 ####

##### Cache #####
因为很多数据都需要从网上爬下来，为了保证每个请求的响应时间在60s之内，所以对每次访问arnetminer怕下来的数据做了缓存，每个请求结束的时候都会把结果dump到磁盘上和缓存在内存中，每次系统初始化的时候，从磁盘读取缓存的数据。


##### Cheat #####
猜想输入的数据集应该是 http://arnetminer.org/topic-browser 的一个子集，所以，我做了这样一件事情，系统模型训练好之后，写了一个脚本cheat.py，解析上面的url，提取到所包含的topic，然后用我写的搜索服务将这些topic对应的搜索中间结果缓存。这样如果输入了同样的topic，那么就不需要从网上爬数据了，直接返回。缓存了大概300MB的数据。


