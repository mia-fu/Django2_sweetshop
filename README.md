# 姜饼小屋项目总结 — Django2.2版本

## [点击查看Python疫情监控系统项目介绍](https://github.com/mia-fu/Django2_sweetshop/blob/master/Python%E7%96%AB%E6%83%85%E7%9B%91%E6%8E%A7.md)

## 1. 简介

本项目采用django2.2.0，该项目包含了实际开发中的电商项目中大部分的功能开发和知识点时间。在此记录一个多月以来走过这个项目的过程，包括 django 版本问题的坑等等，希望自己在程序媛的道路上越走越远╭(′▽`)╯。

关键词：django2  celery fdfs haystack whoosh redis ngnix 高并发 分布式



## 2. 姜饼小屋商业模式

姜饼小屋采用B2C的商业模式。B2C 是 Business-to-Customer 的缩写，而其中文简称为“商对客”。“商对客”是电子商务的一种模式，也就是通常说的直接面向消费者销售产品和服务商业零售模式。这种形式的电子商务**一般以网络零售业**为主，主要借助于互联网开展在线销售活动。

**B2C 即企业通过互联网为消费者提供一个新型的购物环境**——网上商店，消费者通过网络在网上购物、网上支付等消费行为。 

**案例:唯品会、乐蜂网**



## 3. 开发环境

```
Python 3.7.4
django:2.2.10
pycharm:2019.1.3
OS: windows 10 + 后期部署Ubuntu（Linux）
```



## 4. 项目部署

* 依赖库安装

```
pip install -U pip
pip install -r requirements.txt
```

* MySQL 数据库创建

```mysql
CREATE DATABASE `sweetshop` CHARACTER SET 'utf8mb4';
```

* 启动项目所需服务(win10)

```bash
# windows redis的启动，配置文件在redis安装目录下
$ redis-server redis.windows.conf

# 启动celery4.3, 进入项目虚拟环境，在项目根目录下执行
$ celery -A celery_tasks.tasks worker --loglevel=info

# 启动fastdfs
sudo service fdfs_trackerd start
sudo service fdfs_storaged start
```

* 修改nginx配置

```bash
# 进入nginx目录下
cd /usr/local/nginx/conf

# 修改nginx.conf
vim nginx.cong

# 修改如下
#user  nobody;
worker_processes  1;

#error_log  logs/error.log;
#error_log  logs/error.log  notice;
#error_log  logs/error.log  info;

#pid        logs/nginx.pid;


events {
    worker_connections  1024;
}


http {
    include       mime.types;
    default_type  application/octet-stream;

    #log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
    #                  '$status $body_bytes_sent "$http_referer" '
    #                  '"$http_user_agent" "$http_x_forwarded_for"';

    #access_log  logs/access.log  main;

    sendfile        on;
    #tcp_nopush     on;

    #keepalive_timeout  0;
    keepalive_timeout  65;

    #gzip  on;

    server {
        listen       8888;
        server_name  localhost;
        location ~/group[0-9]/ {
                ngx_fastdfs_module;
            }
        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
        root   html;
            }
	}

    upstream sweetshop{
	server 127.0.0.1:8080;
	server 127.0.0.1:8081;	

	}

    server {
	listen 	     80;
        server_name  localhost;
        #location /static {
        #        alias /mnt/hgfs/虚拟机共享文件夹/sweetshop/static;
        #    }

        #location / {
               # root /mnt/hgfs/虚拟机共享文件夹/sweetshop/static;
	       # index index.html index.htm;
	       
        #   }

	location / {
		# 包含 uwsgi 的请求参数
		include uwsgi_params;
		# 转交请求给uwsgi
		#uwsgi_pass 127.0.0.1:8080;
		uwsgi_pass sweetshop;
	}

	location /static {
		# 指定静态文件存放的目录
		alias /var/www/sweetshop/static/;
	}

	location = / {
		# 传递请求给静态文件服务器的nginx
		proxy_pass http://192.168.8.130;
	}

	error_page   500 502 503 504  /50x.html;
        location = /50x.html {
	        root   html;
            }

     }
        #listen       80;
        #server_name  localhost;

        #charset koi8-r;

        #access_log  logs/host.access.log  main;

        #location / {
        #    root   html;
        #    index  index.html index.htm;
        #}

        #error_page  404              /404.html;

        # redirect server error pages to the static page /50x.html
        #
        #error_page   500 502 503 504  /50x.html;
        #location = /50x.html {
        #    root   html;
        #}

        # proxy the PHP scripts to Apache listening on 127.0.0.1:80
        #
        #location ~ \.php$ {
        #    proxy_pass   http://127.0.0.1;
        #}

        # pass the PHP scripts to FastCGI server listening on 127.0.0.1:9000
        #
        #location ~ \.php$ {
        #    root           html;
        #    fastcgi_pass   127.0.0.1:9000;
        #    fastcgi_index  index.php;
        #    fastcgi_param  SCRIPT_FILENAME  /scripts$fastcgi_script_name;
        #    include        fastcgi_params;
        #}

        # deny access to .htaccess files, if Apache's document root
        # concurs with nginx's one
        #
        #location ~ /\.ht {
        #    deny  all;
        #}
    


    # another virtual host using mix of IP-, name-, and port-based configuration
    #
    #server {
    #    listen       8000;
    #    listen       somename:8080;
    #    server_name  somename  alias  another.alias;

    #    location / {
    #        root   html;
    #        index  index.html index.htm;
    #    }
    #}


    # HTTPS server
    #
    #server {
    #    listen       443 ssl;
    #    server_name  localhost;

    #    ssl_certificate      cert.pem;
    #    ssl_certificate_key  cert.key;

    #    ssl_session_cache    shared:SSL:1m;
    #    ssl_session_timeout  5m;

    #    ssl_ciphers  HIGH:!aNULL:!MD5;
    #    ssl_prefer_server_ciphers  on;

    #    location / {
    #        root   html;
    #        index  index.html index.htm;
    #    }
    #}

}

```

* 启动nginx

```bash
# 启动Nginx
sudo /usr/local/nginx/sbin/nginx
```

* 项目配置文件修改

```
1. 修改数据库配置信息
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'sweetshop',
        'HOST': 'localhost',
        'PORT': '3306',
        'USER': '#',  # 数据库用户名
        'PASSWORD': '#',  # 数据库密码
    }
}

2. 修改邮箱配置信息，163邮箱配置信息自查
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.qq.com'
EMAIL_PORT = 25
EMAIL_HOST_USER = 'xxxx@qq.com'  # 发送邮件的邮箱
EMAIL_HOST_PASSWORD = 'xxxx'  # qq邮箱授权码
# EMAIL_USE_TLS = True  # 与SMTP服务器通信时，是否启动TLS链接(安全链接)
EMAIL_FROM = '姜饼小屋<XXXXX@qq.com>'  # EMAIL_FROM 和 EMAIL_HOST_USER必须一样

4. 填写fdfs的配置信息，注意端口是nginx的端口
FDFS_STORAGE_URL = 'http://ip:port/'  

5. 支付功能不需要用到的保持默认即可，需要用到移步官方文档或看配置文件注释
```

* 迁移数据库

```
python manage.py makemigrations
python manage.py migrate
```

* 启动项目

```
# 创建超级管理员
python manage.py createsuperuser admin
# 缓存表
python manage.py createcachetable

# 开启外部访问
python manage.py runserver 0.0.0.0:8000

# 移动端输入ip地址进行访问，这样就可以正常访问了~
# 192.168.123.27:8000
```





## 3. 项目亮点

### 3.1 用户激活Celery

![](https://i.loli.net/2020/09/26/Wr3I9bKJ7NgBya1.png)

* 用户注册方面我的用户模型使用的是Django自带的AbstractUser，在取出用户注册的信息之后保存到数据库中。这里的用户激活要设为0，（user.is_active = 0  # 禁止激活），因为后续要发送激活邮件。

* 激活链接里包含用户的身份信息。用户的身份信息要进行加密。使用itsdangerous包，生成签名的token信息。

* 发送邮件使用django提供的邮件支持。django网站使用内置的send_mail进行发邮件，发送到SMTP服务器（我这里使用QQ邮箱），在setting中进行配置。之后发送到目的邮箱。

* 直接给SMTP服务器发邮件的话，这个时间是不确定的，如果有延迟，就会给用户带来一个不好的体验。我开始做出的一个版本就是每次点击注册都要等待7s左右才能跳转到登录界面。

* 为了解决上面的问题。我就使用了**celery**帮助我**异步**发送邮件。我使用redis作为中间人。启动`celery -A celery_tasks.tasks worker -l info`。celery我主要理解就是处理一些耗时的工作。

```
  serializer.dumps(info) # 进行加密
  serializer.load(token)  # 进行解密
```

### 3.2 用户登录

* 使用**redis作为Django缓存和session后端**。我知道django框架是默认将session保存到数据库中的，如果访问量很多，就会影响服务器的性能。因此我将session保存到redis中避免直接从数据库中读取session数据。
* 使用redis的好处：服务器数据非经常更新。若每次都从硬盘读取一次，浪费服务器资源、拖慢响应速度。而且数据更新频率较高，服务器负担比较大。若保存到数据库，还需要额外建立一张对应的表存储数据。在Django中建立表通常做法是建立一个模型。看似简单，问题调试麻烦、开发时长久。为了进行服务器的加速，使用Redis进行缓存。
* 用户退出的时候使用到了**logout函数清除用户的session信息**。

### 3.3 redis(6379)存储历史浏览记录:

* 在用户访问商品的详情页面的时候，需要添加历史浏览记录
* 在访问用户中心个人信息页的时候获取历史浏览记录
* 历史浏览记录保存在redis数据库中。因为历史浏览记录需要经常的读写。如果放在普通的mysql数据库中速度就会很慢，redis是内存型的数据库。
* redis中的数据类型：string、hash、list、set、zet
* 我将**每个**用户的历史浏览记录都用一条数据来保存。所以我选择了list。history_用户id : [商品id_2,1,3]。添加新的浏览记录是从列表的左侧进行添加（`conn.lpush(history_key, goods_id)`）。
* 只保存用户浏览的前5条信息`conn.ltrim(history_key, 0, 4)`

![](https://i.loli.net/2020/09/26/ZrIetd68qXwV7BC.png)

### 3.4 FastDFS

![](https://i.loli.net/2020/09/25/YSuqHCptXZvTeO5.png)

* tracker-server（跟踪服务器）和storage-server（存储服务器）

* tracker管理storage。

* FastDFS的**优点**就是海量存储，存储容量扩展方便，文件内容重复（hash值解决重复），可以结合nginx提高网站访问图片的效率

* Django将文件上传到FaseDFS系统中，FaseDFS会返回文件的ID保存到相关的数据表中。

* 创建Fdfs_client对象`client = Fdfs_client(self.client_conf)`

  上传文件到fast_dfs系统中`res = client.upload_by_buffer(content.read())`

* 当浏览器用户访问页面的时候，会返回nginx的端口号+文件id返回渲染页面。浏览器会访问fstdfs系统商品的nginx获取图片，之后nginx会返回图片显示在浏览器上。

### 3.5 redis保存购物车信息

* 当用户点击商品加入购物车的的时候需要添加购物车记录

* 当用户访问购物车页面时获取用户的购物车记录

* 每个用户的购物车记录用一条数据表示。使用hash

  `cart_用户id：｛"sku_id1":数量，"sku_id2":数量｝`

* 获取用户购物车中商品的条数：统计hash中元素的数量 hlen



### 3.6 页面静态化

![](https://i.loli.net/2020/09/25/PORvlcygud9hFIJ.png)

* 把原本的动态化页面处理结果保存成html文件，让用户直接访问这个生成出来的静态的html页面。用户访问的首页都是一样的。可以用静态页面**减轻网站的压力**。
* 当后台管理员修改首页中的数据的时候，django就给celery发送消息没让celery重新生成静态页面。静态页面生成后，用户就可以通过**nginx的80端口来访问这个静态页面**。
* 静态页面生成：当在django中修改数据的时候，**django会自动调用管理类中的save_model和delete_model**。我在save_model中添加了一个附加操作。让celery 重新生成静态页面。
* 生成一个首页的静态页面
* 当用户访问首页的时候，直接返回静态页面

- 什么时候需要重新生成静态页面

  **管理员在后台修改了页面上数据表里的信息的时候，需要重新生成静态页面。celery**

```python
# 在admin.py中
class BaseModelAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        """新增或更新表中的数据时调用"""
        super().save_model(request, obj, form, change)

        # 发出任务，让celery worker重新生成首页静态页
        from celery_tasks.tasks import generate_static_index_html
        generate_static_index_html.delay()

        # 清除首页的缓存数据
        cache.delete('index_page_data')
```

### 3.7 数据缓存

* 把页面用到的数据缓存起来，如果使用这些数据的时候，先从缓存中获取，如果获取不到，再去查询数据库

* 什么时候缓存数据需要更新？

  **管理员在后台修改了首页数据表里里的信息的时候，需要重新缓存数据**

* 网站本身性能的优化，减少数据库的查询次数

* 防止恶意的攻击。DDOS攻击

* `cache.delete('index_page_data')  # 清除首页的缓存数据`

* 没有缓存，就会重新在数据库中进行查询，也就重新进行缓存了

* 设置缓存cache.set()  cache.get()

### 3.8 商品搜索

1. 搜索引擎

   * 可以对表中的某些字段进行关键词分析，建立关键词对应的索引数据
   * 

2. 全文搜索框架

   * 帮助用户使用搜索引擎
   * 使用haystack框架+whoosh搜索引擎
   * 表单的提交方式为get，关键词name="q"
   * 搜索出结果后，haystack会把搜索出的结果传递给templates/search目录下的search.html，传递的上下文包括：
     * query：搜索关键字
     * page：当前页的page对象
     * paginator：分页
   * whoosh在进行分词的时候，有一些中文的词语分不清。所以要引入jieba分词。

   ![](https://i.loli.net/2020/09/26/RpcfSk6wrn8biel.png)

### 3.9 订单并发处理

* 在checkbox来说，选中的部分我给它一个name属性为“sku_ids”，没有被选中的值不会被提交，这样选择的商品才会被提交

* 用户每下一个订单就需要向订单表中加入一条记录

  用户的订单中的有几个商品，就需要向订单商品表中加入几条记录(遍历)

* 最后要清除购物车中的记录

  `conn.hdel(cart_key, *sku_ids)  # 拆包`

* 悲观锁：`select * from ss_goods_sku where id=sku_id for update; for update` 为加琐操作

* 悲观锁获取数据时对数据行了锁定，其他事务要想获取锁，必须等原事务结束。

* 乐观锁在查询数据的时候不加锁，在更新的时候进行判断，判断之前查出的库存和更新的库存是否一致。

  `update df_goods_sku set stock=0, sales=1 where id=17 and stock=1;`

* 处理订单并发的时候，我使用到了乐观锁和悲观锁。在冲突比较少的时候使用乐观锁，冲突比较多的时候，使用悲观锁。

* django2.0之后，mysql的默认隔离级别为读已提交。

* 订单支付对接了支付宝，用户点击支付宝沙箱接口。

![](https://i.loli.net/2020/09/26/A97Uwm4iTSPDJxR.png)

### 3.10 项目部署

* uwsgi遵循wsgi协议的web服务器

* nginx配置转发请求给uwsgi

  location / {

  ​	include uwsgi params;

  ​	uwsgi_pass uwsgi服务器的ip:port;

  }

* nginx配置处理静态文件

  在django setting.py 中配置收集静态文件路径

  STATIC_ROOT=收集的静态文件路径 例如:/var/www/sweetshop/static

  django收集静态文件的命令：`python3 manage.py collectstatic`

  就可以收集到STATIC_ROOT指定目录下

  收集完静态文件之后，让**nginx提供静态文件**，需要在nginx配置文件中加如下配置

  location /static {

  ​	alias /var/www/sweetshop/static/;

  }

* nginx转发请求给另外地址

  如果访问的是 / , 就去找静态页面服务器，如果访问其他再去找django服务器

  location = /{

  ​	proxy_pass http://172.16.179.21;

  }

* nginx配置upstream实现负载均衡

  nginx配置负载均衡时，在server配置的前面增加upstream配置项

  upstream sweetshop {

  ​	server 127.0.0.1:8080;

  ​	server 127.0.0.1:8081;

  }






项目架构: Django 2.2+ Python 3+ Nginx + Fast DFS + Redis + MySQL 
项目描述:基于B2C的电商销售系统,包含了实际开发中的电商项目中大部分的功能开发。
  项目技术点:

1. 使用 Haystack + Whoosh + jieba 全文检索框架,修改底层 haystack 使之对中文搜索更加友好。
2. 项目采用 Celery 负责用户注册异步发送邮件以及不同用户登陆系统动态生成首页。
3. 采用 FastDFS + Nginx 存储网站静态文件,实现项目和资源分离,达到分布式效果。
4. 数据库使用 Redis 作为 Django 缓存和 Session 存储后端,提升网站性能,提高用户体验。
5. 使用 Nginx + uWSGI 作为Web服务器, Nginx 配置 upstream 实现负载均衡





## 4. web项目开发流程

![1591694628100](https://upload-images.jianshu.io/upload_images/15729314-ad459951a7c4762f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

## 5. 需求分析

### 5.1 用户模块

1) 注册页

- 注册时校验用户名是否已被注册。
- 完成用户信息的注册。
- 给用户的注册邮箱发送邮件，用户点击邮件中的激活链接完成用户账户的激活。

![注册页](https://upload-images.jianshu.io/upload_images/15729314-9fe886bdd67898b0.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

2) 登录页

- 实现用户的登录功能。
- 如果用户忘记密码，会跳转到忘记密码页面，发送邮件重置密码

![登录页](https://upload-images.jianshu.io/upload_images/15729314-70aae577b22dcec7.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

3)重置密码页

- 实现用户的重置密码功能
- 用户填入自己的用户名和绑定的邮箱，如果正确，将给用户邮箱发送重置密码请求链接。
- 点击链接之后会跳转到重置密码页面进行密码重置。

![忘记密码](https://upload-images.jianshu.io/upload_images/15729314-15eeef4d5f14a54d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![image.png](https://upload-images.jianshu.io/upload_images/15729314-49b7002c94a11b6d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![image.png](https://upload-images.jianshu.io/upload_images/15729314-f12ec4bdbd837b0b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

4) 用户中心

- 用户中心信息页：显示登录用户的信息，包括用户名、电话和地址，同时页面下方显示出用户最近浏览的商品信息。

![个人信息页](https://upload-images.jianshu.io/upload_images/15729314-6c10e1b40fa19c98.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- 用户中心地址页：显示登录用户的默认收件地址，页面下方的表单可以新增用户的收货地址。

![用户地址](https://upload-images.jianshu.io/upload_images/15729314-20424d496b26dcb0.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- 用户中心订单页：显示登录用户的订单信息。

![用户订单](https://upload-images.jianshu.io/upload_images/15729314-34f99e184c4e9190.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

5) 其他

- 如果用户已经登录，页面顶部显示登录用户的信息。

![image.png](https://upload-images.jianshu.io/upload_images/15729314-2e2767dfd6816cef.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



### 5.2 商品相关

1) 首页

- 动态指定首页活动信息。

![](https://upload-images.jianshu.io/upload_images/15729314-c11c0adea50bb8cf.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- 动态获取商品的种类信息并显示。

![](https://upload-images.jianshu.io/upload_images/15729314-aa7f5d58c286ef06.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- 动态指定首页显示的每个种类的商品(包括图片商品和文字商品)。

![商品分类](https://upload-images.jianshu.io/upload_images/15729314-525faf78f19cd663.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- 点击某一个商品时跳转到商品的详情页面。

![商品详情](https://upload-images.jianshu.io/upload_images/15729314-55b0c5a2524558f6.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

2) 商品详情页

- 显示出某个商品的详情信息。

![商品详情](https://upload-images.jianshu.io/upload_images/15729314-55b0c5a2524558f6.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- 页面的左下方显示出该种类商品的2个新品信息。

![](https://upload-images.jianshu.io/upload_images/15729314-506b9bedeb65be09.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

3）商品列表页

- 显示出某一个种类商品的列表数据，分页显示并支持按照默认、价格、和人气进行排序。

![image.png](https://upload-images.jianshu.io/upload_images/15729314-2e5fb3e5834f1cb9.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- 页面的左下方显示出该种类商品的2个新品信息。

![image.png](https://upload-images.jianshu.io/upload_images/15729314-4cbc4bf06618f25e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

4）其他

- 通过页面搜索框搜索商品信息。

![image.png](https://upload-images.jianshu.io/upload_images/15729314-4e49d7eadb7f4c10.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

### 5.3 购物车相关

- 列表页和详情页将商品添加到购物车。

![image.png](https://upload-images.jianshu.io/upload_images/15729314-90429bcd7167d285.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- 用户登录后，首页，详情页，列表页显示登录用户购物车中商品的数目。

![image.png](https://upload-images.jianshu.io/upload_images/15729314-70659094b51db571.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- 购物车页面：对用户购物车中商品的操作。如选择某件商品，增加或减少购物车中商品的数目。

![image.png](https://upload-images.jianshu.io/upload_images/15729314-00dc4d753ccce2de.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

### 5.4 订单相关

- 提交订单页面：显示用户准备购买的商品信息。

![image.png](https://upload-images.jianshu.io/upload_images/15729314-7e1b914f5fe51e9a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- 点击提交订单完成订单的创建。
- 用户中心订单页显示用户的订单信息。

![image.png](https://upload-images.jianshu.io/upload_images/15729314-4b3ad1e5078d6891.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- 点击支付完成订单的支付。

![image.png](https://upload-images.jianshu.io/upload_images/15729314-265b7ef6691020f5.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- 对于完成支付的订单。用户可以在订单页进行订单评论，评论会显示在商品页面的评论区。



## 6. 数据库表

![数据库表图](https://upload-images.jianshu.io/upload_images/15729314-e6921d318ff6867f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

