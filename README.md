## 功能
在图像上寻找特定关键词，该项目基于项目[https://github.com/yfq512/img2words] 提供的文字提取服务，使用热更新后，需调用post.py调用的接口，热更新才完全生效，该项目已基于Flask实现web服务

## 环境

## 运行
python server_word2.py

## API文档
* 寻找关键词：http://wiki.ccwb.cn/web/#/73?page_id=2345
* 热更新-添加词：http://wiki.ccwb.cn/web/#/73?page_id=2258
* 热更新-删除词：http://wiki.ccwb.cn/web/#/73?page_id=2348

## 其他
* 创建文件夹：delkeywords（用于暂存删除词数据），updatawords（用于暂存添加词数据），images（用于暂存被提取图像），keywords（用于存放搜集到的“关键词”txt文件，每行储存一个关键词）
* post.py # 寻找关键词调用示例 
* post2.py # 热更新-添加词调用示例
* post3.py # 热更新-删除词调用示例
