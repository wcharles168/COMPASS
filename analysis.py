import glob
import csv
from collections import defaultdict, OrderedDict
import os

def readReportedData():

    # Stores subjective ratings
    pain_levels = defaultdict(list)

    with open("sub_pain_levels.csv") as f:
        reader = csv.reader(f)

        next(reader)

        for row in reader:
            # Baseline no pain
            pain_levels[int(row[0])].append(0)

            # Subject id as key, pain levels over time as values
            i = 1
            while i < len(row):
                # Checks if there is data
                if row[i] != 'N/A':
                    pain_levels[int(row[0])].append(int(round(float(row[i]))))
                i += 1
        f.close()

    sorted_pain_lev = OrderedDict(sorted(pain_levels.items()))
    return sorted_pain_lev

def calculateAverages(path):
    # Stores the average data values for each subjective rating (0-10)
    rating_to_values = defaultdict(list)

    # Loops through every csv file in training folder
    for file in glob.glob(path):

        # Retrieve subject id from csv file path
        s_subid = ""

        for char in file:
            if char.isdigit():
                s_subid += char
        int_subid = int(s_subid)

        with open(file) as f:
            # Stores all values for each time interval
            total_data = defaultdict(list)

            # Stores average value for each time interval
            avg_data = defaultdict(list)

            reader = csv.reader(f)

            for row in reader:
                for i in range(len(row)): # Loops through each column in a row
                    total_data[i * 20].append(float(row[i]))

            sorted_data = OrderedDict(sorted(total_data.items())) # Sorts by keys (0, 20, 40, etc)

            total = 0.0

            # Subtract all averages by baseline (eliminates variation at baseline)
            baseline_avg = 0.0

            for key, values in sorted_data.items(): # Key is time interval, values are list of data

                for value in values:
                    total += float(value)

                average = total / len(values)

                if key == 0:
                    baseline_avg = average

                avg_data[int_subid].append(abs(average - baseline_avg))

                total = 0.0 # Sets sum back to 0 for next calculation

            # Closes file
            f.close()

            reported_pain_lev = readReportedData()

            # Map averages to subjective pain ratings
            for rating, average in zip(reported_pain_lev[int_subid], avg_data[int_subid]):
                rating_to_values[rating].append(average)

    return rating_to_values

rating_to_values = calculateAverages("./training_data_bvp/*.csv")

# Stores average value for each subjective rating (based on rating_to_values)
rating_to_average = defaultdict()

# Averages values (average under each subject) to get one average value per subjective rating
for rating in rating_to_values.keys():
    average_list = list(rating_to_values[rating])

    average = sum(average_list) / float(len(average_list))
    rating_to_average[rating] = average

    # Write to file all learned data
    with open("learned_data.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(rating_to_average.keys())
        writer.writerow(rating_to_average.values())

        f.flush()
        f.close()

print("Analysis successful")
