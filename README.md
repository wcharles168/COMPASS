# COMPASS
Charles's 2018 Internship at Northeastern COMPASS Lab

The Efficacy of Heart Rate Versus Blood Volume Pressure Using a Simple Method for Objective Pain Measurement: Comment on COMPASS

# Summary
Given access to the ihmslab data on the various physiological signals they collected during their COMPASS project funded by NSF grant #1333524, a rudimentary algorithm was designed to analyze and classify portion of the data in order to develop a framework to objectively predict pain levels. The algorithm performed on blood volume pulse and heart rate data with an accuracy of 50% and 64%, respectively. It is highly recommended that heart rate be preferred over blood volume pulse as a representative signal for pain in future studies involving physiological data.

# Purpose 
The goal of this experiment is to develop an algorithm that can learn and predict a subject’s pain level given training and test data.

# Data
For the physiological channel to analyze, heart rate (HR) was chosen for a couple of reasons. First, it was already pre-processed, so the algorithm could easily sort and extract the data points. Second, it was more representative of each subject’s pain levels compared to a channel such as blood volume pulse. Nevertheless, analysis of BVP data was still performed.
There were a total of 32 subjects with available HR and BVP data in csv file format. The files were divided into a rough 2:1 training to test data ratio. 22 subjects were categorized as training data and put under a folder “training_data_hr”, while 10 were marked as test data and put under a folder “test_data_hr”. 

# Methodology
The algorithm is written in Python, and comprises of two stages: 

“Learning” phase:
Using the csv file containing reported pain scores provided in the Google Drive, the algorithm first parses through the file (named “sub_pain_levels.csv”) and stores the pain levels corresponding to each subject. It then goes through each training file, and averages all data points under each time interval, which corresponds to a reported pain score for that subject. To eliminate inter-subject variation, the baseline (pain score of 0) average is subtracted from all averages. The algorithm then maps each average value to the reported pain score. The final objective of the learning phase is to provide an average value for each pain score (0-10), which can be achieved by once again averaging the averages for every pain score. For example, if subject 1 had an average value of 77.5 with a pain score of 1 and subject 2 had an average value of 78.0 with the same score, the algorithm would output an average of 77.75 for a score of 1. At the end of the learning phase, the algorithm writes the results to a separate csv file (“learned_data.csv”). 

“Prediction” phase: 
Using the test data, the algorithm goes through the same process of averaging data and subtracting the baseline average under each time interval for every subject. It then reads from the learned data that was given under the learning phase, and compares each average to the “learned” averages and their respective pain scores. The algorithm determines the closest pain score as its prediction for the subject under a specific time interval. Afterwards, it groups the pain scores into four groups: No pain (0), Low pain (1-3), Medium pain (4-6), High pain (7-10).

# Results
By dividing the sum of the absolute deltas between the predicted and reported pain scores by the sum of the reported pain scores, a percentage of how inaccurate the algorithm is can be calculated (0 being 100% accurate and 1 being 0% accurate). From that percentage, a percent accuracy can be calculated. For the 10 subjects, the algorithm is ~64% accurate with heart rate data, and ~50% accurate with BVP data. 

# Limitations
This experiment is in no ways perfect, and there are a couple limitations. First, the population size is small, so the results of analyzing the training data may not be completely representative. Second, averaging the data may not be the ideal model for classification. An unexplained phenomenon that occurred as a result of the learning phase, but perhaps could be related to the validity of the model was that the average value peaked at a pain score of 7, rather than at the expected score of 10. Third, the data must be processed first, meaning that EEG data, which is often widely used, could not be analyzed. 


Special thanks to the ihms lab for data access, which will not be included in this github for privacry reasons. This simple algorithm could be expanded in several ways. As a means to improve accuracy, having the algorithm classify between pain and no pain states could be beneficial. But more importantly, it would be helpful to investigate further in regards to the validity of this algorithm compared to more complex machine learning algorithms. Based on preliminary results, a LSTM machine learning algorithm predicts at a 60% accuracy with BVP data and a 63% accuracy with EEG data. It was interesting to see that the experimental yet simple algorithm came close to matching that statistic for BVP. As the saying goes, “simplicity is the ultimate sophistication”.
Whether or not there is room for improvement in this algorithm, an outcome of this experiment that must be emphasized is the comparison between the efficacy of HR and BVP data. It seems that the most representative results would involve HR over BVP, and it is strongly advised that the COMPASS project should consider HR signal as more effective. 
