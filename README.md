# 姜饼小屋项目总结 — Django2.2版本

## 1. 简介

本项目采用django2.2.0，该项目包含了实际开发中的电商项目中大部分的功能开发和知识点时间。在此记录一个多月以来走过这个项目的过程，包括 django 版本问题的坑等等，希望自己在程序媛的道路上越走越远╭(′▽`)╯。

关键词：django2  celery fdfs haystack whoosh redis ngnix 高并发 分布式



## 2. 姜饼小屋商业模式

姜饼小屋采用B2C的商业模式。B2C 是 Business-to-Customer 的缩写，而其中文简称为“商对客”。“商对客”是电子商务的一种模式，也就是通常说的直接面向消费者销售产品和服务商业零售模式。这种形式的电子商务**一般以网络零售业**为主，主要借助于互联网开展在线销售活动。

**B2C 即企业通过互联网为消费者提供一个新型的购物环境**——网上商店，消费者通过网络在网上购物、网上支付等消费行为。 

**案例:唯品会、乐蜂网**



## 3. web项目开发流程

![1591694628100](https://upload-images.jianshu.io/upload_images/15729314-ad459951a7c4762f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

## 4. 需求分析

### 4.1 用户模块

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



### 4.2 商品相关

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

### 4.3 购物车相关

- 列表页和详情页将商品添加到购物车。

![image.png](https://upload-images.jianshu.io/upload_images/15729314-90429bcd7167d285.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- 用户登录后，首页，详情页，列表页显示登录用户购物车中商品的数目。

![image.png](https://upload-images.jianshu.io/upload_images/15729314-70659094b51db571.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- 购物车页面：对用户购物车中商品的操作。如选择某件商品，增加或减少购物车中商品的数目。

![image.png](https://upload-images.jianshu.io/upload_images/15729314-00dc4d753ccce2de.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

### 4.4 订单相关

- 提交订单页面：显示用户准备购买的商品信息。

![image.png](https://upload-images.jianshu.io/upload_images/15729314-7e1b914f5fe51e9a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- 点击提交订单完成订单的创建。
- 用户中心订单页显示用户的订单信息。

![image.png](https://upload-images.jianshu.io/upload_images/15729314-4b3ad1e5078d6891.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- 点击支付完成订单的支付。

![image.png](https://upload-images.jianshu.io/upload_images/15729314-265b7ef6691020f5.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- 对于完成支付的订单。用户可以在订单页进行订单评论，评论会显示在商品页面的评论区。



## 5. 数据库表

![数据库表图](https://upload-images.jianshu.io/upload_images/15729314-e6921d318ff6867f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

