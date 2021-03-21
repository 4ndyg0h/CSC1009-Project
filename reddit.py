import csv
import time
import scrape_class
import os


def scrape_reddit():
    """
    Scrapes reddit for currency related news and posts

    Returns
    -------
    reddit.csv: csv containing currency, reddit posts and post dates
    """

    news_subreddit = {'AUD': 'AusNews',
                      'CAD': 'canadanews',
                      'EUR': 'europeanunion',
                      'HUF': 'hungariannews',
                      'INR': 'indianews',
                      'JPY': 'japannews',
                      'GBP': 'uknews',
                      'USD': 'USNEWS'
                      }

    news_search_term = {'ARS': 'Argentina',
                        'BHD': 'Bahrain',
                        'BWP': 'Botswana',
                        'BRL': 'Brazil',
                        'BND': 'Brunei',
                        'BGN': 'Bulgaria',
                        'CLP': 'Chile',
                        'CNY': 'China',
                        'COP': 'Colombia',
                        'HRK': 'Croatia',
                        'CZK': 'Czech',
                        'DKK': 'Denmark',
                        'HKD': 'Hong Kong',
                        'ISK': 'Iceland',
                        'IDR': 'Indonesia',
                        'IRR': 'Iran',
                        'ILS': 'Israel',
                        'KZT': 'Kazakhstan',
                        'KRW': 'South Korea',
                        'KWD': 'Kuwait',
                        'LYD': 'Libya',
                        'MYR': 'Malaysia',
                        'MUR': 'Mauritius',
                        'MXN': 'Mexico',
                        'NPR': 'Nepal',
                        'NZD': 'New Zealand',
                        'NOK': 'Norway',
                        'OMR': 'Oman',
                        'PKR': 'Pakistan',
                        'PHP': 'Philippines',
                        'PLN': 'Poland',
                        'QAR': 'Qatar',
                        'RON': 'Romania',
                        'RUB': 'Russia',
                        'SAR': 'Saudi Arabia',
                        'ZAR': 'South Africa',
                        'LKR': 'Sri Lanka',
                        'SEK': 'Sweden',
                        'CHF': 'Switzerland',
                        'TWD': 'Taiwan',
                        'THB': 'Thailand',
                        'TTD': 'Trinidad',
                        'TRY': 'Turkey',
                        'AED': 'United Arab Emirates',
                        'VEF': 'Venezuela'
                        }

    # Dictionaries that pair the relevant search terms to the currency codes to facilitate scraping
    all_currency_codes = []
    all_currency_codes.extend(news_search_term.keys())
    all_currency_codes.extend(news_subreddit.keys())

    # Reddit authentication to allow for scraping
    reddit = scrape_class.Scape(None).reddit()

    if os.path.isfile('reddit.csv'):
        # Removes previously scraped data, if any
        os.remove('reddit.csv')

    # To ensure no duplicate headers are written into the csv file
    reddit_header_added = False

    # Iterates through all 53 currencies
    for currency in all_currency_codes:

        with open('reddit.csv', 'a', encoding='utf-8', newline='') as f:
            headers = ['Currency', 'Title', 'Date']
            writer = csv.DictWriter(f, fieldnames=headers)
            if not reddit_header_added:
                # Creates csv file and adds headers
                writer.writeheader()
                reddit_header_added = True

            if currency in news_subreddit:
                # Scrapes the respective news subreddits for each currency
                for k, v in news_subreddit.items():
                    if k == currency:
                        for post in reddit.subreddit(v).top('year', limit=25):
                            writer.writerow({'Currency': currency, 'Title': post.title,
                                             'Date': time.strftime("%b %d %Y", time.localtime(post.created))})


            elif currency in news_search_term:
                for k, v in news_search_term.items():
                    if k == currency:
                        for post in reddit.subreddit('worldnews').search(v, limit=25, sort='top', time_filter='year'):
                            # Scrapes the subreddit r/worldnews for relevant currency news
                            writer.writerow({'Currency': currency, 'Title': post.title,
                                             'Date': time.strftime("%b %d %Y", time.localtime(post.created))})

    forex_header_added = False
    if os.path.isfile('forex.csv'):
        os.remove('forex.csv')
    for currency in all_currency_codes:
        with open('forex.csv', 'a', encoding='utf-8', newline='') as f:
            headers = ['Currency', 'Title', 'Date']
            writer = csv.DictWriter(f, fieldnames=headers)
            if not forex_header_added:
                writer.writeheader()
                forex_header_added = True

            if currency in all_currency_codes:
                # Scrapes r/Forex subreddit for relevant currency posts
                for post in reddit.subreddit('Forex').search(currency, limit=1000, sort='top',
                                                             time_filter='month'):
                    writer.writerow({'Currency': currency, 'Title': post.title,
                                     'Date': time.strftime("%b %d %Y", time.localtime(post.created))})

# scrape_reddit()
