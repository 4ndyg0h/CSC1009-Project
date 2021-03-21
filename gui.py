import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import PySimpleGUI as sg
import matplotlib
import readCsv_class
import pandas as pd
import matplotlib.pyplot as plt
import generateRate, reddit, twitter, scrapeCC
import os
import time

# Theme/Design of the GUI
sg.ChangeLookAndFeel('Dark Teal 12')

month = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

# File name required for the GUI
filename = ['MonthlyRate.csv', 'DailyRate.csv', 'exchangeRate.csv', 'tweets.csv', 'forex.csv', 'reddit.csv']


# Generate the value for the x-axis
def x_value():
    name = []
    data = pd.read_csv("MonthlyRate.csv")
    for z in data.columns[2:]:
        name.append(z[:-5])
    return name[::-1]


# Draw of the graph
def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side="top", fill="both", expand=1)
    return figure_canvas_agg


# Delete the graph from the GUI
def delete_figure_agg(figure_agg):
    figure_agg.get_tk_widget().forget()
    plt.close('all')


def gui_interface():
    # try to get all the currency code out of the file
    try:
        currency = readCsv_class.ReadCSV(None).currency_option()
    except FileNotFoundError:
        # Set drop down list as None
        currency = ["None"]
    # Define the window's contents
    # Left Side of the GUI
    layout_left = [[sg.Text('Report', font='Any 15 underline')],
                   [sg.Button('Extract Data')],
                   [sg.Text("Select Currency: "),
                    sg.Combo(size=(10, 1), values=currency, key='currency_choice', readonly=True,
                             default_value=currency[0]),
                    sg.Button('Search')],
                   [sg.Text(size=(40, 1), key='current')],
                   [sg.Text(size=(40, 1), key='max')],
                   [sg.Text(size=(40, 1), key='min')],
                   [sg.Text(size=(40, 1), key='avg')],
                   [sg.Text(size=(50, 1), key='buy')],
                   [sg.Canvas(key="graph")]]
    # Right side of the GUI
    layout_right = [[sg.Text('News', font='Any 15 underline')],
                    [sg.Text("Select Month: "),
                     sg.Combo(size=(10, 1), values=month, key='month_choice', readonly=True, disabled=True),
                     sg.Button(button_text='Find', disabled=True, key='find')],
                    [sg.MLine(key='news', size=(40, 30), disabled=True)]]

    layout = [[sg.Column(layout_left, element_justification='c', vertical_alignment='t'), sg.VSeperator(),
               sg.Column(layout_right, element_justification='c', vertical_alignment='t')]]

    window = sg.Window('Currency Report', layout, resizable=True).finalize()
    figure_agg = None

    # Display and interact with the Window using an Event Loop
    while True:
        event, values = window.read()
        # See if user wants to quit or window was closed
        if event == sg.WINDOW_CLOSED:
            break
        # Extract data button clicked; Generate the necessary report
        if event == 'Extract Data':
            # Call for the python file to generate report
            sg.popup_non_blocking('Extracting monthly currency exchange rate data. Please wait. \nETA: 30s',
                                  button_type=5)
            start = time.time()
            generateRate.generateMonthlyRate(2020, 12)
            print(f'Time taken for monthly exchange rate data: {int(time.time() - start)} seconds')

            sg.popup_non_blocking('Extracting daily currency exchange rate data. Please wait. \nETA: 3 mins',
                                  button_type=5)
            start = time.time()
            generateRate.generateDailyRate(2020, 12, 1, 2020, 1, 1)
            print(f'Time taken for exchange rate data: {int(time.time() - start)} seconds')

            sg.popup_non_blocking('Extracting best currency exchange location data. Please wait. \nETA: 1 min',
                                  button_type=5)
            start = time.time()
            scrapeCC.scrape()
            print(f'Time taken for location data: {int(time.time() - start)} seconds')

            sg.popup_non_blocking('Extracting twitter data. Please wait. \nETA: 2 min', button_type=5)
            start = time.time()
            twitter.scrape_tweet()
            print(f'Time taken for twitter data: {int(time.time() - start)} seconds')

            sg.popup_non_blocking('Extracting reddit data. Please wait. \nETA: 2 min', button_type=5)
            start = time.time()
            reddit.scrape_reddit()
            print(f'Time taken for reddit data: {int(time.time() - start)} seconds')

            # Update the combo box dropdown list
            currency = readCsv_class.ReadCSV(None).currency_option()
            window['currency_choice'].update(values=currency, size=(10, 7), set_to_index=0)
            # Inform user that the data extraction is completed
            sg.popup("Data extracted")

        # Search button clicked; Search for the information of the currency
        if event == 'Search':
            # Clear the previous graph
            if figure_agg:
                delete_figure_agg(figure_agg)
            # Clear the new sector
            window.FindElement('news').Update('')
            window["month_choice"].update(disabled=False)
            window["find"].update(disabled=False)
            # Get the selected currency code
            option = values['currency_choice']
            if option == 'None':
                sg.popup("No Data. Please extract data")
            else:
                # Retrieve the information by calling ReadCSV class to read the csv
                current = readCsv_class.ReadCSV(option).get_current()
                maximum = readCsv_class.ReadCSV(option).get_max()
                minimum = readCsv_class.ReadCSV(option).get_min()
                avg = readCsv_class.ReadCSV(option).get_avg()
                location = readCsv_class.ReadCSV(option).buy()
                percent = readCsv_class.ReadCSV(option).analyse_reddit()
                if percent is None or percent == 0:
                    percent_msg = "NIL"
                else:
                    percent_msg = '(' + str(percent) + u'% \u2191' + ')'
                # Display out the value
                window['current'].update('Current rate: ' + str(current) + '\t' + percent_msg)
                window['max'].update('Maximum rate: ' + str(maximum))
                window['min'].update('Minimum rate: ' + str(minimum))
                window['avg'].update('Average rate: ' + str(avg))
                if location is None:
                    window['buy'].update(visible=False)
                else:
                    window['buy'].update('Best Location to buy: ' + str(location[0]) + ' (' + str(location[1]) + ')',
                                         visible=True)

                x = x_value()
                # Get the data for y-axis of the graph
                y = readCsv_class.ReadCSV(option).past_record()
                fig = matplotlib.figure.Figure(figsize=(7, 4), dpi=100)
                t = np.arange(0, 3, .01)
                fig.add_subplot(111).plot(x, y)
                matplotlib.use("TkAgg")
                # Generate out the graph
                figure_agg = draw_figure(window["graph"].TKCanvas, fig)

        # Find button clicked; generate out the relevant news about the currency for the month
        if event == 'find':
            option = values['currency_choice']
            month_selected = values['month_choice']
            window.FindElement('news').Update('')
            # Get twitter and reddit news
            tweets = readCsv_class.ReadCSV(option).read_tweets(month_selected)
            reddit_posts = readCsv_class.ReadCSV(option).reddit_dict(month_selected)
            # If there is no news for the month; display out "No News"
            if bool(tweets) is False and bool(reddit_posts) is False:
                window['news'].print("No News")
            else:
                for k, i in tweets.items():
                    window['news'].print(i + "\n" + k)
                    window['news'].print("\n")
                for k, i in reddit_posts.items():
                    window['news'].print(i + "\n" + k)
                    window['news'].print("\n")

            if figure_agg:
                delete_figure_agg(figure_agg)

            # Get the data for both x-axis and y-axis of the graph
            tempX = readCsv_class.ReadCSV(option).readX(month_selected)
            tempY = readCsv_class.ReadCSV(option).pastDaily_record(month_selected)
            fig = matplotlib.figure.Figure(figsize=(7, 4), dpi=100)
            t = np.arange(0, 3, .01)
            ax = fig.add_subplot(111)

            # plotting the line graph for daily rate
            ax.plot(tempX, tempY)
            ax.tick_params(axis='x', labelsize=5, rotation=45)
            matplotlib.use("TkAgg")
            # Generate out the graph
            figure_agg = draw_figure(window["graph"].TKCanvas, fig)
    window.close()


if __name__ == '__main__':
    # Check if file exist
    for i in filename:
        if os.path.exists(i) is False:
            sg.popup("Data not being extracted. Please extract data. \nIt will take about 10-15 minutes")
    gui_interface()
