### unpackFlutter flutter快照解析器

### 项目进度

目前施工完成，达到了预期的静态解析Class和Code Offse目的

各位可以直接使用，后面基本不会再有大的改动。


### 工程说明

项目核心在于让大家了解flutter快照的解析流程

杂事诸多，自由更新，速度不快，耐心等待。

### 使用方式 

在分支里面选择对应的 flutter engine hash 版本的快照解析器

使用二进制文本编辑工具查看快照 version hash

- [hash 1441d6b13b8623fa7fbf61433abebd31](https://github.com/MiDuoKi/unpackFlutter/tree/1441d6b13b8623fa7fbf61433abebd31)


libapp.so 放到 res 目录下即可

下面是解析效果展示

```
class MyApp{
  build(){
 _kDartIsolateSnapshotInstructions + 0x134bc4 
}
}
class UnFind{
  runApp(){
 _kDartIsolateSnapshotInstructions + 0xdfb28 
}
}
class WidgetsFlutterBinding{
  ensureInitialized(){
 _kDartIsolateSnapshotInstructions + 0xdfb84 
}
}
class WhereIterable{
  get:iterator(){
 _kDartIsolateSnapshotInstructions + 0x17b7b8 
}
  map(){
 _kDartIsolateSnapshotInstructions + 0xe919c 
}
}
class _BoxEdge@396082469{
  compareTo(){
 _kDartIsolateSnapshotInstructions + 0x17ca64 
}
}
class _SemanticsDiagnosticableNode@396082469{
}
class SemanticsHintOverrides{
}
class _SemanticsFragment@364266271{
}
class PipelineOwner{
  PipelineOwner.(){
 _kDartIsolateSnapshotInstructions + 0xd6a28 
}
  requestVisualUpdate(){
 _kDartIsolateSnapshotInstructions + 0x63d7c 
}
  set:rootNode(){
 _kDartIsolateSnapshotInstructions + 0x63bcc 
}
  flushLayout(){
 _kDartIsolateSnapshotInstructions + 0xdad40 
}
  flushCompositingBits(){
 _kDartIsolateSnapshotInstructions + 0xda90c 
}
  flushPaint(){
 _kDartIsolateSnapshotInstructions + 0xda614 
}
  ensureSemantics(){
 _kDartIsolateSnapshotInstructions + 0xd5160 
}
  _didDisposeSemanticsHandle@364266271(){
 _kDartIsolateSnapshotInstructions + 0xd4fc8 
}
  flushSemantics(){
 _kDartIsolateSnapshotInstructions + 0xda154 
}
}

```

### 开发笔记和心得

看雪文章 我的主页分享

https://bbs.kanxue.com/user-home-832784.htm

更多相关的可以私聊或者 issue 

### TODO LIST

- 多版本兼容计划，鉴于多数应用还在使用flutter2，需要先适配flutter2版本的

### 感谢以下仓库提供参考

https://github.com/rscloura/Doldrums
