import csv
import scrape_class


def scrape_tweet():
    """
        Create a csv file of all the tweets and post date

        Returns
        -------
        None
    """
    # Set the size of the tweets to be scraped
    sample = 100
    # Link to scrape from
    url = "https://twitter.com/xe"
    # Call scrape class to scrape tweets
    tweets = scrape_class.Scape(url).tweets(sample)

    # Input the tweets and post date to csv file
    with open('tweets.csv', 'w', newline='') as f:
        fieldnames = ['post_date', 'tweets']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for k, i in tweets.items():
            writer.writerow({'post_date': i, 'tweets': repr(k)})


scrape_tweet()
