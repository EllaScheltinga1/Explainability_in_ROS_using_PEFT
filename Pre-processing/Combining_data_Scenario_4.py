import os
import pandas as pd
import json

def read_csv_files(directory):
    csv_data = {}
    for filename in os.listdir(directory):
        if filename.endswith('.csv'):
            filepath = os.path.join(directory, filename)
            df = pd.read_csv(filepath, header=None)  # Read the CSV without treating the first row as column headers
            key = filename.replace('.csv', '')  # Remove the .csv extension
            csv_data[key] = df.values.tolist()  # Convert DataFrame to list of lists
            print(f"Read CSV: {filename}, Key: {key}, Rows: {len(df)}")  # Debug statement
    return csv_data

def read_txt_files(directory, suffix):
    txt_data = {}
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r') as file:
                key = '_'.join(filename.split('_')[:3])  # Extract the first three parts of the filename
                key = key.replace(suffix, '')  # Remove the specified suffix
                txt_data[key] = file.read().strip()
                print(f"Read TXT: {filename}, Key: {key}, Content length: {len(txt_data[key])}")  # Debug statement
    return txt_data

def combine_data(csv_directory, txt_directory, question, txt_suffix):
    csv_data = read_csv_files(csv_directory)
    txt_data = read_txt_files(txt_directory, txt_suffix)
    print(len(csv_data))
    combined_data = []
    
    for key in csv_data:
        if key in txt_data:
            result = {
                'context': csv_data[key],
                'question': question,
                'answers': txt_data[key]
            }
            combined_data.append(result)
            print(f"Combined Key: {key}, Context length: {len(csv_data[key])}, Answer length: {len(txt_data[key])}")  # Debug statement
        else:
            print(f"Key {key} not found in TXT data")  # Debug statement

    return combined_data

def save_combined_data(csv_directory, txt_directory, question, txt_suffix, output_file):
    combined_result = combine_data(csv_directory, txt_directory, question, txt_suffix)
    with open(output_file, 'w') as f:
        json.dump(combined_result, f, indent=4)
    print(f"Combined data has been saved to {output_file}")

# Define the directories, questions, and suffixes
csv_directory = 'Scenario_4/Processed_csv'

txt_directories = [
    'Scenario_4/Answers_Q1',
    'Scenario_4/Answers_Q2',
    'Scenario_4/Answers_Q3',
    'Scenario_4/Answers_Q4',
    'Scenario_4/Answers_Q5',
    'Scenario_4/Answers_Q6',
    'Scenario_4/Answers_Q7',
    'Scenario_4/Answers_Q8',
    'Scenario_4/Answers_Q9',
    'Scenario_4/Answers_Q10',
    'Scenario_4/Answers_Q11',
    'Scenario_4/Answers_Q12',
    'Scenario_4/Answers_Q13',
    'Scenario_4/Answers_Q14'
]

questions = [
    'How many waypoints were received?',
    'Which waypoints were received?',
    'What were the coordinates of all the waypoints?',
    'Were all the received waypoints successfully reached?',
    'What was the first waypoint the robot reached?',
    'Where was the last waypoint the robot reached?',
    'Were all paths feasible during the navigation task?',
    'Were there any waypoints the robot failed to reach?',
    'Were there any obstacles the robot encountered during the navigation task?',
    'What is the task the robot had to perform?',
    'Where was the encountered obstacle located?',
    'How did the robot respond to the detected obstacle?',
    'Why were one or more of the paths not feasible?',
    'How did the robot deal with unfeasible path(s)?'
]

suffixes = [
    '_Q1a.txt',
    '_Q2a.txt',
    '_Q3a.txt',
    '_Q4a.txt',
    '_Q5a.txt',
    '_Q6a.txt',
    '_Q7a.txt',
    '_Q8a.txt',
    '_Q9a.txt',
    '_Q10a.txt',
    '_Q11a.txt',
    '_Q12a.txt',
    '_Q13a.txt',
    '_Q14a.txt'
]

# Combine and save the data for each question
all_combined_data = []
for i in range(14):
    combined_data = combine_data(csv_directory, txt_directories[i], questions[i], suffixes[i])
    all_combined_data.extend(combined_data)

# Save all combined data to a single JSON file
output_file = 'combined_data_4.json'
with open(output_file, 'w') as f:
    json.dump(all_combined_data, f, indent=4)

# Print statement for debugging
print(f"All combined data has been saved to {output_file}")

# Print the number of instances in the combined data
print(f"Total number of instances in the combined data: {len(all_combined_data)}")
