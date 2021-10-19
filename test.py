import time
from datetime import datetime


"""
GOAL HERE IS TO MAKE SURE ANY READINGS WITHIN 
2-3 SECONDS ONLY REPORT THE HIGHEST OF THE READINGS


(FOR EACH ITEM IN SORTED LIST
IF ELEMENT ADJACENT IS WITHIN 1 SECOND
OF READING, ONLY TAKE MAX)
"""

data = """
22.5,10/11/2021-18:12:53
22.7,10/11/2021-18:12:54
23.2,10/11/2021-18:12:54
23.4,10/11/2021-18:12:54
23.8,10/11/2021-18:12:54
24.0,10/11/2021-18:12:55
24.2,10/11/2021-18:12:55
24.3,10/11/2021-18:12:55
24.4,10/11/2021-18:12:55
24.8,10/11/2021-18:12:56
25.0,10/11/2021-18:12:56
25.3,10/11/2021-18:12:57
25.4,10/11/2021-18:12:57
25.8,10/11/2021-18:12:58
26.6,10/11/2021-18:13:52
27.0,10/11/2021-18:13:52
29.3,10/11/2021-18:13:53
30.5,10/11/2021-18:13:53
31.1,10/11/2021-18:13:53
31.5,10/11/2021-18:13:53
31.6,10/11/2021-18:13:53
31.9,10/11/2021-18:13:53
32.0,10/11/2021-18:13:53
32.2,10/11/2021-18:13:53
32.3,10/11/2021-18:13:54
"""

def get_timestamp(row_string):
    timestring = row_string.split(",")[1]
    # print(timestring)
    strp = "%m/%d/%Y-%H:%M:%S"
    t = datetime.strptime(timestring, strp)
    # print(t)
    return t
    # datestring = datetime.datetime.strptime(timestring,strp).timetuple()
    # t = time.mktime(datestring)
    # tdelta = datetime.strptime()

def main():

   newdata = []
   split_data = data.split("\n") 
   for i,row in enumerate(split_data):
    #    print(row)

       try:
           t1 = get_timestamp(row)
           t2 = get_timestamp(split_data[i+1])
           tdelta =  t1 - t2 
           print("{} = {} - {} ".format(tdelta, t1, t2))

        
       except Exception as e:
           print("ERROR: ", e)
           continue

if __name__ == "__main__":
    main()

