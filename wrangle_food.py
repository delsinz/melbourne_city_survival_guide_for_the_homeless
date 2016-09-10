import csv



fields = ['Category', 'Sub Category', 'Name', 'Who', 'Suburb', 'Address 1', 'Address 2', 'Latitude', 'Longitude']
fields_d = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
fields_final = ['Name', 'Suburb', 'Address 1', 'Address 2', 'Latitude', 'Longitude']
BREAKFAST = 0
LUNCH = 1
DINNER = 2



def main():
    filter_category()
    filter_who()
    filter_time()
    clean_up()



# Step_0: pick 'cheap and free meals' category
def filter_category():
    file_r = open('./datasets/food/food.csv', 'r')
    file_w = open('./datasets/food/food_1.csv', 'w')
    reader = csv.DictReader(file_r)
    writer = csv.DictWriter(file_w, fieldnames = fields + fields_d)

    record_w = {}
    writer.writeheader()
    for record_r in reader:
        # Some records don't have geographical data
        if (record_r['Category'].lower() == 'free and cheap meals') and record_r['Longitude']:
            for name in fields + fields_d:
                record_w[name] = record_r[name]
            writer.writerow(record_w)
    file_r.close()
    file_w.close()



# Step_1: pick places for everyone or homeless
def filter_who():
    file_r = open('./datasets/food/food_1.csv', 'r')
    file_w = open('./datasets/food/food_2.csv', 'w')
    reader = csv.DictReader(file_r)
    writer = csv.DictWriter(file_w, fieldnames = fields + fields_d)

    record_w = {}
    writer.writeheader()
    for record_r in reader:
        if (any(keyword in record_r['Who'].lower() for keyword in ['everyone', 'homeless', 'over 18'])):
            for name in fields + fields_d:
                record_w[name] = record_r[name]
            writer.writerow(record_w)
    file_r.close()
    file_w.close()



# Step_2: clean up open time
def filter_time():
    file_r = open('./datasets/food/food_2.csv', 'r')
    file_w = open('./datasets/food/food_3.csv', 'w')
    reader = csv.DictReader(file_r)
    writer = csv.DictWriter(file_w, fieldnames = fields + fields_d)

    record_w = {}
    writer.writeheader()
    for record_r in reader:
        for name in fields:
            record_w[name] = record_r[name]
        for name in fields_d:
            record_w[name] = which_meal(record_r[name])
        writer.writerow(record_w)
    file_r.close()
    file_w.close()



# Step_3: final clean-up. Get rid of useless fields.
def clean_up():
    file_r = open('./datasets/food/food_3.csv', 'r')
    file_w = open('./datasets/food/food_final.csv', 'w')
    reader = csv.DictReader(file_r)
    writer = csv.DictWriter(file_w, fieldnames = ['id'] + fields_final + fields_d)

    index = 0
    record_w = {}
    writer.writeheader()
    for record_r in reader:
        record_w['id'] = index
        index += 1
        for name in fields_final:
            record_w[name] = record_r[name]
        for name in fields_d:
            record_w[name] = record_r[name]
        writer.writerow(record_w)
    file_r.close()
    file_w.close()

# Take string input as open time, detect which meals.
# 3 cases: closed, indication of meal, no indication
def which_meal(data):
    result = []
    if data[0].isalpha():
        if 'Closed' in data:
            return(tuple(result))
        if 'Breakfast' in data:
            result.append(BREAKFAST)
        if 'Lunch' in data:
            result.append(LUNCH)
        if 'Dinner' in data:
            result.append(DINNER)
        return(tuple(result))
    else:
        ##### 7-10 breakfast, 11-14 lunch, 18-21 dinner #####
        # Get time strings in list
        data_l = data.split(' - ')
        # Convert to 24 hr clock num
        for i in range(len(data_l)):
            if('am' in data_l[i]):
                data_l[i] = float(data_l[i].strip()[:-2])
            elif('pm' in data_l[i]):
                if(data_l[i].strip()[:2] == '12'): # 12pm is a pain in the ass
                    data_l[i] = 12.0
                else:
                    data_l[i] = float(data_l[i].strip()[:-2]) + 12
        # Dealing with single value eg. '12.00pm'
        if len(data_l) == 1:
            data_l.append(data_l[0] + 3)
        # Match open time against meal time
        if overlap(data_l, (7, 10)):
            result.append(BREAKFAST)
        if overlap(data_l, (11, 14)):
            result.append(LUNCH)
        if overlap(data_l, (18, 21)):
            result.append(DINNER)
        return(tuple(result))

# Check for overlapping time interval
def overlap(open_time, meal_time):
    if open_time[1] < meal_time[0]:
        return(False)
    if open_time[0] > meal_time[1]:
        return(False)
    return(True)



# Allow declaring functions in arbitrary order.
if __name__ == '__main__':
    main()
