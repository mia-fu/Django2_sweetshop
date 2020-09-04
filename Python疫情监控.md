## 一、项目效果

![](https://upload-images.jianshu.io/upload_images/15729314-a06c2b30398abf90.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

由于我的项目是和电商项目一同部署的。在项目下 apps/cov 和 utils下的 spider.py 是 疫情监控项目。html页面在templates下。

![](https://upload-images.jianshu.io/upload_images/15729314-c3204c590092bab2.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



## 二、项目简介

基于 Python3 + Django2.2+ Echarts 打造一个疫情实时监控系统，涉及技术有：

- Python 爬虫爬取并处理腾讯疫情数据。使用 **selnium** 爬取微博热搜， **jieba** 对热搜进行分词展示
- 使用 Python 与 Mysql 数据库交互（持久化）
- 使用 Django 构建Web项目
- 基于Echarts 数据可视化展示
- 在 Ubuntu上部署 Web 项目及使用 crontab 定时调度爬虫



### 2.1 Jupyter Notebook

> Jupyter Notebook（此前被称为IPython notebook）是一个基于网页的用于交互计算的应用程序，在数据可续额领域很受欢迎。
>
> 简言之，notebook是以网页的形式打开，可以在code类型单元格中直接编写代码和运行代码，代码的运行结果也会直接在代码块下显示。如在编程过程中需要编写说明文档，可在md类型的单元格中直接编写，便于及时的说明和解释。

项目在调试过程中，使用到了 Jupyter Notebook。下面介绍详细安装以及使用，不感兴趣的朋友可以直接跳到`三、数据获取`。



#### 2.1.1 安装

```python
pip3 install notebook
```

#### 2.1.2 启动

```
jupyter notebook
```

**修改工作目录**

如果不想使用 jupyter notebook 默认的目录存储的话，可以自己修改工作目录

1. 选一个喜欢的路径创建一个目录（我这里是C:\Users\76839\note）

2. cmd输入`jupyter notebook --generate-config`

![](https://upload-images.jianshu.io/upload_images/15729314-195fee2385fc74af.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

3. 找到这个配置文件（`jupyter_notebook_config.py`）所在路径，打开它并编辑，

搜索找到`notebook_dir`

![](https://upload-images.jianshu.io/upload_images/15729314-f62fa27a2301c675.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

将前面注释去掉，在后面配置目录路径，如下图。

```
## The directory to use for notebooks and kernels.
c.NotebookApp.notebook_dir = r'C:\Users\76839\note'
```

4. 保存退出，cmd>>`jupyter notebook`启动看效果OK了么（也可以在创建的../../note目录下新建一个.cmd为后缀的脚本，内容编辑为jupyter notebook，以后点击它就可以快捷启动了）



#### 2.1.3 基本操作

1. 新建文件与导入文件

2. 单元格分类：code、md

3. 命令模式（蓝色边框）与编辑模式（绿色模式）

4. 常用快捷键

   单元格类型转换：Y、M；

   插入单元格：A、B；

   进入命令模式：Esc

   代码补全：Tab

   运行单元格：ctrl/shift/alt+enter

   删除单元格：DD

#### 2.1.4 md常用语法

1. 标题：使用1~6个 `#` 跟随一个空格表示1~6级标题

2. 无序列表：使用`*`，`-`或`+`后跟随一个空格来表示

3. 有序列表：使用数字点 `.` 表示

4. 换行：使用两个或以上的空行

5. 代码：三个反引号```

6. 分割线：三个星号`***`或三个减号`---`

7. 链接：`[文字](链接地址)`

8. 图片：`![图片说明](图片链接地址"图片说明信息")`



## 三、数据获取

### 3.1 爬虫概述

* **爬虫，就是给网站发起请求，并从响应中提取需要的数据自动化程序**
* 爬取并处理腾讯疫情数据，selnium 爬取微博热搜

1. 发起请求，获取响应
   - 通过 http 库，对目标站点进行请求。等同于自己打开浏览器，输入网址
   - 常用库：urllib、urllib3、requests
   - 服务器会返回请求的内容，一般为：HTML、二进制文件（视频、音频）、文档、JSON字符串等
2. 解析内容
   - 寻找自己需要的信息，就是利用正则表达式或者其他库提取目标信息
   - 常用库：re、beautifulsoup4
3. 保存数据
   - 将解析得到的数据持久化到文件或者数据库中

### 3.2 urllib发送请求

这里使用jupyter notebook进行测试

#### 3.2.1 测试

```python
from urllib import request
url = "http://www.baidu.com"
res = request.urlopen(url)  #获取响应
print(res.info()) #响应头
print(res.getcode()) #状态码 2xx正常,3xx发生重定向,4xx访问资源问题,5xx服务器内部错误
print(res.geturl()) #返回响应地址
```

![](https://upload-images.jianshu.io/upload_images/15729314-ebb526397ed8829d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



```python
# 获取网页html源码
html = res.read()
print(html)
```

![](https://upload-images.jianshu.io/upload_images/15729314-fe055f9ec461c1a9.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



#### 3.2.2 解决不显示中文问题

```python
# 获取网页html源码
html = res.read()
# print(html)
html = html.decode("utf-8")
print(html)
```

![](https://upload-images.jianshu.io/upload_images/15729314-29ce09776bb4dd84.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



#### 3.2.3 简单解决网站反爬机制的问题

```
例如我把上面的demo的url换成点评（www.dianping.com）的就会遇到
HTTPError: HTTP Error 403: Forbidden这个错误
```

![](https://upload-images.jianshu.io/upload_images/15729314-e6373821fc7ca42c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

解决办法：可以使用浏览器的User-Agent（我这里用的google的）进行伪装:

![](https://upload-images.jianshu.io/upload_images/15729314-53fb0c9b1f160686.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

```python
from urllib import request
url="http://www.dianping.com/"
#最基本的反爬措施：添加header信息
header={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
}
req=request.Request(url,headers=header)
res=request.urlopen(req)  #获取响应

#获取网页html源码
html=res.read()
html=html.decode("utf-8")
print(html)
```

![](https://upload-images.jianshu.io/upload_images/15729314-c8b3004bc537ea58.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



#### 3.2.4 解决报错信息 ConnectionResetError: [WinError 10054]

1. 在request后面写入一个关闭的操作，

```python
response.close()
```

2. 设置socket默认的等待时间，在read超时后能自动往下继续跑

```python
socket.setdefaulttimeout(t_default)
```

3. 设置sleep()等待一段时间后继续下面的操作

```python
time.sleep(t)
```



### 3.3 request 发送请求

#### 3.3.1 测试

1. 首先 pip 安装 requests ：`pip install requests`
2. `requests.get()`

```python
import requests

url = "http://www.baidu.com"
res = requests.get(url)

print(res.encoding)
print(res.headers)
#res.headers返回结果里面 如果没有Content-Type encoding=utf-8 否则就是ISO-8859-1 如果设置了charset就以设置的为准
print(res.url) 
```

![](https://upload-images.jianshu.io/upload_images/15729314-8bb7786b76e008c9.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

---

查看网页html源码

```python
res.encoding = "utf-8"  # 防止乱码
print(res.text)
```

![](https://upload-images.jianshu.io/upload_images/15729314-66b23b2422b9fd39.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



#### 3.3.2 解决反爬

同样，这里也把url改成点评

```python
import requests

url = "http://www.dianping.com/"
res = requests.get(url)

print(res.encoding)
print(res.headers)
#res.headers返回结果里面 如果没有Content-Type encoding=utf-8 否则就是ISO-8859-1 如果设置了charset就以设置的为准
print(res.url) 
print(res.status_code) #查看状态码发现很不幸，又是403
```

![](https://upload-images.jianshu.io/upload_images/15729314-81237b5ba8812d3c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

---

解决方法：

```python
import requests

url = "http://www.dianping.com/"
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
}
res = requests.get(url,headers=header)

print(res.encoding)
print(res.headers)
# res.headers返回结果里面 如果没有Content-Type encoding=utf-8 否则就是ISO-8859-1 如果设置了charset就以设置的为准
print(res.url) 
print(res.status_code) # 设置header，状态码返回200
```

![](https://upload-images.jianshu.io/upload_images/15729314-a787e400312811b8.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

现在就可以正常通过`print(res.text)`查看页面html源码了。不要忘了更改编码，防止乱码。

![](https://upload-images.jianshu.io/upload_images/15729314-54d5a8bf87393b92.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



### 3.4 beautifulSoup4 解析内容

> beautifulsoup4 将复杂的 HTML 文档转换成一个树形结构，每个节点都是 Python 对象

* 安装：`pip3 install beautifulsoup`

* 获取节点：find()、find_all()、select()
* 获取属性：attrs
* 获取文本：text

#### 3.4.1 测试

* 我们爬取辽宁省卫健委官网的一个网页为例。（http://wsjk.ln.gov.cn/）

* 在google浏览器中右键点击检查，出现调试界面
* 点击下图所示的箭头，之后将鼠标光标放到一处链接上

![](https://upload-images.jianshu.io/upload_images/15729314-27d223d8870eb2fc.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

* 就会显示光标所在处的标签类型，这个地方是a标签，接下来以该a标签为例展开降解

```python
from bs4 import BeautifulSoup
import requests

url = "http://wsjk.ln.gov.cn/wst_wsjskx/"
res = requests.get(url)
res.encoding = "gbk"
html = res.text
# print(html)
soup = BeautifulSoup(html)
attr = soup.find(attrs={'class':'jgsz_right_con'})      # 获取网页a标签
# print(attr)
a = attr.find_all("a")
for i in range(len(a)):
    if i == 4:
        a = a[i]
print(a)
print(a.attrs)          # 打印标签属性
print(a.attrs["href"])  # 打印标签属性中的href的值

输出结果：

<a href="./202009/t20200904_3946905.html" target="_blank">2020年9月3日0时至24时辽宁新型冠状病毒肺炎疫情情况</a>
{'href': './202009/t20200904_3946905.html', 'target': '_blank'}
./202009/t20200904_3946905.html

```

---

* 然后获取该标签属性中的href值获取新的url

```python
url_new = "http://wsjk.ln.gov.cn/wst_wsjskx/" + a.attrs["href"]
res = requests.get(url_new)
res.encoding = "gbk"
BeautifulSoup(res.text)	# 获取Html文本
```

![](https://upload-images.jianshu.io/upload_images/15729314-5f0391817727f42a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

---

* 浏览器+开发者工具查看该网页发现该部分是p标签：

![](https://upload-images.jianshu.io/upload_images/15729314-3d001224ffdd0826.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

* 所以我们定位p标签,锁定我们需要的信息以便下一步正则分析数据

```python
soup = BeautifulSoup(res.text)
context = soup.find_all("p")
print(context)



输出显示：
[<p style=" float: left;margin-left: 57px;"><a href="http://www.ln12320.cn/" style="display:block;width:110px;height:58px;" target="_parent">   </a></p>, <p align="justify" class="p" style="margin-bottom: 0pt; text-align: justify; text-justify: inter-ideograph; line-height: 16.2pt; text-indent: 26.5pt"><span style="font-size: 14pt; font-family: 宋体; color: rgb(0,0,0)"><font style="line-height: 175%">9月3日0时至24时，辽宁省无新增新冠肺炎确诊病例。无新增治愈出院病例。</font></span></p>, <p align="justify" class="p" style="margin-bottom: 0pt; text-align: justify; text-justify: inter-ideograph; line-height: 16.2pt; text-indent: 26.5pt"><span style="font-size: 14pt; font-family: 宋体; color: rgb(0,0,0)"><font style="line-height: 175%"><font face="宋体" style="line-height: 175%">截至</font>9月3日24时，全省累计报告确诊病例263例（含境外输入39例），治愈出院259例，死亡2例，在院治疗2例。目前，尚有2例无症状感染者在定点医院隔离治疗。</font></span></p>]

```



### 3.5 re 解析内容

- re是 python 自带的正则表达式模块，使用它需要有一定的正则表达式基础
- re.search(regex,str)
  - 1.在 str 中查找满足条件的字符串，匹配不上返回 None
  - 2.对返回结果可以分组，可在字符串内添加小括号分离数据
    - groups()
    - group(index):返回指定分组内容

我们接着使用刚刚上面获取的context

```python
import re
pattern = "境外输入(\d+)例"
# print(context)
# print(type(context))

text = str(context)
# print(text)
# print(type(text))
res = re.search(pattern, text)
print(res)

输出显示：
<re.Match object; span=(781, 788), match='境外输入39例'>
```

---

* 我们用re解析到我们需要的全部信息

```python
pattern = "确诊病例(\d+).*?境外输入(\d+).*?治愈出院(\d+).*?死亡(\d+)"  # .*? 为非贪心匹配
res = re.search(pattern, text)
print(res.groups())
print(res.group(0))
print(res.group(1), res.group(2), res.group(3), res.group(4))


输出显示：
('263', '39', '259', '2')
确诊病例263例（含境外输入39例），治愈出院259例，死亡2
263 39 259 2
```

![](https://upload-images.jianshu.io/upload_images/15729314-20732ef06b36dda8.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)





### 3.6 数据存储

创建数据库cov，然后建三张表。

```mysql
create database cov;

# history 表存储每日总数据
create table `history`(
    `ds` datetime not null comment '日期',
    `confirm` int(11) default null comment '累计确诊',
    `confirm_add` int(11) default null comment '当日新增确诊',
    `suspect` int(11) default null comment '剩余疑似',
    `suspect_add` int(11) default null comment '当日新增疑似',
    `heal` int(11) default null comment '累计治愈',
    `heal_add` int(11) default null comment '当日新增治愈',
    `dead` int(11) default null comment '累计死亡',
    `dead_add` int(11) default null comment '当日新增死亡',
    `importedCase` int(11) default null comment '境外输入',
    primary key(`ds`) using btree
)engine=innodb default charset=utf8mb4;

# details 表存储每日详细数据
create table `details` (
    `id` int(11) not null auto_increment,
    `update_time` datetime default null comment '数据最后更新时间',
    `province` varchar(50) default null comment '省',
    `city` varchar(50) default null comment '市',
    `confirm` int(11) default null comment '累计确诊',
    `confirm_add` int(11) default null comment '新增确诊',
    `heal` int(11) default null comment '累计治愈',
    `dead` int(11) default null comment '累计死亡',
    `importedCase` int(11) default null comment '境外输入',
    primary key(`id`)
)engine=innodb default charset=utf8mb4;


# hotsearch 表存储热搜数据
create table `hotsearch`(
    `id` int(11) not null auto_increment,
    `dt` datetime default null on update current_timestamp,
    `content` varchar(255) default null,
    primary key(`id`)
)engine=innodb default
charset=utf8mb4;
```

* 使用 pymysql 模块与数据库交互

* 安装： `pip3 install pymysql`

  ① 建立连接 ② 创建游标 ③ 执行操作 ④ 关闭连接

1. 建立连接

   ```mysql
   import pymysql
   conn = pymysql.connect(host="127.0.0.1",
                         user="root",
                         password="123456",
                         db="cov")
   ```

2. 创建游标 

   ```mysql
   cursor = conn.cursor()
   ```

3. 执行操作

   ```mysql
   sql = "select * from history"
   cursor.execute(sql)
   # conn.commit() #提交事务
   res = cursor.fetchall()
   print(res)
   ```

4. 关闭连接

   ```mysql
   cursor.close()
   conn.close()
   ```


## 四、web开发与可视化

### 4.1 echarts 可视化大屏模板设计

>  ECharts，缩写来自 Enterprise Charts，商业级数据图表，是百度的一个开源的数据可视 化工具，提供了丰富的图表库，能够在 PC 端和移动设备上流畅运行

官网网站：<https://echarts.apache.org/zh/index.html>

[5分钟上手echarts](https://www.echartsjs.com/zh/tutorial.html#5%20%E5%88%86%E9%92%9F%E4%B8%8A%E6%89%8B%20ECharts)

上手这个五分钟的案例，我们就可以搞个差不多了

#### 4.1.1 echarts绘制图表

**全国疫情地图实现**

1. 复制中国地图 option，导入 china.js

2. 获取数据

   ```python
   def get_c2_data():
       """
       :return:  返回各省数据
       """
       # 因为会更新多次数据，取时间戳最新的那组数据
       sql = "select province,sum(confirm) from details " \
             "where update_time=(select update_time from details " \
             "order by update_time desc limit 1) " \
             "group by province"
       res = query(sql)
       return res
   ```


**全国累计趋势**

1.复制折线图 option

2.获取数据

```python
def get_l1_data():
	"""
	:return:返回每天历史累计数据
	"""
    sql = "select ds,confirm,suspect,heal,dead from history"
    res = query(sql)
    return res
```



**全国新增趋势**

1. 复制折线图 option
2. 获取数据

```python
def get_l2_data():
    """
    :return:返回每天新增确诊和疑似数据
    """
    sql = "select ds,confirm_add,suspect_add from history"
    res = query(sql)
    return res
```



**非湖北地区TOP5**

1. 复制柱状图 option
2. 获取数据

```python
def get_r1_data():
    """
    :return:  返回非湖北地区城市确诊人数前5名
    """
    sql = 'SELECT city,confirm FROM ' \
          '(select city,confirm from details  ' \
          'where update_time=(select update_time from details order by update_time desc limit 1) ' \
          'and province not in ("湖北","北京","上海","天津","重庆") ' \
          'union all ' \
          'select province as city,sum(confirm) as confirm from details  ' \
          'where update_time=(select update_time from details order by update_time desc limit 1) ' \
          'and province in ("北京","上海","天津","重庆") group by province) as a ' \
          'ORDER BY confirm DESC LIMIT 5'
    res = query(sql)
    return res
```



**疫情热搜**

1. 复制词云图 option，导入wordcloud.js
2. 获取数据，使用 jieba 获取关键字

```python
def get_r2_data():
    """
    :return:  返回最近的20条热搜
    """
    sql = 'select content from hotsearch order by id desc limit 20'
    res = query(sql)  # 格式 (('民警抗疫一线奋战16天牺牲1037364',), ('四川再派两批医疗队1537382',)
    return res
```





## 五、项目部署

### 5.1 部署流程

进入到项目的目录下。

```mysql
python3 manage.py runserver
```



### 5.2 crontab 定时调度爬虫

* 获取脚本参数

  sys.argv

  sys.argv[0] 是脚本所在绝对路径

* 根据不同参数调用不用方法

* Ubuntu 安装 chrome
  1. 使用Ubuntu自带的火狐浏览器打开<https://www.google.cn/chrome/>
  2. 点击下载Chrome，选择64位.deb 下载
  3. 进入到下载目录：右键在终端打开
  4. 执行 `sudo dpkg -i google-chrome-stable_current_amd64.deb`
  5. 安装执行完成后输入：`google-chrome`  打开谷歌浏览器
  6. 把谷歌浏览器加入左侧收藏方便下次使用

* 下载 chromedriver

<http://npm.taobao.org/mirrors/chromedriver/> 项目中使用的 79.0.3945.36/



---



```
crontab -l # 列出当前任务
crontab -e # 编辑任务
```

* 格式：* * * * * 指令 五个星号分别代表 分 、时 、日 、月、周



源码获取：[GitHub地址]()