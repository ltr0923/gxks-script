### 高校考试网（卓越考试平台）刷视频脚本

🎉免费开源🎉www.gaoxiaokaoshi.com 自动刷课脚本，全自动刷课，省心，安心，放心。
------------------------------------------------------------------------------

### 如何使用

- 最简单的使用方法：直接下载对应的exe文件，运行后按照提示输入账号细信息即可
- 或者运行python源文件，源码下载到本地，使用python运行即可，但是需要在控制台依次安装运行所需的第三方库

  ```text
  pip install requests
  pip install lxml
  ```

  建议使用pycharm按照提示安装所需要的第三方库，运行脚本
  **注：嫌麻烦可直接运行exe文件，可达到所有的效果。**

### 文件说明

- GXKSscript终极版.py，通用的，默认刷所有课程（所有视频）到满时间。

### 原理

脚本原理：账号成功登录后，获取所有的视频的参数信息，如果有没有完成的视频，将没有完成的视频进行刷课，已完成的视频则不在进行刷课。
刷课原理：通过分析正常观看时视频时，浏览器向对应的服务器发送的http请求。间歇的伪造http请求去欺骗服务器，就可以达到刷课的目的。

### 说明

本仓库仅进行技术分析与实现，不进行任何的非法牟利，严守中国法律。如果有侵权可联系作者进行删除。

### 支持

在使用过程中有任何的问题，可联系作者邮箱。
如果你想支持作者的学习，可以给作者来一杯卡布奇诺。

### 作者

author: AlwaysLazy21   
email: kunkun317@qq.com   

支持作者   
<img src="./支付宝.jpg" width="60%"/>