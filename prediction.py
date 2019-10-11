import glob
import csv
from collections import defaultdict, OrderedDict
from analysis import readReportedData

def predict(read_data, learned_data):

    predicted_ratings = defaultdict(list)

    # Map subject averages to learned averages
    for id, averages in read_data.items():

        for average in averages:
             # Keeps track of closest distance between read data and learned data
             closest_difference = None
             predicted_rating = None
             collapsed_rating = 0

             # Compares average values to values in learned data
             for rating, mapavg in learned_data.items():
                 difference = abs(mapavg - average)
                 if closest_difference == None:
                     closest_difference = difference
                     predicted_rating = rating
                     continue
                 elif (difference < closest_difference):
                     closest_difference = difference
                     predicted_rating = rating

            # Classifies ratings further
             if predicted_rating == 0:
                 predicted_ratings[id].append(collapsed_rating)
             elif predicted_rating > 0 and predicted_rating <= 3:
                 collapsed_rating = 1
                 predicted_ratings[id].append(collapsed_rating)
             elif predicted_rating > 3 and predicted_rating <= 6:
                 collapsed_rating = 2
                 predicted_ratings[id].append(collapsed_rating)
             elif predicted_rating > 6 and predicted_rating <= 10:
                 collapsed_rating = 3
                 predicted_ratings[id].append(collapsed_rating)

             # Resets for next average value
             closest_difference = None
             predicted_rating = None
             collapsed_rating = 0

    return predicted_ratings

# Retrieves learned data
learned_data = {}

prediction = {}

with open("learned_data.csv") as file:
    reader = csv.DictReader(file)

    for row in reader:
        for key in row:
            learned_data[int(key)] = float(row[key])


ordered_learned_data = OrderedDict(sorted(learned_data.items()))

path = "./test_data_bvp/*.csv"

# Calculates average data from test files
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

     baseline_avg = 0.0

     for key, values in sorted_data.items(): # Key is time interval, values are list of data

         for value in values:
             total += float(value)

         average = total / len(values)

         if key == 0:
             baseline_avg = average

         avg_data[int_subid].append(abs(average - baseline_avg))

         total = 0.0 # Sets sum back to 0 for next calculation

     sub_prediction = predict(avg_data, ordered_learned_data)

     for sub, ratings in sub_prediction.items():
         prediction[sub] = ratings

     # Closes file
     f.close()

ordered_predictions = OrderedDict(sorted(prediction.items()))

reported_data = readReportedData()

delta = defaultdict(list)

delta_total = 0
report_total = 0

for p_id, p_ratings in ordered_predictions.items():
    for r_id, r_ratings in reported_data.items():
        if p_id == r_id:
            r_collapsed_rating_list = []

            for p_rating, r_rating in zip(p_ratings, r_ratings):

                r_collapsed_rating = 0
                # Classifies ratings further
                if r_rating > 0 and r_rating <= 3:
                 r_collapsed_rating = 1
                elif r_rating > 3 and r_rating <= 6:
                 r_collapsed_rating = 2
                elif r_rating > 6 and r_rating <= 10:
                 r_collapsed_rating = 3

                r_collapsed_rating_list.append(r_collapsed_rating)

                delta_total += abs(p_rating - r_collapsed_rating)
                report_total += r_collapsed_rating

                r_collapsed_rating = 0

            print(str(p_id) + " predicted ratings: " + str(p_ratings) + " reported ratings: " + str(r_collapsed_rating_list))

performance = delta_total / float(report_total)
percent_performance = 100 * (1.0 - performance)

print("alogrithm performed with " + str(percent_performance) + "% accuracy")
