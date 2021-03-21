from bs4 import BeautifulSoup
import urllib.request
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import requests
import praw
import lxml


class Scape:
    """
        A class to represent scrape data.

        ...

        Attributes
        ----------
        url : str
            webpage to scrape

        Methods
        -------
        xrate_data():
            Return scrape data of all the currency rate from x-rates.com
        currencyCode():
            Return scrape data of the currency and code from currencysystem.com/codes/
        tweets(sample):
            Return scrape tweets and date
        reddit():
            Return the reddit account information to allow search
        cashchanger():
            Return the currency code, highest sell price and href link from cashchanger.co/singapore#buyrates
    """

    def __init__(self, url):
        """
                Constructs all the necessary attributes for the scrape object.

                Parameters
                ----------
                    url : str
                        link to scrape the data from
        """
        self.url = url

    def xrate_data(self):
        """
                Return the scrape the data from x-rates

                Returns
                -------
                exchange_rate (dictionary) : Dictionary of the currency name and rate
        """
        exchange_rate = {}
        # Get the element of the webpage
        req = urllib.request.Request(self.url)
        response = urllib.request.urlopen(req)
        soup = BeautifulSoup(response, 'html.parser')
        # Search for the relevant class
        html_data = soup.find_all('table', {'class': 'tablesorter ratesTable'})
        table_data = html_data[0].find_all('tbody')
        currency_info = table_data[0].find_all('tr')
        # Loop through the data to get the currency name and rate
        for info in currency_info:
            name = info.find('td').text
            rate = info.find('td', class_='rtRates').text
            exchange_rate[name] = rate
        return exchange_rate

    def currencyCode(self):
        """
                Return the currency name and the corresponding code

                Returns
                -------
                code_dict (dictionary): Dictionary of it currency name and currency code
        """
        # currency name and currency code
        code_dict = {'Bruneian Dollar': 'BND', 'Euro': 'EUR', 'Hong Kong Dollar': 'HKD', 'Israeli Shekel': 'ILS',
                     'Kazakhstani Tenge': 'KZT', 'Mauritian Rupee': 'MUR', 'Qatari Riyal': 'QAR',
                     'Saudi Arabian Riyal': 'SAR', 'Sri Lankan Rupee': 'LKR', 'Trinidadian Dollar': 'TTD',
                     'Emirati Dirham': 'AED', 'Venezuelan Bolivar': 'VEF'}
        # Get the element of the webpage
        req = urllib.request.Request(self.url)
        response = urllib.request.urlopen(req)
        soup = BeautifulSoup(response, 'html.parser')
        html_data = soup.find_all('table', {'border': '1'})
        currency_code = html_data[0].find_all('tr')
        # Get the currency name and code
        for info in currency_code[1:]:
            name = info.find('td', width="194").text
            code = info.find('td', width="41").text
            code_dict[name] = code
        code_dict = {k.lower(): v for k, v in code_dict.items()}
        return code_dict

    def tweets(self, sample):
        """
                Return the tweets scraped out

                Parameters
                ----------
                sample : int
                    The number of tweets to be scrape out

                Returns
                -------
                tweet_dict (dictionary): Dictionary of tweets and posted date
        """
        tweet_dict = {}
        # Use of selenium to open chrome and load the page
        browser = webdriver.Chrome()
        browser.get(self.url)
        time.sleep(3)
        checker = []
        # Check if the tweet reach the size expected
        while len(tweet_dict) < sample:
            # Get the element of the webpage
            soup = BeautifulSoup(browser.page_source, 'html.parser')
            post = soup.find_all("div", attrs={
                'class': "css-1dbjc4n r-j7yic r-qklmqi r-1adg3ll r-1ny4l3l"})
            # Check if the tweet remain the same
            if checker == post:
                # Scroll down the page
                html = browser.find_element_by_css_selector('body')
                html.send_keys(Keys.PAGE_DOWN)
                time.sleep(3)
            else:
                checker = post
                for get_tweet in post:
                    tweets = get_tweet.find("div", attrs={
                        'class': "css-901oao r-18jsvk2 r-1qd0xha r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-bnwqim r-qvutc0"})
                    post_date = get_tweet.find('time')
                    # Retrieve the tweet and post date
                    if tweets is None:
                        break
                    else:
                        tweet_text = tweets.get_text()
                        if tweet_text not in tweet_dict:
                            tweet_dict[tweet_text] = post_date.get_text()
        browser.close()
        return tweet_dict

    def reddit(self):
        """
                Return reddit authentication to allow reddit search and scrape

                Returns
                -------
                reddit (class) : class to allow reddit search and scrape
        """
        reddit = praw.Reddit(client_id='xD6YrdOujyA8Aw',
                             client_secret='2EODniKIdpLjhfQfY3Iw3VFjGDl5ng',
                             password='praw.oop.1009',
                             user_agent='hi',
                             username='BottleWarm151'
                             )
        return reddit

    def cashchanger(self):
        """
                Return the currency code, highest sell price and reference link to scrape more data

                Returns
                -------
                content (Multi-Dimension Array): Array that store all the currency array, highestsellPrice array and
                reference link array
        """
        # Get the element of the webpage
        soup = BeautifulSoup((requests.get(self.url).text), 'lxml')
        transaction = soup.find('div', id="bestratecontent-sell")
        # Find the class that store the currency
        currency = [i.text for i in transaction.find_all('span', class_="currency float-left pl-1")]
        # Find the class that store the highest selling price
        highestsellPrice = [i.text.strip('\n') for i in transaction.find_all('div', class_="text-rate-big text-center")]
        # Find the reference link
        links = [requests.get(str(i['href'])).text for i in transaction.find_all('a', href=True)]
        # Store all in a multi-dimension array
        content = [currency, highestsellPrice, links]
        return content

# print(Scape.__doc__)
# help(Scape)
