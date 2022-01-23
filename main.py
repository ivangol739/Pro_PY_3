import requests
from bs4 import BeautifulSoup

ret = requests.get('https://habr.com/ru/all/')
soup = BeautifulSoup(ret.text, 'html.parser')
posts = soup.find_all('article')

KEYWORDS = ['дизайн', 'фото', 'web', 'python', 'IT-компании', 'Docker']
KEYWORDS = set(map(str.lower, KEYWORDS))

post_list = []
for post in posts:
    post_dict = {}
    preview = post.text.strip().split()
    preview_text = set(map(str.lower, preview))
    hubs = post.find_all('a', class_="tm-article-snippet__hubs-item-link")
    post_hubs = set([hub.find('span').text.lower() for hub in hubs])
    if KEYWORDS & preview_text or KEYWORDS & post_hubs:
        title = post.find('h2')
        url = 'https://habr.com' + title.find('a').attrs['href']
        data = post.find('span', class_="tm-article-snippet__datetime-published").find('time')['title'][0:10]
        post_dict['data'] = data
        post_dict['title'] = title.text
        post_dict['url'] = url
        post_list.append(post_dict)
print(post_list)
