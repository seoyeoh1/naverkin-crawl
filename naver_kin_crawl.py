#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup as bs
import time
import re
import requests
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import NoSuchElementException

driver = webdriver.Chrome('/chromedriver')
urls = []
date = [] # list of dates for desired query span (year.mm.dd)

# 지식인 검색 결과 URL 주소 추출
for k in date[:]:
    i = 1
    while i <= 100:
        driver.get("https://search.naver.com/search.naver?where=kin&kin_display=10&qt=&title=0&&answer=0&grade=0&choice=0&sec=0&nso=so%3Ar%2Ca%3Aall%2Cp%3Afrom{}to{}&query=%EC%BD%94%EB%A1%9C%EB%82%98+%EA%B0%80%EB%8A%A5%ED%95%9C%EA%B0%80%EC%9A%94&c_id=&c_name=&sm=tab_pge&kin_start={}".format (k, k, (i-1)*10 + 1))
        time.sleep(3)
        html = driver.page_source
        soup = bs(html, 'html.parser')
        questions = soup.select("dt.question")
        for question in questions[:]:
            url = question.find("a")["href"]
            urls.append(url)
        i = i + 1
driver.close()

# 지식인 Q&A 크롤링

driver = webdriver.Chrome('/Users/SeoyeonHong/Downloads/chromedriver')
with open("file_name.txt") as sample:
    urls = []
    for line in sample:
        urls.append(line.rstrip())
    print(len(urls))

q_title = []
q_content = []
answer = []
like = []
useful = []
haha = []
toobad = []
likead = []

def naver_kin_crawler(url):
    driver.get(url)
    time.sleep(5)
    html = driver.page_source
    soup = bs(html, "html.parser")
    # 질문 제목
    q_title_elem = soup.select("div.c-heading__title")[0]
    q_title_ = q_title_elem.get_text().strip()
    q_title.append(q_title_)
    # 질문 본문
    try:
        q_content_ = q_title_elem.find_next_sibling('div').get_text().strip()
    except AttributeError:
        q_content_ = " "
    q_content.append(q_content_)
    # 답변
    answers = soup.select("span.se-fs-.se-ff-")
    answer_ = " "
    for item in answers:
        i = str(item.get_text()) + " "
        i = i.replace('\u200b','')
        answer_ += i
    answer.append(answer_)
    # 답변 반응
    like_ = soup.find('li', {'class':'u_likeit_list like'}).get_text().strip()
    like_ = ''.join(filter(str.isdigit, like_))
    like.append(like_)
    useful_ = soup.find('li', {'class':'u_likeit_list useful'}).get_text().strip()
    useful_ = ''.join(filter(str.isdigit, useful_))
    useful.append(useful_)
    haha_ = soup.find('li', {'class':'u_likeit_list haha'}).get_text().strip()
    haha_ = ''.join(filter(str.isdigit, haha_))
    haha.append(haha_)
    toobad_ = soup.find('li', {'class':'u_likeit_list toobad'}).get_text().strip()
    toobad_ = ''.join(filter(str.isdigit, toobad_))
    toobad.append(toobad_)
    try:
        likead_ = soup.find('li', {'class':'u_likeit_list likead _button off'}).get_text().strip()
        likead_ = ''.join(filter(str.isdigit, likead_))
    except AttributeError:
        likead_ = soup.find('a', {'class':'u_likeit_list_button _button off'}).get_text().strip()
        likead_ = ''.join(filter(str.isdigit, likead_))
    likead.append(likead_)

for url in urls[:]:
    naver_kin_crawler(url)

driver.close()

# 수집한 데이터를 .csv로 저장
data_ = zip(urls, q_title, q_content, answer, like, useful, haha, toobad, likead)
df = pd.DataFrame(data = data_, columns=["url", "q_title", "q_content", "answer", "like", "useful", "haha", "toobad", "likead"])
df.to_csv("file_name.csv")

# etc

def search_jisikin(query):
    """지식인 검색"""
    elem_search = driver.find_element_by_class_name("search_input")
    elem_search_input = driver.find_element_by_class_name("search_btn")
    elem_search.send_keys(query)
    elem_search_input.click()

def set_span(from_date, to_date):
    """지식인에서 키워드 검색 이후 검색 결과 기간 설정"""
    select_span = driver.find_element_by_class_name("selectbox-box")
    span_input = driver.find_element_by_class_name("selectbox-notclose _nclicks:kin.dateinput selectbox-item selectbox-item-selected selectbox-item-over")
    elem_from_date = driver.find_element_by_id("sel_from_date")  
    select_span.click()
    span_input.click()
    elem_from_date.send_keys(Keys.DELETE)
    elem_from_date.send_keys(from_date)
    actions.send_keys(Keys.TAB).perform()
    actions.send_keys(Keys.DELETE).perform()
    actions.send_keys(to_date).perform()
    actions.send_keys(Keys.Return).perform()
