from bs4 import BeautifulSoup
import csv
import scrape_class


def scrape():
    """
    The following function allows the user to scrape data from "https://cashchanger.co/singapore" and writes into a comma seperated value files (.csv) for storage.

    Pre-requisites:
    BeautifulSoup, CSV and scrape_class library has to be installed within Python runtime environment

    --------------------

    No parameters required.

    --------------------

    Creates a .CSV file, return 0 to show run was successful 

    """

    url = "https://cashchanger.co/singapore"
    csv_file = open('exchangeRate.csv', 'w')
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(
        ['Currency', 'Highest Sell Price', 'Sell Location', 'Sell Price'])

    # Define a class that is inherited from the imported module scrape class, creating a multidimensional array
    scape_data = scrape_class.Scape(url).cashchanger()

    sellPrice = []
    sellLocation = []

    # initialize 3 variables into the multidimensional array
    currency = scape_data[0]
    highestsellPrice = scape_data[1]
    links = scape_data[2]

    # Iterate through every link and creates and saves the html file into a variable
    for link in links:
        soupSell = BeautifulSoup(link, 'lxml')
        list_locations = []
        list_price = []
        # Iterates through every line in the html file finding all classes
        # Extracts 2 data, location and price. Stores data onto individual list.
        for location in soupSell.find(class_="js-currencyresultlist").find_all(class_="currencyresult-item-container"):
            prices = location.find('span', class_="text-black text-weight-500").text.strip('\n')
            prices = prices.strip(' ')
            list_price.append(prices)
            list_locations.append((location.find('div', class_="text-grey shop-label")).text)

        sellPrice.append(','.join(list_price))
        sellLocation.append(','.join(list_locations))

    # Iterates through both list writes onto CSV file per row
    # Order of into = currency, highest selling price, location of said price and selling price

    for i in range(len(currency)):
        csv_writer.writerow(
            [currency[i], highestsellPrice[i], sellLocation[i], sellPrice[i]])
    csv_file.close()

    return 0
