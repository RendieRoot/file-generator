from random import randint
import datetime
import sched
import time
import sys
import os

now = datetime.datetime.now()
year = '{:02d}'.format(now.year)
month = '{:02d}'.format(now.month)
day = '{:02d}'.format(now.day)
hour = '{:02d}'.format(now.hour)
minute = '{:02d}'.format(now.minute)

def saveToCSV(csv_columns, dict_data):
    newFile = "history_{0}-{1}-{2}_{3}h{4}m{5}sZ_TEMP_FILE.csv".format(year, month, day, hour, minute, str(randint(10,59)))
    
    headers = ", ".join(csv_columns)

    with open("/opt/splunk/etc/apps/something/data/{0}".format(newFile), 'a') as csvfile:
        csvfile.write(headers)
        for data in dict_data:
            d = ", ".join(data)
            csvfile.write(d + '\n')

def main(count, lines):
    columns = [] # headers
    tempValue = [] # base conten
    content = []

    for c in range(0, count):
        for l in range(0,lines):
            dict_data = []

            for x, i in enumerate(columns):
                if x < len(tempValue):
                    dict_data.append(str(tempValue[x]))
                else:
                    dict_data.append(str(randint(1,1000)))
            content.append(dict_data)
        saveToCSV(columns, content)
        content = []

if __name__ == "__main__":
    params = sys.argv

    if len(params) < 5:
        print("python3 multiply.py {number of files} {lines inside a file} {interval} {times}")
    else:
        count = int(params[1])
        lines = int(params[2])
        interval = int(params[3])
        times = int(params[4])

        print("%s files will created %s times with interval %s seconds" % (count, times, interval))

        counting = 1
        while True:
            if counting >= times:
                print("Process completed")
                break

            print("Iteration %s started" % (counting))
            startTime = int(time.time())
            main(count, lines)
            diffTime = int(time.time() - startTime)
            print("Iteration %s took %s seconds" % (counting, diffTime))

            sleepInterval = interval - diffTime
            print("New iteration will start (%s) in %s seconds" % (counting+1, sleepInterval))

            if sleepInterval <= 0:
                continue

            time.sleep(sleepInterval)
            counting = counting + 1
