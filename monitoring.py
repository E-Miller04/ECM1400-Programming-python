# This is a template. 
# You should modify the functions below to match
# the signatures determined by the project specification.
# 
# This module will access data from the LondonAir Application Programming Interface (API)
# The API provides access to data to monitoring stations. 
# 
# You can access the API documentation here http://api.erg.ic.ac.uk/AirQuality/help
#

import requests
import datetime
import matplotlib.pyplot as mat_plot



#@errors: depends on what pollutant types are stored for what dates - some pollutants are not recorded any more
#@working values for 1 pollutant = NO and any date
#@working values for 3 pollutants = either NO, NO2, CO, SO2, O3 for 2020-12-12



def get_live_data_from_api(site_code='MY1',species_code='NO',start_date=None,end_date=None):
    """
    Return data from the LondonAir API using its AirQuality API. 
    
    *** This function is provided as an example of how to retrieve data from the API. ***
    It requires the `requests` library which needs to be installed. 
    In order to use this function you first have to install the `requests` library.
    This code is provided as-is. 
    """
    import requests
    import datetime
    start_date = datetime.date.today() if start_date is None else start_date
    end_date = start_date + datetime.timedelta(days=1) if end_date is None else end_date
    
    
    endpoint = "https://api.erg.ic.ac.uk/AirQuality/Data/SiteSpecies/SiteCode={site_code}/SpeciesCode={species_code}/StartDate={start_date}/EndDate={end_date}/Json"
   
    url = endpoint.format(
        site_code = site_code,
        species_code = species_code,
        start_date = start_date,
        end_date = end_date
    )
    
    res = requests.get(url)
    return res.json()

def request_function(site_code='MY1',species_code='NO',start_date=None,end_date=None):
    """
    handles the requests to the API
    @param site_code: place where data was recorded
    @param species_code: type of pollutant
    @param start_date: when to get data from
    @param end_date: when to stop getting data from
    @return res: request response
    """
    
    if start_date is None:
        start_date = datetime.date.today()
    

    if end_date is None:
        end_date = start_date + datetime.timedelta(days=1)
    
    
    endpoint = "https://api.erg.ic.ac.uk/AirQuality/Data/SiteSpecies/SiteCode={site_code}/SpeciesCode={species_code}/StartDate={start_date}/EndDate={end_date}/Json"
   
    url = endpoint.format(
        site_code = site_code,
        species_code = species_code,
        start_date = start_date,
        end_date = end_date
    )
    
    res = requests.get(url)
    
    return res.json()

def display_graph_1pollutant_1day(strdate, pollutant):
    """
    retrives and displays data, in text and graph form, for 1 pollutant for a 24 hours period
    @param strdate: the date selected by the user for data to be retrieved from
    @param pollutant: the pollutant selected by the user for data to be retrieved from
    """

    if strdate == None:
        date2 = None
    else:
        date1 = datetime.datetime.strptime(strdate, '%Y-%m-%d')
        date2 = date1.date()
    rawdata = request_function("MY1", pollutant, date2)

    details = rawdata['RawAQData']

    siteCode = details['@SiteCode']
    speciesCode = details['@SpeciesCode']

    data = details['Data']

    timeList = []
    valueList = []

    print("\nDate                 Value")

    for measurements in data:

        time = measurements['@MeasurementDateGMT']
        value = measurements['@Value']

        print(time + "  " + value)

        

        if value != "":
            valueList.append(float(value))
            timeList.append(time)


    dateTime = timeList[0]
    title = "Site Code = " + str(siteCode) + "   Species Code = " + str(speciesCode) + "    Date = " + str(dateTime[:10])

    sortedList = sorted(valueList)
    maxValue = sortedList[len(sortedList) - 1]


    hourList = []
    for time in timeList:
        hourList.append(time[11:13])

    maxHour = hourList[len(hourList) -1]


    mat_plot.plot(hourList, valueList, 'x:b')
    mat_plot.axis([0, maxHour, 0, maxValue + (maxValue/20)])    #xmin, xmax, ymin, ymax
    mat_plot.title(title)
    mat_plot.xlabel('Hour')
    mat_plot.ylabel('Pollution Value')
    mat_plot.show()


def display_graph_3pollutants_1day(strdate, pollutants):
    """
    retrives and displays data, in text and graph form, for 3 pollutants for a 24 hours period
    @param strdate: the date selected by the user for data to be retrieved from
    @param pollutants: the pollutants (list) selected by the user for data to be retrieved from
    """
    if strdate == None:
        date2 = None
    else:
        date1 = datetime.datetime.strptime(strdate, '%Y-%m-%d')
        date2 = date1.date()
    

    totalData = {}


    maxValue = 0
    for species in pollutants:
        print(species)
        
        rawdata = request_function("MY1", species, date2)

        details = rawdata['RawAQData']

        siteCode = details['@SiteCode']
        speciesCode = details['@SpeciesCode']

        data = details['Data']
        

        timeList = []
        valueList = []

        print("\nDate                 Value")

        for measurements in data:

            time = measurements['@MeasurementDateGMT']
            value = measurements['@Value']

            print(time, value)

            

            if value != "":
                valueList.append(float(value))
                timeList.append(time[11:13])

                if float(value) > maxValue:
                    maxValue = float(value)

        dictionary = {"value":valueList, "time":timeList}
        totalData[species] = dictionary

    #print(totalData)
    
    #print(valueList)
    speciesCode = ""
    for species in pollutants:
        speciesCode += " " + str(species)

    dateTime = str(date2)
    title = "Site Code = " + str(siteCode) + "   Species Code =" + str(speciesCode) + "    Date = " + str(dateTime[:10])

    valueList1 = []
    timeList1 = []
    valueList2 = []
    timeList2 = []
    valueList3 = []
    timeList3 = []

    first = totalData[pollutants[0]]
    valueList1 = first["value"]
    timeList1 = first["time"]

    second = totalData[pollutants[1]]
    valueList2 = second["value"]
    timeList2 = second["time"]

    third = totalData[pollutants[2]]
    valueList3 = third["value"]
    timeList3 = third["time"]


    maxHour = "23"


    mat_plot.plot(timeList1, valueList1, 'x:b', label= str(pollutants[0]))
    mat_plot.plot(timeList2, valueList2, 'o:g', label= str(pollutants[1]))
    mat_plot.plot(timeList3, valueList3, 's:r', label= str(pollutants[2]))

    mat_plot.axis([0, maxHour, 0, maxValue + (maxValue/20)])    #xmin, xmax, ymin, ymax
    mat_plot.title(title)
    mat_plot.xlabel('Hour')
    mat_plot.ylabel('Pollution Value')
    mat_plot.legend()
    mat_plot.show()
 


def pollutant_choice():
    """"
    keep looping until valid pollutant is selected
    @return choice: valid pollutant
    """
    valid = False

    while valid == False:
        print("\nChoose which pollutant")
        print("CO - carbon monoxide")
        print("NO2 - Nitrogen Dioxide")
        print("NO - Nitric Oxide")
        print("NOx - Oxides of Nitrogen")
        print("O3 - Ozone")
        print("PM10 Particulates")
        print("PM2.5 Particulates")
        print("SO2 - Sulphur Dioxide")
        
        
        choice = input("\nChoose an option: ")

        if choice == "CO":
            valid = True

        elif choice == "NO2":
            valid = True

        elif choice == "NO":
            valid = True

        elif choice == "NOx":
            valid = True

        elif choice == "O3":
            valid = True

        elif choice == "PM10 Particulates":
            valid = True

        elif choice == "PM2.5 Particulates":
            valid = True
        
        elif choice == "SO2":
            valid = True
    
    return choice


def date_choice():
    """
    user enters 't' for today's date or selects their own date
    @return date: date chosen by user
    """
    valid = False

    #user selecting which function to execute on data from station
    #keep looping until quit is selected
    while valid == False:
        print("\nEnter a date or 't' for today")
        
        choice = input("Enter a Date: ")

        if choice == "t":
            date = None
            valid = True

        else:
            try:
                Fulldate = datetime.datetime.strptime(choice, '%Y-%m-%d')
                date = str(Fulldate)[:10]
                valid = True
            except:
                print("Must be in format yyyy-mm-dd")
                
    return date


def three_pollutants_1day():
    """
    user selects 3 pollutants to be displayed - 3 separate pollutants - and a date for a the data and a graph to be displayed with all 3 pollutants for a site
    """
    print("\nChoose 3 pollutants and then a date")

    pollutants = []
    while len(pollutants) != 3:
        choice = pollutant_choice()

        if len(pollutants) == 0:
            pollutants.append(choice)
        else:
            notChosenBefore = False
            for species in pollutants:
                if str(species) == choice:
                    print("Pollutant already selected - please choose another pollutant")
                    notChosenBefore = True
            
            if notChosenBefore == False:
                print("valid")
                pollutants.append(choice)

        print("chosen pollutants = " + str(pollutants))

    date = date_choice()


    try:
        display_graph_3pollutants_1day(date, pollutants)
    except:
        print("Error creating graph")


def one_pollutant_1day():
    """
    1 pollutant and 1 date is selected 
    Data is retrieved and a graph is plotted - provided there is data from the API
    """
    print("\nChoose 1 pollutant and then a date")

    pollutant = pollutant_choice()
    date = date_choice()


    try:
        display_graph_1pollutant_1day(date, pollutant)
    except:
        print("Error creating graph")


def main_menu():
    """
    Gets users choice and acts based on input
    """
    choice = main_menu_choice()

    if choice == "1":
        one_pollutant_1day()
    if choice == "2":
        three_pollutants_1day()


def main_menu_choice():
    """
    user selects which functions to execute on data from sitecode MY1
    @return choice: the chosen function or quit
    """
    valid = False

    #user selecting which function to execute on data from station
    #keep looping until quit is selected
    while valid == False:
        print("\nSelect one of options below")
        print("1 - display a graph for 1 pollutant on 1 day")
        print("2 - display a graph for 3 pollutants on 1 day")
        print("Q - Quit")
        
        choice = input("\nChoose an option: ")

        if choice == "1":
            valid = True

        elif choice == "2":
            valid = True

        elif choice == "Q":
            valid = True
    
    return choice



