import csv
from collections import defaultdict


PED_COUNT = 0
HR_COUNT = 1


def main():
    aggregate()


def aggregate():
    # Read & aggregate data.
    file_r = open('./datasets/counts/counts.csv', 'r')
    reader = csv.DictReader(file_r)
    count_dic = defaultdict(lambda: [0]*2) # count_dic = {id: [xxxx, yyyyy]}
    for record in reader:
        count_dic[record['Sensor_ID']][PED_COUNT] += int(record['Hourly_Counts'])
        count_dic[record['Sensor_ID']][HR_COUNT] += 1
    file_r.close()

    # Write to output file.
    file_w = open('./datasets/counts/counts_final.csv', 'w')
    writer = csv.DictWriter(file_w, fieldnames = ['id', 'avg_count'])
    writer.writeheader()
    for sensor_id in count_dic:
        if sensor_id == '': # There is the a missing sensor 41 id in the OG data.
            writer.writerow({'id': '41', 'avg_count': count_dic[sensor_id][PED_COUNT]/count_dic[sensor_id][HR_COUNT]})
        else:
            writer.writerow({'id': sensor_id, 'avg_count': count_dic[sensor_id][PED_COUNT]/count_dic[sensor_id][HR_COUNT]})
    file_w.close()


# Allow declaring functions in arbitrary order.
if __name__ == '__main__':
    main()
