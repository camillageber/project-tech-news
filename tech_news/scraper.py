# Requisito 1
import requests
from parsel import Selector
from requests.exceptions import ConnectionError, ReadTimeout
import time

from tech_news.database import create_news


def fetch(url):
    """Busca uma URL para realizar o scrape"""
    time.sleep(1)
    HEADERS = {"user-agent": "Fake user-agent"}

    try:
        res = requests.get(url, headers=HEADERS, timeout=3)
    except (ConnectionError, ReadTimeout):
        return None

    if res.status_code == 200:
        return res.text
    return None


# Requisito 2
def scrape_updates(url_content):
    """Faz o scrape da página Novidades para obter as URLs das notícias"""
    selector = Selector(url_content)
    urls = selector.css("a.cs-overlay-link ::attr(href)").getall()
    return urls


# Requisito 3
def scrape_next_page_link(url_content):
    """Busca o link da próxima página"""
    selector = Selector(url_content)
    next_page = selector.css("a.next.page-numbers ::attr(href)").get()
    return next_page


# Requisito 4
def scrape_news(url_content):
    """Retorna os dados buscados pelo scrape sobre uma matéria"""
    selec = Selector(text=url_content)
    url = selec.css("head > link[rel='canonical'] ::attr(href)").get()
    title = selec.css("h1.entry-title ::text").get().strip()
    writer = selec.css("a.url.fn.n ::text").get()
    timestamp = selec.css("li.meta-date ::text").get()
    reading_time = int(
        selec.css("li.meta-reading-time *::text").get().split()[0]
    )
    category = selec.css("span.label ::text").get()
    summary = selec.css("div.entry-content > p:nth-of-type(1) ::text").getall()

    data_data_result = {
        "url": url,
        "title": title,
        "writer": writer,
        "timestamp": timestamp,
        "reading_time": reading_time,
        "summary": "".join(summary).strip(),
        "category": category,
    }
    return data_data_result


# Requisito 5
def get_tech_news(amount):
    """Busca dados dos links de todas as páginas e insere no banco de dados"""
    url_base = "https://blog.betrybe.com/"
    links_list = []
    data_result = []

    while len(links_list) < amount:
        html = fetch(url_base)
        links_list += scrape_updates(html)
        next = scrape_next_page_link(html)
        url_base = next

    for link in links_list:
        if len(data_result) == amount:
            break
        data_result.append(scrape_news(fetch(link)))

    create_news(data_result)

    return data_result
