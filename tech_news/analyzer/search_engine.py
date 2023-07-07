from tech_news.database import search_news
from datetime import datetime


# Requisito 7
def search_by_title(title):
    data_news = search_news({"title": {"$regex": title, "$options": "i"}})

    result = [(news["title"], news["url"]) for news in data_news]
    return result


# Requisito 8
def search_by_date(date):
    try:
        iso_date = datetime.strptime(date, "%Y-%m-%d")
        valid_date = datetime.strftime(iso_date, "%d/%m/%Y")

        data_news = search_news({"timestamp": valid_date})
        result = [(news["title"], news["url"]) for news in data_news]
        return result
    except ValueError:
        raise ValueError('Data inválida')


# Requisito 9
def search_by_category(category):
    data = search_news({"category": {"$regex": category, "$options": "i"}})

    result = [(news["title"], news["url"]) for news in data]
    return result
