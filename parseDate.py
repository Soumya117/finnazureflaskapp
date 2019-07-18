import datetime

def splitDate(date_str):
    split_date = ""
    try:
        split_date = date_str.split(":")
        print("Start date: ", split_date[0])
        print("End date: ", split_date[1])
    except:
        split_date = "Error in format"
    return split_date

def validateDateFormat(date):
    #2019-07-16 check for this format easier to compare
    #{2018-01-12:2019-02-2019}
    valid = False
    if date == '0':
        valid = True
    else:
        #should be in correct format
        try:
           dateFormat = datetime.datetime.strptime(date, "%Y-%m-%d")
           valid = True
        except:
            print("Invalid date")
    return valid

def validate(date_str):
    result = "success"
    date_range = splitDate(date_str)
    if "Error" in date_range:
        return date_range

    start = date_range[0]
    end = date_range[1]
    if not validateDateFormat(start):
        return "Invalid start date"
    if not validateDateFormat(end):
        return "Invalid end date"
       
    #now if both formats are okay we can check if start date is less than end date
    #ignore if one of them is 0
    if not start == '0' and not end == '0':
        if not end > start:
            result = "End date must be greater than start date"
    
    return result

    
    
    
    
