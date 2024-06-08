import requests as re
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import os

def fetch_url(url):
    response = re.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    return soup

def ptt_potential_stock_parser():
    post_obj = {}
    base_url = 'https://www.ptt.cc/'
    target_url = 'bbs/Stock/index.html'
    
    latest_date = datetime.now()
    end_date = latest_date - timedelta(days=6)
    
    while latest_date > end_date:
        i=0
        sp = fetch_url(base_url + target_url)
        target_url = sp.find_all('a', class_='btn wide')[1]['href']
        title_lst = sp.find_all('div', class_='title')
        date_lst = sp.find_all('div', class_='date')
    
        for title,date in zip(title_lst,date_lst):
            a_tag = title.find('a')
            if not a_tag:
                continue
            post_url = a_tag['href']
            post_title = a_tag.text.strip()
            post_date = date.text.strip()
    
            post_obj[post_url] = {'title': post_title, 'date': post_date, 'url': post_url}
            #print(post_obj[post_url])
    
            if '公告' in post_title or '閒聊' in post_title or '行事曆' in post_title:
                continue
    
            latest_date = datetime.strptime(f'{latest_date.year}/{post_date}', '%Y/%m/%d')
            i+=1
            print(i," ", post_title, " ", post_date," ", post_url)
    msg = "\n"
    
    for post_url in post_obj:
        # print(post_url)
        post_detail = post_obj[post_url]
        if '標的' in post_detail['title']:
            post_content = fetch_url(base_url + post_url)
            potential_score = 0
            comment_lst = post_content.find_all('div', class_='push')
            i=0
            for comment in comment_lst:
                if '低調' in comment.text.strip():
                    # print("低調")
                    potential_score += 1
            # print("potential_score = ", potential_score)
            if potential_score >= 1:
                msg += f"{post_detail['title']} {potential_score}\n"
    print(msg)

if __name__ == "__main__":
    ptt_potential_stock_parser()
