import urllib2
import re
import os
import urlparse
import sys
from bs4 import BeautifulSoup

# __author__:chenyuepeng

"""
This demon is a webspider to get a novel from https://www.qu.la
"""


def download(url, num_retries=5):
    """
    :param url: the fist chapter's url of novel like 'https://www.qu.la/book/25877/8923073.html'
    :param num_retries: times to retry to reconnect when fail to connect
    :return:html of url which be inputted
    """
    print 'Start downloading:', url
    try:
        html = urllib2.urlopen(url).read()
        print 'Download finished:', url
    except urllib2.URLError as e:
        print 'Download fail.Download error:', e.reason
        html = None
        if num_retries > 0:
            print 'Retrying:', url
            html = download(url, num_retries - 1)
    return html


def get_title(html):
    """Find Title of each chapter,return the title of chapter
    """
    title_regex = re.compile('<h1>(.*?)</h1>', re.IGNORECASE)
    title = str(title_regex.findall(html)[0])
    return title


def get_content(html):
    """get content of each chapter from the html
    """
    soup = BeautifulSoup(html, 'html.parser')
    # fixed_html = soup.prettify()
    div = soup.find('div', attrs={'id': 'content'})
    [s.extract() for s in soup('script')]
    # print div
    content = str(div).replace('<br/>', '\n').replace('<div id="content">', '').replace('</div>', '').strip()
    return content


def get_linkofnextchapter(html):
    """This method will get the url of next chapter
    :return: a relative link of the next chapter
    """
    soup = BeautifulSoup(html, 'html.parser')
    a = soup.find('a', attrs={'class': 'next', 'id': 'A3', 'target': '_top'})
    # print a['href']
    return a['href']


def save(title, content):
    with open(r'C:\Users\admin\Desktop\DNAofSuperGod\novel.txt', 'a+') as f:
        f.writelines(title + '\n')
        f.writelines(content + '\n')


def begin(url):
    # make sure panth exited
    if not os.path.isdir(r'C:\Users\admin\Desktop\DNAofSuperGod'):
        os.mkdir(r'C:\Users\admin\Desktop\DNAofSuperGod')
    # remove old file and build a new one
    if os.path.isfile(r'C:\Users\admin\Desktop\DNAofSuperGod\novel.txt'):
        os.remove(r'C:\Users\admin\Desktop\DNAofSuperGod\novel.txt')
    html = download(url)
    # if html is None,download fail.
    if not html == None:
        title = get_title(html)
        print title
        content = get_content(html)
        save(title, content)
        print 'Have saved %s for you.' % title
        link = get_linkofnextchapter(html)
        # judge if has next chapter?
        if not re.match(r'./', link):
            nexturl = urlparse.urljoin(url, link)
            begin(nexturl)
        else:
            print 'Save finished!'
    else:
        print 'Download fail'


# change recursion depth as 10000(defult is 900+)
sys.setrecursionlimit(10000)
url = 'https://www.qu.la/book/25877/8923072.html'
begin(url)