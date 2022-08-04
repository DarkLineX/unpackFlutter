### 前言

分析flutter最核心的部分应该是了解dart类布局，这要从flutter快照里面解析出来。

基于静态的有Doldrums库
基于动态的有reFlutter

鉴于Doldrums的效果良好，我更喜欢静态的解析，不怕重打包的对抗。

当然需要我们自己适配新的版本，实际上我们只要动手写过一个版本。后面的版本都是改动一点点就行。

### 编写思路

总体思路:把Snapshot看成一种异化的DEX，只是他的格式不是标准和公开的。需要自己阅读flutter engine 源码去对照字段。好在有Doldrum源码。我们可以节约时间分析。

### 直接开写

#### 1.下载flutter engine源码

看小黄鸭这篇就行 


https://bbs.pediy.com/thread-272866.htm

具体下什么版本和你要研究的快照版本有关

#### 2.确认快照Magic

要从libapp.so里面解析出快照信息，先要对so文件进行分析。

我们使用`elftools`进行解析

我们提取用010edit查看就知道区段的内容

>源代码中关于 snapshot.h snapshot.cc 的内容对应 snapshot 对象 

因为Snapshot有个魔数头

```
static const int32_t kMagicValue = 0xdcdcf5f5;
```
所以我们搜索 `F5F5DCDC` 

![9de4a5496db3d38459ea51e728963fd2.png](en-resource://database/2719:1)

为什么有两个，因为有两个快照。当然格式一样可以一起解析。

- DartVmSnapshot
- DartIsolateSnapshot

如果app对so进行重命名你找不到flutter.so可以进行魔数检测找出来对应的so.当然查看导出函数也可以

```
'_kDartVmSnapshotData','
_kDartVmSnapshotInstructions',
'_kDartIsolateSnapshotData',
'_kDartIsolateSnapshotInstructions',
'_kDartSnapshotBuildId'
```

### 3.分析源码对so的解析流程

从so到Snapshot到具体的Dart方法流程大概如下:

我简单理一下给大家


- dart.cc  `Dart::Init`
- dart.cc  `Dart::DartInit`
- dart.cc  `Dart::InitIsolateFromSnapshot`
- snapshot.cc `Snapshot* Snapshot::SetupFromBuffer`


在mian.cc的main函数中有个最早的初始化参数`Dart_InitializeParams` 里面包含了最初的一些东西

![856a64e3eba59d465544cf5e47c616cb.png](en-resource://database/2721:1)

核心的 `  init_params.vm_snapshot_data = vm_snapshot_data;`就是我们要找的

具体要怎么从ELF文件中找到对的段映射成sn

我使劲的搜索 Snapshot Elf 这几个关键字 终于让我找到了

```
AppSnapshot* Snapshot::TryReadAppendedAppSnapshotElf
AppSnapshot* TryReadAppSnapshotElf
```
要验证是不是只要打个log调试下就行，为了赶时间我直接就用它法分析了，错了大不了换个函数测试。

我们想要的逻辑在这里

![0b2cc9b0a444d16036b718349724e90b.png](en-resource://database/2723:1)

分析出这几个symbol传进来就行，进行区间的映射关系

一个大小和起始位置计算出所有的blob


![47253cf63ca0a189ceace37e941cf477.png](en-resource://database/2725:1)

### 3.解析出Snapshot


前面已经拿到了我们的blobs 下面

在DartVM虚拟机原理里面已经告诉我们，每种快照格式都对应两个数据存放


VmSnapshot = 
`_kDartVmSnapshotData` 和_`kDartVmSnapshotInstructions`


IsolateSnapshot = 
`_kDartIsolateSnapshotData` 和 `_kDartIsolateSnapshotInstructions`

很合理对应我们四个blob区块

对应源码就是

InitIsolateFromSnapshot

![8cd6bb43f8c26a9787f8f8cbb146c729.png](en-resource://database/2727:1)


### 源码

具体的源码已经分享

https://github.com/MiDuoKi/unpackFlutter

### 参考

 https://github.com/rscloura/Doldrums