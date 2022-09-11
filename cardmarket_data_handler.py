from bs4 import BeautifulSoup
import requests
import yaml
import cardmarket_resources
from data_classes import CardArticle
from data_classes import Card

class DataHandler:
    def __init__(self):
        pass

    def login(self, username, password):
        pass

    def setup(self, config_file):
        pass


class CardmarketDataHandler(DataHandler):
    def __init__(self):
        self.session = requests.session()
        self.base_url = 'https://www.cardmarket.com'
        self.mtg_singles_subpath = 'Magic/Products/Singles'
        self.site_lang_prefix = '/en/'
        self.seller_country = '7'

    def setup(self, config_file):
        config = yaml.safe_load(open("path/to/config.yml"))

    def login(self, username, password):
        login_page = 'https://www.cardmarket.com/en/Magic/PostGetAction/User_Login'
        account_page = 'https://www.cardmarket.com/en/Magic/Account'
        payload = {
            'referalPage': '/en/Magic',
            'username': username,
            'password': password
        }

        self.session.post(login_page, data=payload)
        response = self.session.get(account_page)
        print(response.text)

    def is_filtered_language_in_sold_cards(self, card_article_list, language):
        for article in card_article_list:
            if article.language == language:
                return True

        return False

    def get_card_article_information(self, card_link, card):
        card_page = self.session.get(card_link)
        card_page_handle = BeautifulSoup(card_page.content, "html.parser")

        dd_data = [dl_el for dl_el in card_page_handle.find_all("dl", class_='labeled row no-gutters mx-auto')[0] if
                   dl_el.name == 'dd']
        available_sales = dd_data[1]
        # 1 = verfügbare Karten
        # 5 = Preis ab
        # 6 = Preis - Trend
        # 7 = 30 - Tages - Durchschnitt
        # 8 = 7 - Tages - Durchschnitt
        # 9 = 1 - Tages - Durchschnitt

        card_articles = card_page_handle.findAll('div', id=lambda x: x and x.startswith('articleRow'))
        card_article_list = []
        for article in card_articles:
            product_attributes = article.find_all("div", class_="product-attributes col")[0]
            product_condition = product_attributes.find_all('a', href=True)[0].text
            product_language = product_attributes.find_all('span')[1].attrs['data-original-title']

            product_offer_div = article.find_all("div", class_="col-offer")[0]
            product_price = product_offer_div.find_all('span')[0].text.replace('.', '').strip('€').strip(
                ' ').replace(',', '.')
            product_amount = product_offer_div.find_all('span')[1].text
            card_article_list.append(
                CardArticle(product_condition, product_language, float(product_price), int(product_amount)))

        card.article_list = card_article_list

    def get_card_information(self, card):
        search_url = self.base_url + self.site_lang_prefix + self.mtg_singles_subpath + '?' + 'idExpansion=' + card.expansion_id + '&searchString=' + card.name + '&idRarity=' + card.rarity + 'perSite=30'

        page = self.session.get(search_url)
        search_page_handle = BeautifulSoup(page.content, "html.parser")

        search_results = search_page_handle.findAll('div', id=lambda x: x and x.startswith('productRow'))

        for card_result in search_results:
            card_result_link = self.base_url + [a['href'] for a in card_result.find_all('a', href=True) if a.text][0]
            filtered_card_result_link = card_result_link + '?' + 'sellerCountry=' + self.seller_country + '&' + 'language=' + card.language_id

            # HAVE TO CHECK LANGUAGE AGAIN EVEN THOUGH FILTER OPTION IN URL
            print(filtered_card_result_link)

            self.get_card_article_information(filtered_card_result_link)


if __name__ == '__main__':
    cardmarket_handler = CardmarketDataHandler()

    test_card = Card('Mana Crypt', '3', '0', '0', [])
    cardmarket_handler.get_card_information(test_card)
