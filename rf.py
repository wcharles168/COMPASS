from sklearn.ensemble import RandomForestClassifier

# Load pandas
import pandas as pd

# Load numpy
import numpy as np

# Set random seed
np.random.seed(0)

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


# Create dataframe with one feature variable
df = pd.DataFrame(iris.data, columns=iris.feature_names)
