selenium for taobao.com
对淘宝商品数据进行爬虫

../TaobaoProducts/tbspider.py
利用账号密码对taobao.com进行模拟登录，输入要爬虫的商品，并将爬虫的结果存储在MongoDB中
iteration
demo现只爬虫天猫数据，商品的sid存储在MongoDB中

../TaobaoProducts/tmall.py
根据爬取的淘宝天猫商品的sid，对商品详情页面的详情图进行下载并保存本地
iteration
demo现只爬虫商品详情页的详情图，详情页面的主图暂时还不能下载

../TaobaoProducts/dbconfig.py
本地数据库MongoDB的配置文件以及相关的存取函数
