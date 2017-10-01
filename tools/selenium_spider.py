# -*- coding: utf-8 -*-

from selenium import webdriver

chrome_opt = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images": 2}
chrome_opt.add_experimental_option("prefs", prefs)
browser = webdriver.Chrome(executable_path='/Users/pangxing/bin/chromedriver', chrome_options=chrome_opt)


browser.get('http://list.jd.com/list.html?cat=9987,653,655&page=1&stock=0&sort=sort_rank_asc')
print browser.page_source