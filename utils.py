# This is a template. 
# You should modify the functions below to match
# the signatures determined by the project specification


def sumvalues(values):
    """
    Recieves a list and returns the sum of all elements - raises an exception to non numerical elements
    @param values: list of values
    @return sum: the sum of the list values
    """    
    
    sum = 0
    try:
        for item in values:       
            sum += float(item)
        return sum
    except:
        print("Error - non numerical value")

    
def maxvalue(values):
    """
    Recieves a list and returns the element with the highest value and the index - raises an exception to non numerical elements
    @param values: list of values
    @return maxIndex: the index at which the highest value occurs
    @return max: the maxiumum value in the list
    """    
    
    max = 0
    index = 0
    #multiple entries may have the same value
    #use a list in case multiple have the highest
    maxIndex = []
    
    #1 = first element
    try:
        for item in values:   
            index += 1    
            if float(item) > max:
                max = float(item)
                #if new highest then clear the index for previous highest
                maxIndex = [index]

            elif float(item) == max:
                maxIndex.append(index)

        return max, maxIndex
    except:
        print("Error - non numerical value")


def minvalue(values):
    """
    Recieves a list and returns the element with the lowest value and the index - raises an exception to non numerical elements
    @param values: list of values
    @return minIndex: the index at which the lowest value occurs
    @return min: the minimum value in the list
    """    
    
    min = 10000 #for reporting section this number is bigger than any of the values so is valid for that module
    index = 0
    minIndex = []
    try:
        for item in values: 
            index += 1      
            
            if float(item) < min:
                min = float(item)
                #if new lowest then clear the index for previous lowest
                minIndex = [index]

            
            elif float(item) == min:
                minIndex.append(index)
        
        return min, minIndex
    except:
        print("Error - non numerical value")


def meannvalue(values):
    """
    Recieves a list and returns the arthimetic mean of all elements - raises an exception to non numerical elements
    @param values: list of values
    @return mean: the mean of the list values
    """    

    sum = 0
    count = 0
    try:
        for item in values:       
            sum += float(item)
            count += 1
        
        mean = sum / count
        return mean
    except:
        print("Error - non numerical value")


def countvalue(values,xw):
    """
    Recieves a list and a value and then returns the amount of times the value appears in the list - 0 if it doesn't appear
    @param values: list of values
    @param xw: the value to find the amount of in the list
    @return count: the amount of times the value xw occurs in the list
    """    

    count = 0
    for item in values:       
        if str(item) == str(xw):
            count += 1
    return count

