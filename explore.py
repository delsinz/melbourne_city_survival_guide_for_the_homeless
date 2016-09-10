'''
Approach:
0. Score locations by count -> score_counts
1. Score locations by min distance to food -> score_dist
2. score_final = score_counts*0.6 + score_dist*0.4
3. Explore with final_score

Explore:
0. Best spot for specifed day of the week and meal.
1. Best/worst day of the week (highest/lowest avg score)
2. Best/worst spot.
'''


import csv
from collections import defaultdict
from math import sqrt
import matplotlib.pyplot as plt


BREAKFAST = 0
LUNCH = 1
DINNER = 2


def main():
    print(survive(5, DINNER))

    days_score = score_days()
    print(sorted(days_score.keys(), key = days_score.get))
    #plot_score_days()

    spots_score = score_spots()
    print(sorted(spots_score.keys(), key = spots_score.get))
    #plot_score_spots()



#==================== start functions for loading data ====================#

# Load in sensor data, return dict {id: (latitude, longitude)}
def load_sensors_data():
    file_s = open('./datasets/sensors/sensors_final.csv')
    reader_s = csv.DictReader(file_s)
    sensors_dic = defaultdict(list)

    for record in reader_s:
        sensors_dic[int(record['Sensor ID'])].append(float(record['Latitude']))
        sensors_dic[int(record['Sensor ID'])].append(float(record['Longitude']))
    file_s.close()
    for key in sensors_dic:
        sensors_dic[key] = tuple(sensors_dic[key])

    return sensors_dic


# Load in counts data, return dict {id: count}
def load_counts_data():
    file_c = open('./datasets/counts/counts_final.csv')
    reader_c = csv.DictReader(file_c)
    counts_dic = defaultdict(float)

    for record in reader_c:
        counts_dic[int(record['id'])] = float(record['avg_count'])
    file_c.close()

    return counts_dic


# Load in food data, return dict {id: ((latitude, longitude), (mon), (tue),...)}
def load_food_data():
    file_f = open('./datasets/food/food_final.csv')
    reader_f = csv.DictReader(file_f)
    food_dic = {}

    for record in reader_f:
        food_dic[int(record['id'])] = (
            (float(record['Latitude']), float(record['Longitude'])),
            eval(record['Monday']),
            eval(record['Tuesday']),
            eval(record['Wednesday']),
            eval(record['Thursday']),
            eval(record['Friday']),
            eval(record['Saturday']),
            eval(record['Sunday'])
        )
    file_f.close()

    return food_dic

#==================== end functions for loading data ====================#


#==================== start functions for scoring ====================#

# input: {id: count}, return: {id: score}
# return: {id: score}
# score = (val - min)/(max-min), max count has the highest score
def score_counts(counts):
    score = {}
    max_val = max(counts.values())
    min_val = min(counts.values())
    gap = max_val - min_val

    for sensor_id in counts:
        score[sensor_id] = (counts[sensor_id] - min_val)/gap

    return score


# input: {id: min_dist}
# return: {id: score}
# score = (max - val)/(max - min), min dist has the highest score
def score_dist(dist):
    score = {}
    max_val = max(dist.values())
    min_val = min(dist.values())
    gap = max_val - min_val

    for sensor_id in dist:
        score[sensor_id] = (max_val - dist[sensor_id])/gap

    return score


# counts = {id: score_counts}
# dist = {id: score_dist}
# return: {id: score_final}
def score_final(counts, dist):
    if set(counts.keys()) != set(dist.keys()):
        print('Error: Not same keys set!')
        return
    else:
        score = {}
        for key in counts:
            score[key] = counts[key]*0.6 + dist[key]*0.4
        return score


# day: 1, 2, 3, 4, 5, 6, 7
# meal: BREAKFAST, LUNCH, DINNER
# sensors: {id: (latitude, longitude)}
# food: {id: ((latitude, longitude), (mon), (tue),...)}
# return: {id: min_dist}
def min_dist(day, meal, sensors, food):
    dist = {}
    food_filtered = {}

    for food_id in food:
        if meal in food[food_id][day]:
            food_filtered[food_id] = food[food_id][0] # food_filtered: {id: (latitude, longitude)}

    if food_filtered:
        for sensor_id in sensors:
            dist[sensor_id] = min([calc_dist(sensors[sensor_id], food_filtered[food_id]) for food_id in food_filtered])
    else:
        # No food spots fit the requirement
        for sensor_id in sensors:
            dist[sensor_id] = 0

    return dist


# Input: (latitude, longitude) * 2, return distance between coordinates
def calc_dist(sensor, food):
    dist = sqrt((sensor[0] - food[0])**2 + (sensor[1] - food[1])**2)
    return dist


#==================== end functions for scoring ====================#


#==================== start functions for exploring ====================#

# Find the best spot for specified day of the week and meal.
# day: 1-7 for Mon-Sun
# meal: 0,1,2 for breakfast,lunch,dinner
def survive(day, meal):
    counts = score_counts(load_counts_data())
    dist = score_dist(min_dist(day, meal, load_sensors_data(), load_food_data()))
    final = score_final(counts, dist)
    best = sorted(final.keys(), key = final.get)[-1]
    return(best, final[best])


# Score of days of week
def score_days():
    counts = score_counts(load_counts_data())
    score = {}
    day_total = 0 # total score of all spots for all meals in one day

    for day in [1,2,3,4,5,6,7]:
        for meal in [0,1,2]:
            dist = score_dist(min_dist(day, meal, load_sensors_data(), load_food_data()))
            final = score_final(counts, dist)
            day_total += sum(final.values())
        score[day] = day_total
        day_total = 0

    return score

# Scores of locations (total score in week)
def score_spots():
    counts = score_counts(load_counts_data())
    score = defaultdict(float)

    for day in [1,2,3,4,5,6,7]:
        for meal in [0,1,2]:
            dist = score_dist(min_dist(day, meal, load_sensors_data(), load_food_data()))
            final = score_final(counts, dist)
            for sensor_id in final:
                score[sensor_id] += final[sensor_id]

    return score


#==================== end functions for exploring ====================#

#==================== start functions for visualization ====================#

def plot_score_days():
    days = [1,2,3,4,5,6,7]
    score = score_days()

    plt.plot(days, [score[day] for day in days], 'ro')
    plt.xlabel('Day of week')
    plt.ylabel('Total score for day')
    plt.axis([0, 8, 40, 60])
    plt.show()

def plot_score_spots():
    score = score_spots()
    ids = sorted(score.keys())

    plt.bar(ids, [score[id] for id in ids])
    plt.show()


#==================== end functions for visualization ====================#
# Allow declaring functions in arbitrary order.
if __name__ == '__main__':
    main()
