# This is a template. 
# You should modify the functions below to match
# the signatures determined by the project specification
import sys
import reporting
import intelligence
import monitoring
import utils
import datetime
import matplotlib

def main_menu():
    """Loaded upon initialisation and displays menu options for the user to choose from"""
    
    finish = False

    #keep looping until quit is selected
    while  finish == False:
        print("\nSelect Module")
        print("R - Pollution Reporting")
        print("I - Mobility Intelligence")
        print("M - Real-time Monitoring")
        print("A - About")
        print("Q - Quit")
        
        choice = input("\nChoose an option: ")

        #only valid inputs execute something new
        if choice == "R":
            print("Loading Pollution Report")
            reporting_menu()
        elif choice == "I":
            print("Loading Mobility Intelligence")
            intelligence_menu()
        elif choice == "M":
            print("Loading Real-time Monitoring")
            monitoring_menu()
        elif choice == "A":
            print("Loading About information")
            about()
        elif choice == "Q":
            print("Loading Quit")   
            finish = True    
            quit()

#reporting menu
    
def reporting_menu():
    """
    Loaded from main_menu - gives the user the option to select one of the 3 datasets before using the Reporting Module, user must select Quit to return
    """    
      
    #importing the data
    data = reporting_menu_data_handling("Harlington", "Marylebone Road", "N Kensington")

    finish = False

    #user selecting which station
    #keep looping until quit is selected
    while finish == False:
        print("\nSelect Dataset")
        print("0 - Marylebone Road")
        print("1 - N Kensington")
        print("2 - Harlington")
        print("Q - Quit")
        
        choice = input("\nChoose an option: ")
        
        #only valid inputs execute something new
        if choice == "0":
            print("Selecting Marylebone Road dataset")
            reporting_menu_data_options(data, "Marylebone Road")
        elif choice == "1":
            print("Selecting N Kensington dataset")
            reporting_menu_data_options(data, "N Kensington")
        elif choice == "2":
            print("Selecting Harlington dataset")
            reporting_menu_data_options(data, "Harlington")
        elif choice == "Q":
            finish = True

def reporting_menu_data_handling(first, second, third):
    """
    Loaded from reporting_menu - Imports the 3 datasets from the data subdirectory so that it can be used in the Reporting Module
    @param first: name of the first station to import data from
    @param second: name of the second station to import data from
    @param third: name of the third station to import data from
    @return allDataSets: a dictionary containing all 3 station's pollutant data
    """
    
    #directory to hold all of the data
    allDataSets = {}

    for station in [first, second, third]:
        #import a single station at a time
        singleDataSet = reporting_menu_data_import(station)

        #the key is the station name and the values are another dictionary with pollutant as key and values as another dictionary with dtae-time as key and values of data in file
        #e.g. {'Harlington': {'no': {'date time': ['value'], '2021-01-01 01:00:00': ['1.43738']...}, 'PM10': {'date time': ['PM10'], '2021-01-01 01:00:00': ['25.838']... }, 'PM25': {'date time': ['PM25'], '2021-01-01 01:00:00': ['22.453']... }}, 'Marylebine Road': {'no': {'date time': ['value'], ...}, 'PM10': {'date time': ['PM10'], ... }, 'PM25': {'date time': ['PM25'], ... }}, 'N Kensington': {'no': {'date time': ['value'], ...}, 'PM10': {'date time': ['PM10'], ... }, 'PM25': {'date time': ['PM25'], ... }}}
        allDataSets[station] = singleDataSet

    return allDataSets

    
def reporting_menu_data_import(fileName):
    """
    Loaded from reporting_menu_data_handling - Imports 1 dataset to a dictionary before returning
    @param fileName: which dataset to import
    @return dataSet: dictionary of the 3 pollutants and their recorded values for each date/hour
    """

    dataSet = {}

    noData = {}
    PM10Data = {}
    PM25Data = {}

    #navigate to data subdirectory and find file based on station name
    file = open("data/" + "Pollution-London " + str(fileName) + ".csv", "r")

    #skip headings
    next(file)
    for line in file:
        #remove new line from end of data 
        line = line.strip('\n')

        #split along the commas
        splitLine = line.split(",")
        
        #the key is made up of the date and time (it's unqiue) and the values are the pollution values
        noData[splitLine[0]+" "+splitLine[1]] = [splitLine[2]]
        PM10Data[splitLine[0]+" "+splitLine[1]] = [splitLine[3]]
        PM25Data[splitLine[0]+" "+splitLine[1]] = [splitLine[4]]

    #{'no': {'date time': ['value'], '2021-01-01 01:00:00': ['1.43738']...}, 'PM10': {'date time': ['PM10'], '2021-01-01 01:00:00': ['25.838']... }, 'PM25': {'date time': ['PM25'], '2021-01-01 01:00:00': ['22.453']... }}
    dataSet["no"] = noData
    dataSet["PM10"] = PM10Data
    dataSet["PM25"] = PM25Data
    

    file.close()

    return dataSet


def reporting_menu_data_options(dataSet, station):
    """
    Loaded from reporting_menu - Gives the user access to the functions available in the Reporting Module to perform on selected station and pollutant
    @param dataSet: all 3 datasets from the 3 csv files as a dictionary
    @param station: which dataset to use
    """
    
    #get which pollutant to use
    pollutant = reporting_menu_data_options_pollutant()

    #if Quit for either function or pollutant return to calling function (selecting dataset screen)

    if pollutant != "Q":
        #get which function to execute if user didn't select quit for pollutant
        chosenFunction = reporting_menu_data_options_function()

        if chosenFunction != "Q":
            #select appropriate function from inputs if user didn't select quit for function
            returned = None
            if chosenFunction == "1":
                returned = reporting.daily_average(dataSet, station, pollutant)
                print("\nDaily average for " + station + " for pollutant " + pollutant + " is:")
                print(returned)

            elif chosenFunction == "2":
                returned = reporting.daily_median(dataSet, station, pollutant)
                print("\nDaily median for " + station + " for pollutant " + pollutant + " is:")
                print(returned)

            elif chosenFunction == "3":
                returned = reporting.hourly_average(dataSet, station, pollutant)
                print("\nHourly average for " + station + " for pollutant " + pollutant + " is:")
                print(returned)

            elif chosenFunction == "4":
                returned = reporting.monthly_average(dataSet, station, pollutant)
                print("\nMonthly average for " + station + " for pollutant " + pollutant + " is:")
                print(returned)

            elif chosenFunction == "5":
                #get the required extra argument for date parameter
                valid = False
                print("\nAll dates have the year 2021")
                print("\nPlease enter the month and day in the format mm-dd")
                while valid == False:
                    date = input("\nPlease enter a date: ")
                    try:
                        datetime.datetime.strptime("2021-" + date, '%Y-%m-%d')
                        valid = True
                    except:
                        print("Must be in format yyyy-mm-dd")
                fullDate = "2021-" + date
                returned = reporting.peak_hour_date(dataSet, fullDate, station, pollutant)

                maxIndex, max = returned

                if max != "None":
                    print("Peak hour(s) for " + str(fullDate) + " are:")

                    for values in maxIndex:
                        print(values[11:])


                    print("with the value " + str(max))
                else:
                    print("no data entries on " + str(fullDate))              

                
            elif chosenFunction == "6":
                returned = reporting.count_missing_data(dataSet, station, pollutant)
                print("\nAmount of missing data for " + station + " for pollutant " + pollutant + " is:")
                print(returned)

            elif chosenFunction == "7":
                newValue = input("\nEnter new value to replace 'No data' values: ")
                returned = reporting.fill_missing_data(dataSet, newValue, station, pollutant)
                print(returned)


def reporting_menu_data_options_pollutant():
    """
    Loaded from reporting_menu_data_options - user selects which pollutant to use for function
    @return choice: pollutant selected to be used from dataset, or Quit
    """

    valid = False
    while valid == False:
        print("\nSelect Pollutant")
        print("  no - nitric oxide")
        print("PM10 - PM10 inhalable particulate matter")
        print("PM25 - PM2.5 inhalable particulate matter")
        print("   Q - Quit")
        
        choice = input("\nChoose an option: ")
        
        #only valid inputs allowed to progress
        if choice == "no":
            print("Selecting no")
            valid = True
        elif choice == "PM10":
            print("Selecting PM10")
            valid = True
        elif choice == "PM25":
            print("Selecting PM25")
            valid = True
        elif choice == "Q":
            valid = True

    return choice
    
def reporting_menu_data_options_function():
    """
    Loaded from reporting_menu_data_options - user selects which function to 
    @return choice: function selected to perform on dataset, or Quit
    """
    
    valid = False

    #user selecting which function to execute on data from station
    #keep looping until quit is selected
    while valid == False:
        print("\nSelect Function")
        print("1 - Daily Average")
        print("2 - Daily Median")
        print("3 - Hourly Average")
        print("4 - Monthly Average")
        print("5 - Peak Hour Data")
        print("6 - Count Missing Data")
        print("7 - Fill Missing Data")
        print("Q - Quit")
        
        choice = input("\nChoose an option: ")
        
        #only valid inputs allowed to progress
        if choice == "1":
            print("Selecting Daily Average")
            valid = True
        elif choice == "2":
            print("Selecting Daily Median")
            valid = True
        elif choice == "3":
            print("Selecting Hourly Average")
            valid = True
        elif choice == "4":
            print("Selecting Monthly Average")
            valid = True
        elif choice == "5":
            print("Selecting Peek Hour Data")
            valid = True
        elif choice == "6":
            print("Selecting Count Missing Data")
            valid = True
        elif choice == "7":
            print("Selecting Fill Missing Data")
            valid = True
        elif choice == "Q":
            valid = True

    return choice
    

#intelligence menu

def intelligence_menu():
    """
    Loaded from main_menu - user can choose which pavement type, to save selected path, and whether to display and save connected componets (sorted and unsorted) before returning
    """
    
    #returned_red_img = find_red_pixels("map.png")

    choice = intelligence_menu_type_choice()

    if choice != "Q":
        choice2 = intelligence_menu_save_pixel_Colour(choice)

        if choice2 != "Q":      

            if choice == "1": #red pixel map
                returned_img = intelligence.find_red_pixels("map.png")
            else: #cyan pixel map
                returned_img = intelligence.find_cyan_pixels("map.png")

            choice3 = intelligence_menu_display_connected_components()

            if choice3 != "Q":
                returned2Darray = intelligence.detect_connected_components(returned_img)

                choice4 = intelligence_menu_display_connected_components_sorted()

                if choice4 != "Q":
                    intelligence.detect_connected_components_sorted(returned2Darray)


            
def intelligence_menu_type_choice():
    """
    Loaded from intelligence_menu - user selects one of the two types of pavement
    @return choice: red, cyan or Quit
    """
    valid = False

    #user selecting which function to execute on data from station
    #keep looping until quit is selected
    while valid == False:
        print("\nSelect path type")
        print("1 - pavement on both sides (red)")
        print("2 - no info regarding pavement (cyan)")
        print("Q - Quit")
        
        choice = input("\nChoose an option: ")

        if choice == "1":
            valid = True

        elif choice == "2":
            valid = True

        elif choice == "Q":
            valid = True
    
    return choice

def intelligence_menu_save_pixel_Colour(type):
    """
    Loaded from intelligence_menu - user inputs whether they want to save a jpeg of the path type selected
    @param type: which colour is being saved
    @return choice: Yes or Quit
    """
    valid = False

    if type == "1":
        colour = "red"
    else:
        colour = "cyan"

    #user selecting which function to execute on data from station
    #keep looping until quit is selected
    while valid == False:
        print("\nSave selected path type")
        print("Y - save " + colour + " coloured path to jpeg")
        print("Q - Quit")
        
        choice = input("\nChoose an option: ")

        if choice == "Y":
            valid = True

        elif choice == "Q":
            valid = True
    
    return choice


def intelligence_menu_display_connected_components():
    """
    Loaded from intelligence_menu - user inputs whether they want to display the connected components and save to text file
    @return choice: Yes or Quit
    """
    valid = False

    #user selecting which function to execute on data from station
    #keep looping until quit is selected
    while valid == False:
        print("\nDisplay connected component list and save to txt file")
        print("Y - yes")
        print("Q - Quit")
        
        choice = input("\nChoose an option: ")

        if choice == "Y":
            valid = True

        elif choice == "Q":
            valid = True
    
    return choice


def intelligence_menu_display_connected_components_sorted():
    """
    Loaded from intelligence_menu - user inputs whether they want to display the connected components in descending order, save to text file and save largest 2 to jpeg
    @return choice: Yes or Quit
    """
    valid = False

    #user selecting which function to execute on data from station
    #keep looping until quit is selected
    while valid == False:
        print("\nDisplay SORTED connected component list and save to txt file as well as saving top 2 largest to jpeg")
        print("Y - yes")
        print("Q - Quit")
        
        choice = input("\nChoose an option: ")

        if choice == "Y":
            valid = True

        elif choice == "Q":
            valid = True
    
    return choice




#monitoring menu
def monitoring_menu():
    """
    Loaded from main_menu - runs the menus and options in monitoring before returning
    @errors: depends on what pollutant types are stored for what dates - some pollutants are not recorded any more
    @example working values for 1 pollutant = NO and any date
    @example working values for 3 pollutants = either NO, NO2, CO, SO2, O3 for 2020-12-12
    """
    
    monitoring.main_menu()



#about 
def about():
    """Loaded from main_menu - displays module code and candidate number before returning"""
    #candidate details
    print("ECM1400")
    print("233968")


#quit
def quit():
    """Loaded from main_menu - terminates program"""
    #terminate program
    sys.exit
    


if __name__ == '__main__':
    main_menu()