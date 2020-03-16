# 基于Python的logging模块实现日志系统

----

## logging模块简介
logging模块是Python的一个标准库模块，其所定义的函数和类为开发任意提供了可灵活使用的事件日志系统。  

关于logging模块的详细文档，请参考[日志 HOWTO](https://docs.python.org/zh-cn/3/howto/logging.html)和[日志操作手册](https://docs.python.org/zh-cn/3/howto/logging-cookbook.html)。  

这里只讲述logging模块的基本概念和简单使用。  

### 日志等级
| 日志等级（level） | 描述 |
| -- | -- |
| DEBUG | 调试用的日志信息，一般应用在开发环境中 |
| INFO | 等级比DEBUG要高，一般用于记录关键日志信息 |
| WARNING | 用于记录发生不期望但不影响程序运行的事件信息 |
| ERROR | 程序产生错误而导致功能异常的信息 |
| CRITICAL | 程序产生严重错误而导致无法继续运行的信息 |

  * 对应日志等级的函数有：logging.debug、logging.info、logging.warning、logging.error、logging.critical。
  * logging.log可将**日志等级**作为参数传入，如logging.log(level, *args, **kwargs)。

### 格式字符串字段
这里只列举一些常用的格式字符串字段。  
| 字段/属性名称 | 使用格式 | 描述|
| -- | -- | -- |
|asctime|%(asctime)s|日志事件发生的时间，如：2020-03-08 12:00:00,121
|levelname|%(levelname)s|该日志记录的文字形式的日志级别（'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'）|
|name|%(name)s|所使用的日志器名称，默认是'root'|
|message|%(message)s|日志记录的文本内容，通过 msg % args计算得到的|
|pathname|%(pathname)s|调用日志记录函数的源码文件的全路径|
|filename|%(filename)s|pathname的文件名部分，包含文件后缀|
|module|%(module)s|filename的名称部分，不包含后缀|
|lineno|%(lineno)d|调用日志记录函数的源代码所在的行号|
|funcName|%(funcName)s|调用日志记录函数的函数名

### 日志器
可通过以下方式来获取日志器。  
```py
# 该方法使用通过logging.basicConfig(filename="xxx.log", level=logging.DEBUG, format="%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s")设置的配置来创建日志器
logger = logging.getLogger("logger-name");

# 直接通过构造类类获取新的日志器
logger = logging.Logger("name", level = logging.DEBUG);
```

### 处理器
处理器主要将消息分发到指定位置，其中日志器可以有多个处理器。  
以下列举了几种处理器：
|Handler|描述|
|--|--|
|logging.StreamHandler|将日志消息发送到输出到Stream，如std.out, std.err或任何file-like对象。|
|logging.FileHandler|将日志消息发送到磁盘文件，默认情况下文件大小会无限增长|
|logging.handlers.RotatingFileHandler|将日志消息发送到磁盘文件，并支持日志文件按大小切割|
|logging.hanlders.TimedRotatingFileHandler|将日志消息发送到磁盘文件，并支持日志文件按时间切割|
|logging.handlers.HTTPHandler|将日志消息以GET或POST的方式发送给一个HTTP服务器|
|logging.handlers.SMTPHandler|将日志消息发送给一个指定的email地址|
|logging.NullHandler|该Handler实例会忽略error messages，通常被想使用logging的library开发者使用来避免'No handlers could be found for logger XXX'信息的出现。|


## 封装及改进日志功能
改进点：
  * 输出日志的函数（如`logging.debug`）时，想输出多个数据，要在首个参数中使用占位符（如`"%s"`、`"%d"`等），感觉比较麻烦。
  * 输出日志函数名可以进行缩短，以减少要敲的字符。
  * 将窗口和文件输出的处理器进行封装，而避免要分两次设置处理器。

完整代码参考：  
Github链接：[https://github.com/JDreamHeart/DailyCodes/python/article/logger.py](https://github.com/JDreamHeart/DailyCodes/blob/master/python/article/logger.py)  

使用方式：  
```py
import os;
import Logger; # 上面完整代码中定义的Logger

# 初始化
name = "file_name";
curTimeStr = time.strftime("%Y_%m_%d", time.localtime());
logger = Logger("Main", isLogFile = True, logFileName = os.path.join(os.getcwd(), "log", name+("_%s.log"%curTimeStr)),
            maxBytes = 1024 * 100, backupCount = 10);

# 使用
logger.d("Debug info:", "first info.");

logger.e("Error info:", "failed! Err:", Exception("detail error info"));
```


## 在Linux上删除7日前的日志
sh脚本：  
```sh
# 配合crontab定时任务使用

function remove_log() {
    echo "搜索路径："
    echo $1
    path=$1
    head=$2
    log=`find ${path} -mtime +7 -name \"${head}*_*.log\"`
    log_bak=`find ${path} -mtime +7 -name \"${head}*_*.log.*\"`
    for name in $log
    do
        echo "删除日志${name}"
        sudo chmod 777 ${name}
        rm -f 777 ${name}
    done
    for name in $log_bak
    do
        echo "删除日志${name}"
        sudo chmod 777 ${name}
        rm -f 777 ${name}
    done
}

remove_log /data/project/....../log file_name
```
