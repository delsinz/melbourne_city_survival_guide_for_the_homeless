import csv


fields = ['Sensor ID', 'Sensor Description', 'Latitude', 'Longitude']


def main():
    clean_up()
    #file = open('./datasets/sensors/sensors_final.csv', 'r')
    #reader = csv.DictReader(file)
    #print(tuple(reader))


def clean_up():
    file_r = open('./datasets/sensors/sensors.csv', 'r')
    file_w = open('./datasets/sensors/sensors_final.csv', 'w')
    reader = csv.DictReader(file_r)
    writer = csv.DictWriter(file_w, fieldnames = fields)

    record_w = {}
    writer.writeheader()
    for record_r in reader:
        if(record_r['Status'] == 'Installed'):
            for name in fields:
                record_w[name] = record_r[name]
            writer.writerow(record_w)
    file_r.close()
    file_w.close()


# Allow declaring functions in arbitrary order.
if __name__ == '__main__':
    main()
