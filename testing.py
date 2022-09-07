from bs4 import BeautifulSoup
import requests
import cardmarket_resources
from data_classes import CardArticle
from data_classes import Card

def is_filtered_language_in_sold_cards(card_article_list, language):
    for article in card_article_list:
        if article.language == language:
            return True

    return False

'https://www.cardmarket.com/de/Magic/Products/Singles?idExpansion=0&searchString=test&idRarity=0&perSite=30'

base_url = 'https://www.cardmarket.com'
mtg_singles_subpath = 'Magic/Products/Singles'
site_lang_prefix = '/en/'
seller_country = '7'

test_card = Card('Mana Crypt', '3', '0', '0', [])

search_url = base_url + site_lang_prefix + mtg_singles_subpath + '?' + 'idExpansion=' + test_card.expansion_id +'&searchString=' + test_card.name + '&idRarity=' + test_card.rarity + 'perSite=30'

#print(search_url)

page = requests.get(search_url)
soup = BeautifulSoup(page.content, "html.parser")

search_results = soup.findAll('div', id=lambda x: x and x.startswith('productRow'))

for card_result in search_results:
    card_result_link = base_url + [a['href'] for a in card_result.find_all('a', href=True) if a.text][0]
    filtered_card_result_link = card_result_link + '?' + 'sellerCountry=' + seller_country + '&' + 'language=' + test_card.language_id

    # HAVE TO CHECK LANGUAGE AGAIN EVEN THOUGH FILTER OPTION IN URL
    print(filtered_card_result_link)

    card_page = requests.get(filtered_card_result_link)
    card_page_handle = BeautifulSoup(card_page.content, "html.parser")

    #card_page_handle.find

    dd_data = [dl_el for dl_el in card_page_handle.find_all("dl", class_='labeled row no-gutters mx-auto')[0] if dl_el.name == 'dd']
    available_sales = dd_data[1]
    # 1 = verfügbare Karten
    # 5 = Preis ab
    # 6 = Preis - Trend
    # 7 = 30 - Tages - Durchschnitt
    # 8 = 7 - Tages - Durchschnitt
    # 9 = 1 - Tages - Durchschnitt

    #test =
    #print(test)

    card_articles = card_page_handle.findAll('div', id=lambda x: x and x.startswith('articleRow'))
    card_article_list = []
    for article in card_articles:
        product_attributes = article.find_all("div", class_="product-attributes col")[0]
        product_condition = product_attributes.find_all('a', href=True)[0].text
        product_language = product_attributes.find_all('span')[1].attrs['data-original-title']

        product_offer_div = article.find_all("div", class_="col-offer")[0]
        product_price = product_offer_div.find_all('span')[0].text.replace('.' , '').strip('€').strip(' ').replace(',', '.')
        product_amount = product_offer_div.find_all('span')[1].text
        card_article_list.append(CardArticle(product_condition, product_language, float(product_price), int(product_amount)))
