import csv
import math
from datetime import datetime

def get_raw_data():
    with open("./data/data.csv", "r") as f:
        reader = csv.reader(f)
        return [row for row in reader if float(row[0]) > 10]
    
# def compress_data(data):
#     compressed_data = []
#     for row in data:
#         a = datetime.strptime(rows[i+1][1], timefstr)
#         b = datetime.strptime(rows[i][1], timefstr)
#         diff = a - b
#         if diff.seconds < 2:`


def process_data(raw_data):
    # Parse the data, this is where we need to:
    # * Reverse order
    # * Filter within a second or so?
    data_map = {}
    for row in raw_data:
        # Keep the highest value for each second
        current_value = float(data_map.get(row[1], "0.0"))

        if float(row[0]) > current_value:
            data_map[row[1]] = row[0]

    rows = list(zip(data_map.values(), data_map.keys())) 
    rows.sort(key=lambda x: x[1], reverse=True)

    return rows

def paginate_data(data, page_number, page_length):
    page_number = int(page_number)
    page_length = int(page_length)

    number_of_pages = math.ceil(len(data) / page_length)

    try:
        lower_bound = (page_number - 1) * page_length
        upper_bound = page_number * page_length
        return data[lower_bound : upper_bound], number_of_pages
    except Exception as e:
        print("ERROR: ", e)
        return [], 0

def get_stats(processed_data, speed_limit):
    over_limit = len(list(filter(lambda x: float(x[0]) > speed_limit, processed_data)))
    over30 = len(list(filter(lambda x: float(x[0]) > 30, processed_data))) 
    over40 = len(list(filter(lambda x: float(x[0]) > 40, processed_data))) 
    over50 = len(list(filter(lambda x: float(x[0]) > 50, processed_data))) 
    percentage_over = ( over_limit / float(len(processed_data)) ) * 100
    percentage_over = round(percentage_over, 1)

    print("over: ", over30, over40, over50)
    stats = {
        "over30": over30,
        "over40": over40,
        "over50": over50,
        "percentage_over": percentage_over,
        "over_limit": over_limit,
        "speed_limit": speed_limit
    }

    return stats
