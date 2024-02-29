import lxml
import requests
from bs4 import BeautifulSoup
import csv
import time


def get_soup(url):  # функция создания супа ленты RSS
    response = requests.get(url=url)
    response.encoding = 'utf-8'
    return BeautifulSoup(response.content, 'xml')


def split_description(text):  # функция текстового среза значений нужных подтайтлов, т.к. они находятся внутри
    # description
    start = description[description.find(text):]  # ищу вход нужного подтайтла в строке
    return start[start.find(':') + 1:start.find(';')]  # обрезаю нужный текст подтайтла и возвращаю до разделителя ;


def csv_writer(filename, data):
    with open(filename, 'a', encoding='utf-8', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(data)


u = 'https://www.upwork.com/ab/feed/jobs/rss?paging=0%3B10&sort=recency&api_params=1&q=&securityToken=959001d70e2ea' \
    '935e7fc3a0c2291d9464192ef78be7e3ea5fd499a6eaf77b096594d7f460aa08a8411f6383cece2144268650464c330f7efba57922a476' \
    'a3b96&userUid=1661145749274374144&orgUid=1661145749274374145'
counter = []  # лист-счетчик уникальных ссылок вакансий
run_time = 24 * 60 * 60
start_time = time.time()  # время старта
timeout = 30  # таймаут чтения RSS-ленты

with open('UW_rss_2802.csv', 'w', encoding='utf-8', newline='') as file:  # прописываю заголовки файла
    writer = csv.writer(file, delimiter=';')
    writer.writerow(['Posted On', 'Title', 'Category', 'Skills', 'Full Description', 'Country', 'Link'])
while time.time() - start_time < run_time:  # цикл на run_time
    soup = get_soup(u)
    for item in soup.findAll('item'):

        description = BeautifulSoup(item.description.text.replace('<br /><b>', '; '),
                                    "html.parser").get_text()  # здесь я
        # заранее заменяю некоторое сочетание html тегов разделителем (;), чтобы удобнее было срезать нужные мне
        # подтайтлы, и достаю текст
        posted = split_description('Posted On')
        category = split_description('Category')
        skills = split_description('Skills')
        country = split_description('Country')
        title = item.title.text
        link = item.link.text

        if link not in counter:  # если текущая ссылка уже присутствует в листе-счетчике, то данные по этой вакансии
            # не будут записываться в файл csv
            csv_writer('UW_rss_2802.csv', [posted, title, category, skills, description, country, link])
            counter.append(link)
    print(f'Total links: {len(counter)}')
    print(f'Elapsed time: {(time.time() - start_time) / 3600}')
    time.sleep(timeout)
