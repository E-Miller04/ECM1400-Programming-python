# This is a template. 
# You should modify the functions below to match
# the signatures determined by the project specification

import numpy as np
import datetime
from datetime import timedelta
import utils


def daily_average(data, monitoring_station, pollutant):
    """
    Returns a list of daily averages (365 days) for given pollutant and station - does not include "No Data" values
    @param data: all of the data in dictionary form from csv file
    @param monitoring_station: which station the data to be used is coming from
    @param pollutant: which pollutant from the station is to be used
    @return dailyAverage: list of 365 values representing each day's average pollution level for the pollutant type selected
    """
    
    dailyAverage = []

    #{'no': {'date time': ['value'], '2021-01-01 01:00:00': ['1.43738']...}, 'PM10': {'date time': ['value'], '2021-01-01 01:00:00': ['25.838']... }, 'PM25': {'date time': ['value'], '2021-01-01 01:00:00': ['22.453']... }}
    stationData = data[monitoring_station]
    #selecting pollutant's data
    pollutantData = stationData[pollutant]
    
    #keep looping through all data entries
    #new day at 01:00:00
    total = 0
    howMany = 0
    for key in pollutantData:
        #just look at time values
        #each day starts at 01:00:00
        if key[11:] == "01:00:00":
            total = 0
            howMany = 0

        #value is a list with 1 element
        value = pollutantData[key]

        strValue = str(value[0])
        
        #skip "No data" values
        if strValue != "No data":
            total += float(strValue)
            howMany += 1

        #end of day so append to list
        #each day ends at 24:00:00
        if key[11:] == "24:00:00":
            #if all values are "No data" then store as no data - 0 could be misleading
            if howMany == 0:
                dailyAverage.append("No data for this day")
            else:
                #calc average
                average = total/howMany
                dailyAverage.append(average)             


    return dailyAverage
        


def daily_median(data, monitoring_station, pollutant):
    """
    Returns a list of daily medians (365 days) for given pollutant and station - does not include "No Data" values
    @param data: all of the data in dictionary form from csv file
    @param monitoring_station: which station the data to be used is coming from
    @param pollutant: which pollutant from the station is to be used
    @return dailyMedian: list of 365 values representing each day's median pollution level for the pollutant type selected
    """
        
    #{'no': {'date time': ['value'], '2021-01-01 01:00:00': ['1.43738']...}, 'PM10': {'date time': ['value'], '2021-01-01 01:00:00': ['25.838']... }, 'PM25': {'date time': ['value'], '2021-01-01 01:00:00': ['22.453']... }}
    stationData = data[monitoring_station]
    #selecting pollutant's data
    pollutantData = stationData[pollutant]

    dailyMedian = []
    #keep looping through all data entries
    #new day at 01:00:00
    howMany = 0
    dataEntriesForDay = []
    for key in pollutantData:
        #just look at time values
        #each day starts at 01:00:00
        if key[11:] == "01:00:00":
            dataEntriesForDay = []
            howMany = 0

        #value is a list with 1 element
        value = pollutantData[key]

        strValue = str(value[0])

        #skip "No data" values
        if strValue != "No data":
            dataEntriesForDay.append(float(strValue))
            howMany += 1

        #end of day so append to list
        #each day ends at 24:00:00
        if key[11:] == "24:00:00":

            #if all values are "No data" then store as no data - 0 could be misleading
            if howMany == 0:
                dailyMedian.append("No data for this day")
            else:
                #calc median
                #tuple for div and mod values
                div, mod = divmod(howMany, 2)
                if mod == 0:
                    dataEntriesForDaySorted = sorted(dataEntriesForDay)
                    median = (dataEntriesForDaySorted[div] + dataEntriesForDaySorted[div - 1] ) / 2
                else:
                    dataEntriesForDaySorted = sorted(dataEntriesForDay)
                    median = dataEntriesForDaySorted[div]


                dailyMedian.append(median) 

    return dailyMedian



def hourly_average(data, monitoring_station, pollutant):
    """
    Returns a list of hourly averages (24 hours) for given pollutant and station - does not include "No Data" values
    @param data: all of the data in dictionary form from csv file
    @param monitoring_station: which station the data to be used is coming from
    @param pollutant: which pollutant from the station is to be used
    @return hourlyAverage: list of 24 values representing each hour's average, over the 365 days, pollution level for the pollutant type selected
    """
    
    #{'no': {'date time': ['value'], '2021-01-01 01:00:00': ['1.43738']...}, 'PM10': {'date time': ['value'], '2021-01-01 01:00:00': ['25.838']... }, 'PM25': {'date time': ['value'], '2021-01-01 01:00:00': ['22.453']... }}
    stationData = data[monitoring_station]
    #selecting pollutant's data
    pollutantData = stationData[pollutant]
    
    hourlyAverage = []

    #each hour is identifiable through time column from file so can use it as key
    eachHoursData = {"T01": [],"T02": [],"T03": [],"T04": [],"T05": [],"T06": [],"T07": [],"T08": [],"T09": [],"T10": [],"T11": [],"T12": [],"T13": [],"T14": [],"T15": [],"T16": [],"T17": [],"T18": [],"T19": [],"T20": [],"T21": [],"T22": [],"T23": [],"T24": []}

    #get all the data for each hour into a single list
    for key in pollutantData:
        value = pollutantData[key]

        strValue = str(value[0])

        if strValue != "No data":
            #01 to 24
            hourKey = "T" + key[11:13]
            
            #append new value to list
            eachHoursData[hourKey] += [float(strValue)]

    #for each hour get the sum and append the average to the list
    for key in eachHoursData:
        values = eachHoursData[key] 
        howMany = len(values)
        total = 0

        for element in values:
            total += float(element)

        if howMany != 0:
            average = total/howMany
            hourlyAverage.append(average)
        else:
            hourlyAverage.append("No data for this hour")

    return hourlyAverage


def monthly_average(data, monitoring_station, pollutant):
    """
    Returns a list of monthly averages (12 months) for given pollutant and station - does not include "No Data" values
    @param data: all of the data in dictionary form from csv file
    @param monitoring_station: which station the data to be used is coming from
    @param pollutant: which pollutant from the station is to be used
    @return monthlyAverage: list of 12 values representing each months's average pollution level for the pollutant type selected
    """
    
    #{'no': {'date time': ['value'], '2021-01-01 01:00:00': ['1.43738']...}, 'PM10': {'date time': ['value'], '2021-01-01 01:00:00': ['25.838']... }, 'PM25': {'date time': ['value'], '2021-01-01 01:00:00': ['22.453']... }}
    stationData = data[monitoring_station]
    #selecting pollutant's data
    pollutantData = stationData[pollutant]
    
    monthlyAverage = []

    #each month is identifiable through date column from file so can use it as key
    eachMonthsData = {"M01": [],"M02": [],"M03": [],"M04": [],"M05": [],"M06": [],"M07": [],"M08": [],"M09": [],"M10": [],"M11": [],"M12": []}

    #get all the data for each month into a single list
    for key in pollutantData:
        value = pollutantData[key]

        strValue = str(value[0])

        if strValue != "No data":
            #01 to 12
            monthKey = "M" + key[5:7]
            
            #append new value to list
            eachMonthsData[monthKey] += [float(strValue)]


    #for each month get the sum and append the average to the list
    for key in eachMonthsData:
        values = eachMonthsData[key] 
        howMany = len(values)
        total = 0

        for element in values:
            total += float(element)

        if howMany != 0:
            average = total/howMany
            monthlyAverage.append(average)
        else:
            monthlyAverage.append("No data for this month")

    return monthlyAverage


def peak_hour_date(data, date, monitoring_station,pollutant):
    """
    Returns the hour and pollutant value of the highest pollution level for given date
    @param data: all of the data in dictionary form from csv file
    @param date: the date selected to be used to find peak hour
    @param monitoring_station: which station the data to be used is coming from
    @param pollutant: which pollutant from the station is to be used
    @return maxIndex: the hour(s) at which the peak hour occur at
    @return max: the value of the peak hour(s)
    """

    #{'no': {'date time': ['value'], '2021-01-01 01:00:00': ['1.43738']...}, 'PM10': {'date time': ['value'], '2021-01-01 01:00:00': ['25.838']... }, 'PM25': {'date time': ['value'], '2021-01-01 01:00:00': ['22.453']... }}
    stationData = data[monitoring_station]
    #selecting pollutant's data
    pollutantData = stationData[pollutant]

    
    #how many non "No data" entries there are
    howMany = 0
    #dataList = the values for each hour of the pollutant - doesn't include "No data" entries
    dataList = []
    #the date-time at which each value is from
    dataListIndex = []

    #datetime works in 00:00:00 to 23:00:00
    #set to 00:00:00 then increment 1 at the start of the loop so the first key is 01:00:00 and last is 24:00:00
    time = datetime.datetime.strptime(date + " 00:00:00", '%Y-%m-%d %H:%M:%S')


    for increment in range(1, 25):
        time += timedelta(hours=1)
        if increment == 24:
            #special case as timedelta can't do 24:00:00 (only 00:00:00 to 23:00:00)
            time = date + " 24:00:00"

        current = pollutantData[str(time)]
        strValue = str(current[0])
        if strValue != "No data":
            dataList.append(strValue)
            dataListIndex.append(str(time))
            howMany +=1
        

    #if at least 1 value for pollutant that isn't "No data" then find the max
    if howMany != 0:
        results = utils.maxvalue(dataList)
        max, index = results
        maxIndex = []

        for values in index:
            maxIndex.append(dataListIndex[values - 1])
    else:
        max = "None"           
        maxIndex = []
    

    return maxIndex, max

def count_missing_data(data,  monitoring_station,pollutant):
    """
    Returns the number of no data entries for a given pollutant and station
    @param data: all of the data in dictionary form from csv file
    @param monitoring_station: which station the data to be used is coming from
    @param pollutant: which pollutant from the station is to be used
    @return amount: how many "No data" values there are for the station's pollutant
    """

    #{'no': {'date time': ['value'], '2021-01-01 01:00:00': ['1.43738']...}, 'PM10': {'date time': ['value'], '2021-01-01 01:00:00': ['25.838']... }, 'PM25': {'date time': ['value'], '2021-01-01 01:00:00': ['22.453']... }}
    stationData = data[monitoring_station]
    #selecting pollutant's data
    pollutantData = stationData[pollutant]
    
    #countvalue accepts lists so convert the dictionary values into a list
    valueList = []
    for key in pollutantData:
        value = pollutantData[key]

        strValue = str(value[0])

        valueList.append(strValue)

    amount = utils.countvalue(valueList, "No data")

    return amount

def fill_missing_data(data, new_value,  monitoring_station,pollutant):
    """
    Returns a copy of the data with the 'no data' values replcaed by the new value for a given pollutant and station
    @param data: all of the data in dictionary form from csv file
    @param new_value: value to replace "No data" in dictionary
    @param monitoring_station: which station the data to be used is coming from
    @param pollutant: which pollutant from the station is to be used
    @return newValueDict: new dictionary storing the replaced "No data" with the new value
    """
    
    #{'no': {'date time': ['value'], '2021-01-01 01:00:00': ['1.43738']...}, 'PM10': {'date time': ['value'], '2021-01-01 01:00:00': ['25.838']... }, 'PM25': {'date time': ['value'], '2021-01-01 01:00:00': ['22.453']... }}
    stationData = data[monitoring_station]
    #selecting pollutant's data
    pollutantData = stationData[pollutant]

    #new dictionary to replace "No data" with new_value
    #interpreting "copy" as a new dictionary and not changing the values from the data files
    newValueDict = {}
    for key in pollutantData:
        value = pollutantData[key]

        strValue = str(value[0])

        if strValue == "No data":
            newValueDict[key] = [new_value]
        else:
            newValueDict[key] = [strValue]

    return newValueDict