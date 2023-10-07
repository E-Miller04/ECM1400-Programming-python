import pytest
import numpy as np
from utils import sumvalues, maxvalue, minvalue, meannvalue, countvalue
from reporting import daily_average, daily_median, hourly_average, monthly_average, peak_hour_date, count_missing_data, fill_missing_data
from intelligence import detect_connected_components


#testing utils functions
def test_sum():   
    vallist = [2,3,4,5,10]     
    assert sumvalues(vallist) == 24

def test_mean():
    vallist = [2,3,4,5,10]     
    assert meannvalue(vallist) == 4.8

def test_max():
    vallist = [2,3,4,5,10] 
    max, index = maxvalue(vallist)    
    assert max == 10
    assert index == [5]

def test_min():
    vallist = [2,3,4,5,10]    
    min, index = minvalue(vallist) 
    assert min == 2
    assert index == [1]

def test_count():
    vallist = [2,3,4,5,10]     
    assert countvalue(vallist, 4) == 1


#testing reporting functions
def dictionaryData():
    dictionary = {}
    
    #10
    dictionary['2021-01-01 01:00:00'] = ['1']
    dictionary['2021-01-01 02:00:00'] = ['1']
    dictionary['2021-01-01 03:00:00'] = ['1']
    dictionary['2021-01-01 04:00:00'] = ['1']
    dictionary['2021-01-01 05:00:00'] = ['1']
    dictionary['2021-01-01 06:00:00'] = ['1']
    dictionary['2021-01-01 07:00:00'] = ['1']
    dictionary['2021-01-01 08:00:00'] = ['1']
    dictionary['2021-01-01 09:00:00'] = ['1']
    dictionary['2021-01-01 10:00:00'] = ['No data']
    dictionary['2021-01-01 11:00:00'] = ['No data']
    dictionary['2021-01-01 12:00:00'] = ['No data']
    dictionary['2021-01-01 13:00:00'] = ['No data']
    dictionary['2021-01-01 14:00:00'] = ['No data']
    dictionary['2021-01-01 15:00:00'] = ['No data']
    dictionary['2021-01-01 16:00:00'] = ['No data']
    dictionary['2021-01-01 17:00:00'] = ['No data']
    dictionary['2021-01-01 18:00:00'] = ['No data']
    dictionary['2021-01-01 19:00:00'] = ['No data']
    dictionary['2021-01-01 20:00:00'] = ['No data']
    dictionary['2021-01-01 21:00:00'] = ['No data']
    dictionary['2021-01-01 22:00:00'] = ['No data']
    dictionary['2021-01-01 23:00:00'] = ['No data']
    dictionary['2021-01-01 24:00:00'] = ['1']

    #36
    dictionary['2021-01-02 01:00:00'] = ['4']
    dictionary['2021-01-02 02:00:00'] = ['4']

    dictionary['2021-01-02 03:00:00'] = ['5']
    dictionary['2021-01-02 04:00:00'] = ['5']
    dictionary['2021-01-02 05:00:00'] = ['2']
    dictionary['2021-01-02 06:00:00'] = ['2']
    dictionary['2021-01-02 07:00:00'] = ['1']
    dictionary['2021-01-02 08:00:00'] = ['1']
    dictionary['2021-01-02 09:00:00'] = ['1']
    dictionary['2021-01-02 10:00:00'] = ['No data']
    dictionary['2021-01-02 11:00:00'] = ['No data']
    dictionary['2021-01-02 12:00:00'] = ['No data']
    dictionary['2021-01-02 13:00:00'] = ['No data']
    dictionary['2021-01-02 14:00:00'] = ['No data']
    dictionary['2021-01-02 15:00:00'] = ['No data']
    dictionary['2021-01-02 16:00:00'] = ['No data']
    dictionary['2021-01-02 17:00:00'] = ['No data']
    dictionary['2021-01-02 18:00:00'] = ['No data']
    dictionary['2021-01-02 19:00:00'] = ['No data']
    dictionary['2021-01-02 20:00:00'] = ['No data']
    dictionary['2021-01-02 21:00:00'] = ['No data']

    dictionary['2021-01-02 22:00:00'] = ['6']
    dictionary['2021-01-02 23:00:00'] = ['3']
    dictionary['2021-01-02 24:00:00'] = ['2']


    dictionary['2021-03-03 01:00:00'] = ['No data']
    dictionary['2021-03-03 24:00:00'] = ['No data']

    return dictionary

def test_daily_average():
    data = dictionaryData()
    pollutant = "no"
    station = "Marylebone Road"

    Station_dict = {}
    Station_dict[pollutant] = data

    Final_dict = {}
    Final_dict[station] = Station_dict

    returnedValues = daily_average(Final_dict, station, pollutant)

    assert returnedValues == [1, 3, "No data for this day"]

def test_daily_median():
    data = dictionaryData()
    pollutant = "no"
    station = "Marylebone Road"

    Station_dict = {}
    Station_dict[pollutant] = data

    Final_dict = {}
    Final_dict[station] = Station_dict

    returnedValues = daily_median(Final_dict, station, pollutant)

    assert returnedValues == [1, 2.5, "No data for this day"]

def test_hourly_average():
    data = dictionaryData()
    pollutant = "no"
    station = "Marylebone Road"

    Station_dict = {}
    Station_dict[pollutant] = data

    Final_dict = {}
    Final_dict[station] = Station_dict

    returnedValues = hourly_average(Final_dict, station, pollutant)

    assert returnedValues == [2.5, 2.5, 3, 3, 1.5, 1.5, 1, 1, 1,"No data for this hour", "No data for this hour", "No data for this hour", "No data for this hour", "No data for this hour", "No data for this hour", "No data for this hour", "No data for this hour", "No data for this hour", "No data for this hour", "No data for this hour", "No data for this hour", 6, 3, 1.5]   

def test_monthly_average():
    data = dictionaryData()
    pollutant = "no"
    station = "Marylebone Road"

    Station_dict = {}
    Station_dict[pollutant] = data

    Final_dict = {}
    Final_dict[station] = Station_dict

    returnedValues = monthly_average(Final_dict, station, pollutant)

    assert returnedValues == [23/11, "No data for this month", "No data for this month", "No data for this month", "No data for this month", "No data for this month", "No data for this month", "No data for this month", "No data for this month", "No data for this month", "No data for this month", "No data for this month"]

def test_peak_hour():
    data = dictionaryData()
    pollutant = "no"
    station = "Marylebone Road"

    Station_dict = {}
    Station_dict[pollutant] = data

    Final_dict = {}
    Final_dict[station] = Station_dict

    maxIndex, max = peak_hour_date(Final_dict, "2021-01-02", station, pollutant)

    assert max == 6
    assert str(maxIndex[0]) == "2021-01-02 22:00:00"

def test_count_missing():
    data = dictionaryData()
    pollutant = "no"
    station = "Marylebone Road"

    Station_dict = {}
    Station_dict[pollutant] = data

    Final_dict = {}
    Final_dict[station] = Station_dict

    returnedValues = count_missing_data(Final_dict, station, pollutant)

    assert returnedValues == 28

def smallDictionaryData():
    dictionary = {}

    dictionary['2021-01-02 01:00:00'] = ['4']
    dictionary['2021-01-02 02:00:00'] = ['4']

    dictionary['2021-01-02 03:00:00'] = ['5']
    dictionary['2021-01-02 04:00:00'] = ['5']
    dictionary['2021-01-02 05:00:00'] = ['2']
    dictionary['2021-01-02 06:00:00'] = ['2']
    dictionary['2021-01-02 07:00:00'] = ['1']
    dictionary['2021-01-02 08:00:00'] = ['1']
    dictionary['2021-01-02 09:00:00'] = ['1']
    dictionary['2021-01-02 10:00:00'] = ['No data']
    dictionary['2021-01-02 11:00:00'] = ['No data']
    dictionary['2021-01-02 12:00:00'] = ['No data']
    dictionary['2021-01-02 13:00:00'] = ['No data']

    return dictionary

def test_replace_values():
    data = smallDictionaryData()
    pollutant = "no"
    station = "Marylebone Road"

    Station_dict = {}
    Station_dict[pollutant] = data

    Final_dict = {}
    Final_dict[station] = Station_dict

    returnedValues = fill_missing_data(Final_dict, "20", station, pollutant)

    assert returnedValues == {"2021-01-02 01:00:00":["4"], "2021-01-02 02:00:00":["4"], "2021-01-02 03:00:00":["5"], "2021-01-02 04:00:00":["5"],"2021-01-02 05:00:00":["2"],"2021-01-02 06:00:00":["2"],"2021-01-02 07:00:00":["1"], "2021-01-02 08:00:00":["1"],"2021-01-02 09:00:00":["1"], "2021-01-02 10:00:00":["20"], "2021-01-02 11:00:00":["20"], "2021-01-02 12:00:00":["20"], "2021-01-02 13:00:00":["20"]}


#testing intelligence functions
def test_connected():
    IMG = np.array([[0,0,0,0], [0,1,0,0], [0,1,0,1]])

    # 0000
    # 0100
    # 0101

    #connected component in a 2D array with each connected component having a unique identifiable number (1 and 2 here)
    mark = np.array([[0,0,0,0], [0,1,0,0], [0,1,0,2]])

    returned = detect_connected_components(IMG)
    
    assert np.array_equal(returned, mark) == True

