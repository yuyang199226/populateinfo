'''爬取诗人的基本信息'''
import requests
from bs4 import BeautifulSoup
from gevent import monkey;monkey.patch_all()
import gevent
import timeit
from gevent.pool import Pool



def parse_author_home(html,url=None):
    soup = BeautifulSoup(html, 'lxml')
    main3 = soup.find(class_='main3')  # >.right div.cont>a'
    a_tags = main3.find(class_='right').find('div', class_='cont').find_all('a')
    author_urls = []
    for a in a_tags:
        auth_url = url + a.attrs['href'][1:]
        name = str(a.string).strip()
        tmp = {'name': name, 'url': auth_url}
        author_urls.append(tmp)
    return author_urls

def parse_author_bio(html,url=None):
    '''爬取作者详细页面的简介，头像链接，典故没爬'''
    soup = BeautifulSoup(html, 'lxml')
    name = soup.find('h1').string.strip()
    main3 = soup.find(class_='main3')
    bio = main3.find(class_='left').find('div', class_='cont').find('p').string.strip()  #作者生平简介
    bio = str(bio)
    try:
        img_link = main3.find(class_='left').find('div', class_='cont').find('img').attrs['src']
    except AttributeError:
        img_link = None
    return {
        'name':name,
        'profile':bio,
        'quotation':None,
        'img_link':img_link}



def get_html(url):
    headers={
        'Uesr-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0',
        'Host':'so.gushiwen.org',
    }
    response = requests.get(url=url,headers=headers)
    print(response.status_code)
    print(response.encoding)
    return response.text

def parse_html(html,url=None,func=None):
    data = func(html,url)
    return data


def clean_data(data):
    pass

def main():
    '''函数入口'''
    root_url = 'http://so.gushiwen.org/'
    url = 'http://so.gushiwen.org/authors/'
    html = get_html(url)
    author_urls = parse_html(html,url=root_url,func=parse_author_home)

    ls_authors_info = []
    #同步调用开始
    # for dic in author_urls:
    #     html = get_html(dic['url'])
    #     data = parse_html(html,func=parse_author_bio)
    #     ls_authors_info.append(data)
    #同步调用结束

    # 协程池开始
    pool=Pool(80)
    jobs = [pool.spawn(get_html,i['url']) for i in author_urls]
    complete_jobs = gevent.joinall(jobs)
    for g in complete_jobs:
        data = parse_html(g.value,func=parse_author_bio)
        ls_authors_info.append(data)
    #协程池结束
    return ls_authors_info

if __name__ == '__main__':
    main()


