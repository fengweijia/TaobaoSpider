#！/usr/bin/env python
# -*- coding:utf-8 -*-
# https://www.jianshu.com/p/32f0755de50b

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from pyquery import PyQuery as pq
import time
from dbconfig import *


class TBSpider(object):
    def __init__(self):
        self.driver = webdriver.Chrome()
        #self.driver.maximize_window()
       
        # 设置一个智能等待
        self.wait = WebDriverWait(self.driver,10)

    def Index_Page(self,page):
        """
        爬虫抓取的索引页
        :param page: 页码
        """
        print('正在爬取第',page,'页')

        try:
            if page > 1:
                page_input = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-pager div.form > input')))
                page_submit = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-pager div.form > span.btn.J_Submit')))
                page_input.clear()
                page_input.send_keys(page)
                page_submit.click()
                time.sleep(10)

            self.wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR,'#mainsrp-pager li.item.active > span'),str(page)))
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'.m-itemlist .items .item')))
            self.Spider_Details()
        except TimeoutException:
            print("当前页数据爬虫失败")

    def Spider_Details(self):
        """
        提起淘宝商品数据
        """
        html = self.driver.page_source
        doc = pq(html)
        items = doc('#mainsrp-itemlist .items .item').items()
        for item in items:
            product = {
                    'image': item.find('.pic .img').attr('data-src'),
                    'price': item.find('.price').text(),
                    'deal': item.find('.deal-cnt').text(),
                    'title': item.find('.title').text(),
                    'shop': item.find('.shop').text(),
                    'location': item.find('.location').text(),
                    'data_sid': item.find('.pic-link').attr('data-nid')
                    }
            print(product)
            tb_db.save_to_mongo(product)

    def TB_Login(self,key,pw):
        url = 'https://login.taobao.com/member/login.jhtml'
        self.driver.get(url)
        try:
            # 寻找密码登陆按钮
            login_links = self.wait.until(
                EC.presence_of_element_located((By.XPATH,"//a[text()='密码登录']"))
            )
            login_links.click()
        except TimeoutException as e:
            print("找不到登陆入口，原因是：",e)
        else:
            # 输入账号密码
            input_key = self.wait.until(
                EC.presence_of_element_located((By.XPATH,"//input[@name='TPL_username']"))
            )
            input_pw = self.wait.until(
                EC.presence_of_element_located((By.XPATH,"//input[@name='TPL_password']"))
            )
            input_key.clear()
            input_pw.clear()
            input_key.send_keys(key)
            input_pw.send_keys(pw)

            # 定位滑块位置，滑动滑块
            src_loc = self.driver.find_element_by_xpath("//*[@id='nc_1_n1z']")
            ActionChains(self.driver).drag_and_drop_by_offset(src_loc,298,0).perform()

            self.driver.find_element_by_xpath('//*[@id="J_SubmitStatic"]').click()
            
            try:
                #  点击支付宝登录，用支付宝的方式进行登录
                self.driver.find_element_by_xpath("//*[@id='J_OtherLogin']/a[2]").click()
                print('支付宝方式登录淘宝')
                self.driver.find_element_by_xpath("//*[@id='J-loginMethod-tabs']/li[2]").click()
                zfb_input_key = self.wait.until(EC.presence_of_element_located((By.XPATH,"//*[@id='J-input-user']")))
                zfb_input_key.clear()
                for i in key:
                    zfb_input_key.send_keys(i)
                    time.sleep(0.5)
                zfb_input_pw = self.wait.until(EC.presence_of_element_located((By.XPATH,"//*[@id='password_rsainput']")))
                zfb_input_pw.clear()
                for i in pw:
                    zfb_input_pw.send_keys(i)
                    time.sleep(0.5)
                self.driver.find_element_by_xpath('//*[@id="J-login-btn"]').click()
                time.sleep(10)
                # 点击进入淘宝首页
                self.driver.find_element_by_xpath('//*[@id="J_SiteNavHome"]/div/a/span').click()
                time.sleep(10)
                detail_input = self.wait.until(EC.presence_of_element_located((By.XPATH,"//*[@id='q']"))) 
                detail_input.clear()
                detail_product = input("请输入要爬虫的商品： ").strip()
                detail_input.send_keys(detail_product)
                self.driver.find_element_by_xpath('//*[@id="J_TSearchForm"]/div[1]/button').click()
                time.sleep(10)
                # 点击天猫按钮
                self.driver.find_element_by_xpath('//*[@id="tabFilterMall"]').click()
                time.sleep(10)

            except TimeoutException:
                print("淘宝taobao.com登录失败")

if __name__ == '__main__':
    start_t = time.time()
    tb_item = TBSpider()
    tb_db = MongDB()

    tb_item.TB_Login('feng409231@163.com','fengweijia409231')
    tb_item.Index_Page(1)

    print('登录完成，耗时{:.2f}秒'.format(float(time.time()-start_t)))
