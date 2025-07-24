# Welcome to PyLucas

---

## 安装

```
pip install pylucas
pip install pylucas[all]
pip install pylucas[fileops, log, rwxl]
```

```
poetry add pylucas
poetry add pylucas[all]
poetry add pylucas[fileops, log, rwxl]
```

---

## 支持的功能列表:

- fileops
  - ConfigEditor
    - 用于 创建/读写 配置文件
    - 支持格式: Toml, Json
  - ListFiles
    - 返回指定路径下的所有满足条件的文件.
  - FilesCopyer
    - 拷贝文件或目录下的所有文件到指定目录下.
  - FilesClear
    - 清除指定文件或指定目录下的所有文件.
- log
  - LogManager
    - 用于进行日志管理.
  - ASCII_Art
    - 用于输出 ASCII 艺术字.
- rwxl
  - ReadExcel
    - 用于读取 Excel 文件并按一定规则进行基础的数据清洗.
- struct
  - result
    - 用于作为通用的函数返回值的类型.
- function
  - GetTimeStamp
    - 用于获取当前时间戳.
  - GetCurrentFrameInfo
    - 获取当前帧信息, 可以定位到当前执行到的调用栈.
  - lindex
    - 用于从左侧查找值索引, 类似 str.find, 如未找到则返回 -1.
  - rindex
    - 用于从右侧查找值索引, 类似 str.rfind, 如未找到则返回 -1.

---

## 计划列表:

### ~~1.2.0:~~

- **_出现了大量的因向前兼容而产生的被标记为'即将弃用'的函数与方法, 并且经历大范围的重构, ThreadPool 类因性能原因没有被添加, 此版本被跳过, 直接并入包含破坏性更新的 2.0.0 版本._**

- [ ] ~~添加 ThreadPool 类, 用于线程池创建和子线程管理.~~
- [x] ~~更改 Function 文件夹结构, 使更易于管理.~~

### 2.0.0:

- **_该版本是实际意义上的第一个正式版, 尽可能的将所有接口固定下来, 以防止因为后续的修复和优化等操作导致的无法向前兼容._**

- [x] 修复各种 BUG.
- [x] 理顺项目结构.
- [x] 部分重构和优化.W
- [x] 移除部分功能(被弃用的或是被重构为新方法/函数的).

### **3.0.0:**

- **_该版本大幅度的修改了整个项目结构, 引入了子包和可选依赖._**
- **fileops.ConfigEditor:**

  - [x] 移除基类 ConfigEditorSL, 在 ConfigEditor 中直接调用 ConfigEditorSL_Json, ConfigEditorSL_Toml 的方法.
  - [x] 为 ConfigEditor 添加魔术方法 \_\_getitem\_\_, \_\_setitem\_\_ 允许使用 [] 运算符进行键索引.
  - [x] 未修改已存在的对外接口.

- **fileops.Function:**

  - [x] 将原有 Function 中的部分涉及文件操作的函数移至此处, 包含 ListFiles, FilesCopyer, FilesClear.

- **function.Function:**

  - [x] 包含 GetTimeStamp, GetCurrentFrameInfo, lindex, rindex.

- **log.LogManager:**

  - [x] 为 LogManager 添加魔术方法 \_\_call\_\_, 允许使用 () 关键字直接调用 Log 方法.

- **log.Function:**

  - [x] 把原本在 Function 内的 ASCII_Art 函数移动到此处.

- **rwxl.Function:**

  - [x] 添加函数 ReadExcel.

- **struct.Struct:**

  - [x] 移动类 result 至此.

### 未来:

- [ ] 增加类 zDownloader, 实现多线程下载器.(实现中)
- [ ] ~~增加类 zThreadPool, 实现线程池.(计划中)~~
- [ ] ~~增加类 zEventHandler, 实现事件处理系统.(计划中)~~
- [ ] ~~增加类 KbdCapturer, 实现键盘捕获.(计划中)~~
- [ ] 增加类 rpa, 实现自动化.(实现中)
