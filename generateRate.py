import csv
import scrape_class
import datetime
import pandas as pd
from datetime import date


def extractData(currentDate, filename, colName, firstData, monthData):
    """
    Description
    -----------
    The existence of extractData function is to retrieve the information about the currency rate from certain website
    i.e. www.x-rates.com and save those imported data into a newly created csv file. The function also helps to format 
    the data into desired rows and columns in csv file. This function can only run the program if the caller function 
    has called this function.

    Run the program to export data from online weblinks to csv file.

    Caller Function:
        generateMonthlyRate()
        generateDailyRate()

    Parameters
    ----------
        currentDate: date
            specific date to extract exchange rates 

        filename: str
            name of the csv file

        colName: str
            column name 

        firstData: boolean
            to check if the program extracts the first set of data

    """

    if (firstData == True):
        if (monthData == True):
            # url link for today's exchange rate
            link = "https://www.x-rates.com/table/?from=SGD&amount=1"
        else:
            # url link from the date to be extracted
            link = "https://www.x-rates.com/historical/?from=SGD&amount=1&date=" + str(currentDate)

        # Scrape data from xrate_data() function in class scape
        currentRate = scrape_class.Scape(link).xrate_data()

        # Import list of currency code from the given url link using currencyCode() function in class scape
        currencycode_url = "https://currencysystem.com/codes/"
        currency_code = scrape_class.Scape(currencycode_url).currencyCode()

        # Write into CSV files with csv.DictWriter
        with open(filename, 'w', newline='') as csvfile:

            # Add in the column name
            fieldnames = ['CurrencyName', 'CurrencyCode', colName]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            # Write the data into csv in a certain format
            for k, i in currentRate.items():
                if k.lower() in currency_code:
                    writer.writerow({'CurrencyName': k, 'CurrencyCode': currency_code[k.lower()], colName: i})
                else:
                    writer.writerow({'CurrencyName': k, 'CurrencyCode': ' ', colName: i})
    else:
        # Retrieve different url links based on required date
        link = "https://www.x-rates.com/historical/?from=SGD&amount=1&date=" + str(currentDate)

        currentRate = scrape_class.Scape(link).xrate_data()

        # Read the existed csv filename using pandas
        df = pd.read_csv(filename)
        x = []

        # Import the subsequent rate into csv file with for loop
        for i in currentRate.values():
            # append columns in csv
            x.append(i)
        # define column name for each set of currency rate and save it into current csv
        df[colName] = x
        df.to_csv(filename, index=False)


def generateMonthlyRate(numYear, numMonth):
    """
    Description 
    -----------
    generateMonthlyRate is a caller function to call another function to scrape historical rates from online source. 
    Generally, the function will invoke adding column names in csv file which was named as "MonthlyRate.csv"
    
    Callee Function:
    extractDate()

    Parameters:
        numYear: int
            date of the year
        numMonth: int
            date of the month

    """

    # boolean to get first set of data for currency name, code and the current rate
    firstData = True

    # boolean to show the current function computing monthly rate
    monthData = True

    # csv filename for the monthly rate
    filename = "MonthlyRate.csv"

    # retrieve both the latest rate and the monthly rate in a specific date using for loop
    for i in range(0, 13):
        if (firstData == True):
            extractDate = None
            columnDate = "Current Rate"
        else:
            extractDate = datetime.date(numYear, numMonth, 1)
            columnDate = extractDate.strftime("%b %Y")

        # call function
        extractData(extractDate, filename, columnDate, firstData, monthData)

        # get month in descending order
        if (firstData == False):
            numMonth -= 1

        # switch boolean to false when first set of data has been retrieved
        firstData = False


def generateDailyRate(fromYear, fromMonth, fromDay, toYear, toMonth, toDay):
    """
    Description 
    -----------
    generateDailyRate is a caller function to call another function to scrape day-to-day historical rates from 
    online source. Generally, the while loop ensures the set data from each date are exported to csv file,
    "DailyRate.csv", in descending order.
    
    Callee Function:
    extractDate()

    Parameters:
        fromYear: int
            from date of the year
        fromMonth: int
            from date of the month
        fromDay: int
            from day   
        toYear: int
            to date of the year
        toMonth: int
            to date of the month
        toDay: int
            to day

    """

    # extract data from certain period
    start_date = datetime.date(fromYear, fromMonth, fromDay)  # from date
    end_date = datetime.date(toYear, toMonth, toDay)  # to date
    delta = datetime.timedelta(days=1)

    # boolean to get first set of data
    firstData = True

    # boolean to show the current function not using monthlyRate
    monthData = False

    # csv filename for the daily rate
    filename = "DailyRate.csv"

    # To extract data from and to certain period
    while start_date >= end_date:
        columnDate = start_date
        # call function
        extractData(start_date, filename, columnDate, firstData, monthData)

        # switch to false when first set of data is retrieved
        if (firstData == True):
            firstData = False

        # reduce date by 1
        start_date -= delta

# Enter year & month to generate monthly rate
# generateMonthlyRate(2020, 12)

# Run generateDailyRate function to compute daily rate from 01/12/20 to 01/01/20
# generateDailyRate(2020, 12, 31, 2020, 1, 1)
