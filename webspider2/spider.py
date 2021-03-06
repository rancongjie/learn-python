import re
import requests


class spider(object):
    def __init__(self):
        print(u'开始爬取内容')

    def getsource(self, url):
        html = requests.get(url)
        return html

    def changepage(self, url, total_page):
        now_page = int(re.search('pageNum=(\d+)', url, re.S).group(1))
        page_group = []
        for i in range(now_page, total_page + 1):
            link = re.sub('pageNum=\d+', 'pageNum=%d' % i, url, re.S)
            page_group.append(link)
        return page_group

    def geteveryclass(self, source):
        everyclass = re.findall('<li id=.*?>(.*?)</li>', source, re.S)
        return everyclass

    def getinfo(self, eachclass):
        info = {}
        info['title'] = re.search('<h2 class="lesson-info-h2"><a .*?>(.*?)</a></h2>', eachclass, re.S).group(1)
        info['content'] = re.search('<p style="height: 0px; opacity: 0; display: none;">\s(.*?)</p>', eachclass,re.S).group(1)
        timeandlevel = re.findall('<em>(.*?)</em>', eachclass, re.S)
        info['classtime'] = timeandlevel[0]
        info['classlevel'] = timeandlevel[1]
        info['learnnum'] = re.search('"learn-number">(.*?)</em>', eachclass, re.S).group(1)
        return info

    def saveinfo(self, classinfo):
        f = open('info.txt', 'a')
        for each in classinfo:
            f.writelines('title:' + each['title'] + '\n')
            f.writelines('content:' + each['content'] + '\n')
            f.writelines('classtime:' + each['classtime'] + '\n')
            f.writelines('classlevel:' + each['classlevel'] + '\n')
            f.writelines('learnnum:' + each['learnnum'] + '\n\n')
        f.close()


if __name__ == '__main__':
    classinfo = []
    url = 'http://www.jikexueyuan.com/course/?pageNum=1'
    jikespider = spider()
    all_links = jikespider.changepage(url, 5)
    for link in all_links:
        print(u'正在处理页面：' + link)
        html = jikespider.getsource(link)
        everyclass = jikespider.geteveryclass(html.text)
        for each in everyclass:
            info = jikespider.getinfo(each)
            classinfo.append(info)
    jikespider.saveinfo(classinfo)
