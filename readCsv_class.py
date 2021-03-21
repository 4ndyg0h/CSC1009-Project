import csv
import pandas as pd
import datetime


class ReadCSV:
    """
        A class to read csv file.

        ...

        Attributes
        ----------
        choice : str
            the currency code to read from


        Methods
        -------
        currency_option():
            Return all the currency code
        get_current():
            Return the current currency rate of the choice read from csv file generated
        get_max():
            Return the maximum rate of the choice from csv file generated
        get_min():
            Return the minimum rate of the choice from csv file generated
        get_avg():
            Return the average rate of the choice from csv file generated
        buy():
            Return the best location to buy the currency with the rate.
        past_record():
            Return all the record of the currency
        read_tweets(month):
            Return the tweet based on the month and choice
        reddit_dict(month):
            Return the reddit post based on the month and choice
        analyse_reddit():
            Return the percentage of the currency raising
        pastDailyRecord(month):
            Return all the daily record of the rate based on the currency choice
        readX(month):
            Return the list of the date based on selected month
    """

    def __init__(self, choice):
        """
                Constructs the necessary attributes for ReadCSV object.

                Parameters
                ----------
                    choice : str
                        currency code selected
        """
        self.choice = choice

    def currency_option(self):
        """
                Return all the currecny code in the csv file

                Returns
                -------
                currency (array): Array of the currency code
        """
        currency = []
        with open('MonthlyRate.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                currency.append(row['CurrencyCode'])
        return currency

    def get_current(self):
        """
                Return the current rate of the currency choice

                Returns
                -------
                current (float) : Float of the current rate rounded up to 4 decimal places
        """
        with open('MonthlyRate.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if self.choice == row['CurrencyCode']:
                    current = row["Current Rate"]
        csvfile.close()
        # Round the value to 4 d.p.
        current = round(float(current), 4)
        return current

    def get_max(self):
        """
                Return the maximum rate of the currency choice

                Returns
                -------
                max (float): Float of the maximum rate rounded up to 4 decimal places
        """
        df = pd.read_csv("MonthlyRate.csv")
        df = df[df.CurrencyCode == self.choice]
        maximum = df.max(axis=1).values[0]
        # Round the value to 4 d.p.
        maximum = round(float(maximum), 4)
        return maximum

    def get_min(self):
        """
                Return the minimum rate of the currency choice

                Returns
                -------
                min (float): Float of the minimum rate rounded up to 4 decimal places
        """
        df = pd.read_csv("MonthlyRate.csv")
        df = df[df.CurrencyCode == self.choice]
        minimum = df.min(axis=1).values[0]
        # Round the value to 4 d.p.
        minimum = round(float(minimum), 4)
        return minimum

    def get_avg(self):
        """
                Return the average rate of the currency choice

                Returns
                -------
                mean (float): Float of the average rate rounded up to 4 decimal places
        """
        df = pd.read_csv("MonthlyRate.csv")
        df = df[df.CurrencyCode == self.choice]
        mean = df.mean(axis=1).values[0]
        # Round the value to 4 d.p.
        mean = round(float(mean), 4)
        return mean

    def buy(self):
        """
                Return the best location to buy the currency and the rate.

                Returns
                -------
                info (array): Array of the location and the rate
        """
        csv_file = open('exchangeRate.csv', 'r')
        reader = csv.reader(csv_file)
        pointer = None

        for row in reader:
            try:
                if row[0] == self.choice:
                    pointer = row
                    break
            except:
                pass
        best = float('-inf')
        counter = 0
        if pointer is not None:
            prices = [float(x) for x in pointer[3].split(',')]
            for i in range(len(prices)):
                if prices[i] > best:
                    best = prices[i]
                    counter = i
                else:
                    continue
            location = pointer[2].split(',')[counter]
            price = best
            info = [location, price]
            return info
        csv_file.close()
        return None

    def past_record(self):
        """
                Return all the record of the rate based on the currency choice

                Returns
                -------
                record (array): Array of all the record
        """
        data = pd.read_csv("MonthlyRate.csv")
        code = data["CurrencyCode"]
        position = 0
        for x in code:
            # Get the row of the currency choice
            if x == self.choice:
                value = data.iloc[position]
            else:
                position += 1
        # Get the record from column 2 onward and reversed the order
        record = list(value[2:])[::-1]
        return record

    def read_tweets(self, month):
        """
                Return tweets and post date based on the currency choice and month

                Parameters
                ----------
                month : str
                    to filter out the tweet based on the month

                Returns
                -------
                tweet_dict (dictionary) : Dictionary of the tweets and post date after filtering
        """
        tweet_dict = {}
        with open('tweets.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Check if the post date is same as the month
                if month in row['post_date'] and "2020" in row['post_date']:
                    # Check if the tweets is relevant to the selected currency
                    if self.choice in row['tweets']:
                        # Add the tweet with the date to the dictionary
                        tweet_dict[row['tweets']] = row['post_date']
        csvfile.close()
        return tweet_dict

    def reddit_dict(self, month):
        """
                Return top 3 reddit news posts and post date based on the currency choice and month

                Parameters
                ----------
                month : str
                    to filter out the tweet based on the month

                Returns
                -------
                reddit_dict (dictionary) : Dictionary of the reddit posts and post date after filtering
        """
        reddit_dict = {}
        with open('reddit.csv', "rt", encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter=",")
            for row in reader:
                if len(reddit_dict) < 3:
                    # Check if the post date is same as the month
                    if month in row['Date'] and "2020" in row['Date']:
                        # Check if the posts is relevant to the selected currency
                        if self.choice in row['Currency']:
                            # Add the post with the date to the dictionary
                            reddit_dict[row['Title']] = row['Date']
        return reddit_dict

    def analyse_reddit(self):
        """
                Analyse reddit posts and determine the chances of the currency rate rising

                Returns
                -------
                percentage (float): Float of the percentage of the currency rising in 2 decimal places
        """
        currency_codes = ['ARS', 'BHD', 'BWP', 'BRL', 'BND', 'BGN', 'CLP', 'CNY', 'COP', 'HRK', 'CZK', 'DKK', 'HKD',
                          'ISK', 'IDR', 'IRR', 'ILS', 'KZT', 'KRW', 'KWD', 'LYD', 'MYR', 'MUR', 'MXN', 'NPR', 'NZD',
                          'NOK', 'OMR', 'PKR', 'PHP', 'PLN', 'QAR', 'RON', 'RUB', 'SAR', 'ZAR', 'LKR', 'SEK', 'CHF',
                          'TWD', 'THB', 'TTD', 'TRY', 'AED', 'VEF', 'AUD', 'CAD', 'EUR', 'HUF', 'INR', 'JPY', 'GBP',
                          'USD']

        # Word to determine the post
        word = ['all time high', 'positive', 'high', 'back up', 'peak', 'bounding off', 'playing well', 'drop',
                'skyrocket']
        counter = 0
        total = 0
        today = datetime.date.today()
        first = today.replace(day=1)
        thisMonth = today.strftime("%b")
        lastMonth = (first - datetime.timedelta(days=1)).strftime("%b")
        # Reddit posts from this month and last month are accounted for analysis
        if self.choice in currency_codes:
            with open('forex.csv', "rt", encoding='utf-8') as f:
                reader = csv.DictReader(f, delimiter=",")
                for row in reader:
                    if self.choice in row['Currency']:
                        if thisMonth or lastMonth in row['Date']:
                            # Count the total number of post scraped
                            total += 1
                            for i in word:
                                # If the post contain the word, increase the counter
                                if i in row["Title"]:
                                    counter += 1
        # Calculate the percentage
        if counter != 0:
            percentage = (counter / total) * 100
            percentage = round(percentage, 2)
            return percentage
        else:
            return 0

    def pastDaily_record(self, month):
        """
                Return all the record of the rate based on the currency choice

                Parameters
                ----------
                month : str
                    to filter out the daily rate based on the month

                Returns
                -------
                record (array): Array of the historical rate for the selected month
        """
        data = pd.read_csv("DailyRate.csv")
        code = data["CurrencyCode"]
        position = 0
        for x in code:
            # Get the row of the currency choice
            if x == self.choice:
                value = data.iloc[position]
            else:
                position += 1

        # Get first and last index from class Index
        p = Index()
        index1, index2 = p.getIndex(data, month)

        # Get the data from index to index of that month and reversed the order
        record = list(value[index1:index2 + 1])[::-1]
        return record

    def readX(self, month):
        """
            Return the list of the date based on selected month

            Parameters
            ----------
            month : str
                to filter out the column name based on the month

            Returns
            -------
            name (array): Array of the date for the selected month
        """
        data = pd.read_csv("DailyRate.csv")

        # Get first and last index from class Index
        p = Index()
        index1, index2 = p.getIndex(data, month)

        name = []

        # Generate the value for the x-axis, date of the selected month
        for z in data.columns[index1:index2 + 1]:
            name.append(z)
        return name[::-1]


class Index:
    def getIndex(self, data, month):
        """
            Return the first index and last index of the column date based on selected month

            Parameters
            ----------
            data : array
                list of dataset in csv file

            month : str
                to filter out the column name based on the month

            Returns
            -------
            index1 (int): first index of the same date of the month
            index2 (int): last index of the same date of the month

        """

        # get total number of columns containing in csv file
        numColumn = len(data.columns)

        with open('DailyRate.csv', newline='') as csvfile:
            reader = csv.reader(csvfile)
            rate = list(reader)

            firstCol = True
            prev = 0

            # return the first and last index of the selected month
            for i in range(2, numColumn):
                # format date of column i.e. "Jan"
                d = datetime.datetime.strptime(rate[0][i], "%Y-%m-%d")
                datee = d.strftime("%b")

                # check if the date of the historical rates matches with the selected month
                if month == datee:
                    temp = i

                    # get the first index of the historical rates
                    if firstCol is True:
                        index1 = i
                        firstCol = False

                    # get the last index of the historical rates
                    if firstCol is False and temp != prev:
                        index2 = i

                    prev = temp
        csvfile.close()

        return index1, index2

# print(ReadCSV.__doc__)
# help(ReadCSV)
