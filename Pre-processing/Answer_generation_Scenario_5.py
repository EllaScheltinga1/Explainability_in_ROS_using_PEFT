import csv
import os
from openai import OpenAI

# Initialize the OpenAI client with the API key
client = OpenAI(api_key='') # Add your API key here

# Path to your CSV file
folder_path = 'Scenario_5/Processed_csv/'

def ask_question(document_string, question):
    """Generate a response from the OpenAI API for a given question."""
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "###Instruction### You are an explainability AI specialized in analyzing and interpreting ROS log messages for autonomous robots. Your task is to provide clear, concise, and factual explanations based on the logs generated during robot operations. Focus on delivering precise answers to the user's queries."},
            {"role": "user", "content": f"###Context### Based on the ROS log messages in the following document: \n{document_string}\. ###Question### {question}"}
        ]
    )
    return response.choices[0].message.content

def process_csv_file(file_path):
    """Process the CSV file and generate answers for each question."""
    # Reading the CSV file and converting it to a single string document
    document_content = []
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            # Concatenate each row into a single line and append to the document content list
            document_content.append(' '.join(row))

    # Join all lines to form the document string
    document_string = '\n'.join(document_content)

    # Dictionary of questions
    questions = {
        "q1": "How many waypoints were received?",
        "q2": "Which waypoints were received?",
        "q3": "What were the coordinates of all the waypoints the robot received?",
        "q4": "Were all received waypoints successfully reached?",
        "q5": "What was the first waypoint the robot reached?",
        "q6": "Where was the last waypoint the robot reached?",
        "q7": "Were all planned paths feasible during the navigation task?",
        "q8": "Were there any waypoints that the robot failed to reach?",
        "q9": "Were there any obstacles encountered during the navigation task?",
        "q10": "What is the task the robot had to perform?",

        # Only for Scenario 2 & 4
        # "q11": "Where is the encountered obstacle located?",  
        # "q12": "How did the robot respond to the detected obstacle?",  

        # Only for Scenario 3, 4, & 5
        "q13": "Why were one or more paths not feasible?",  
        "q14": "How did the robot deal with unfeasible path(s)?"     
    }

    # Generate responses for each question
    responses = {key: ask_question(document_string, question) for key, question in questions.items()}

    return responses

# Iterate through all .csv files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(".csv"):
        # Process the CSV file
        file_path = os.path.join(folder_path, filename)
        responses = process_csv_file(file_path)
        
        ######## Q1 ########
        # Create the output file name
        file_base_name = os.path.splitext(filename)[0]
        output_file_name_q1 = f"{file_base_name}_Q1a.txt"
        output_file_path_1 = os.path.join("Scenario_5/Answers_Q1", output_file_name_q1)
        
        # Write the response to the output text file
        with open(output_file_path_1, 'w', encoding='utf-8') as output_file:
            output_file.write(responses["q1"])
        
        print(f"The response has been saved to {output_file_path_1}")

        ######## Q2 ########
        # Create the output file name
        file_base_name = os.path.splitext(filename)[0]
        output_file_name_q2 = f"{file_base_name}_Q2a.txt"
        output_file_path_2 = os.path.join("Scenario_5/Answers_Q2", output_file_name_q2)
        
        # Write the response to the output text file
        with open(output_file_path_2, 'w', encoding='utf-8') as output_file:
            output_file.write(responses["q2"])
        
        print(f"The response has been saved to {output_file_path_2}")

        ######## Q3 ########
        # Create the output file name
        file_base_name = os.path.splitext(filename)[0]
        output_file_name_q3 = f"{file_base_name}_Q3a.txt"
        output_file_path_3 = os.path.join("Scenario_5/Answers_Q3", output_file_name_q3)
        
        # Write the response to the output text file
        with open(output_file_path_3, 'w', encoding='utf-8') as output_file:
            output_file.write(responses["q3"])
        
        print(f"The response has been saved to {output_file_path_3}")

        ######## Q4 ########
        # Create the output file name
        file_base_name = os.path.splitext(filename)[0]
        output_file_name_q4 = f"{file_base_name}_Q4a.txt"
        output_file_path_4 = os.path.join("Scenario_5/Answers_Q4", output_file_name_q4)
        
        # Write the response to the output text file
        with open(output_file_path_4, 'w', encoding='utf-8') as output_file:
            output_file.write(responses["q4"])
        
        print(f"The response has been saved to {output_file_path_4}")

        ######## Q5 ########
        # Create the output file name
        file_base_name = os.path.splitext(filename)[0]
        output_file_name_q5 = f"{file_base_name}_Q5a.txt"
        output_file_path_5 = os.path.join("Scenario_5/Answers_Q5", output_file_name_q5)
        
        # Write the response to the output text file
        with open(output_file_path_5, 'w', encoding='utf-8') as output_file:
            output_file.write(responses["q5"])
        
        print(f"The response has been saved to {output_file_path_5}")

        ######## Q6 ########
        # Create the output file name
        file_base_name = os.path.splitext(filename)[0]
        output_file_name_q6 = f"{file_base_name}_Q6a.txt"
        output_file_path_6 = os.path.join("Scenario_5/Answers_Q6", output_file_name_q6)
        
        # Write the response to the output text file
        with open(output_file_path_6, 'w', encoding='utf-8') as output_file:
            output_file.write(responses["q6"])
        
        print(f"The response has been saved to {output_file_path_6}")

        ######## Q7 ########
        # Create the output file name
        file_base_name = os.path.splitext(filename)[0]
        output_file_name_q7 = f"{file_base_name}_Q7a.txt"
        output_file_path_7 = os.path.join("Scenario_5/Answers_Q7", output_file_name_q7)
        
        # Write the response to the output text file
        with open(output_file_path_7, 'w', encoding='utf-8') as output_file:
            output_file.write(responses["q7"])
        
        print(f"The response has been saved to {output_file_path_7}")

        ######## Q8 ########
        # Create the output file name
        file_base_name = os.path.splitext(filename)[0]
        output_file_name_q8 = f"{file_base_name}_Q8a.txt"
        output_file_path_8 = os.path.join("Scenario_5/Answers_Q8", output_file_name_q8)
        
        # Write the response to the output text file
        with open(output_file_path_8, 'w', encoding='utf-8') as output_file:
            output_file.write(responses["q8"])
        
        print(f"The response has been saved to {output_file_path_7}")

        ######## Q9 ########
        # Create the output file name
        file_base_name = os.path.splitext(filename)[0]
        output_file_name_q9 = f"{file_base_name}_Q9a.txt"
        output_file_path_9 = os.path.join("Scenario_5/Answers_Q9", output_file_name_q9)
        
        # Write the response to the output text file
        with open(output_file_path_9, 'w', encoding='utf-8') as output_file:
            output_file.write(responses["q9"])
    
        print(f"The response has been saved to {output_file_path_9}")

        ######## Q10 ########
        # Create the output file name
        file_base_name = os.path.splitext(filename)[0]
        output_file_name_q10 = f"{file_base_name}_Q10a.txt"
        output_file_path_10 = os.path.join("Scenario_5/Answers_Q10", output_file_name_q10)
        
        # Write the response to the output text file
        with open(output_file_path_10, 'w', encoding='utf-8') as output_file:
            output_file.write(responses["q10"])
    
        print(f"The response has been saved to {output_file_path_10}")

        ######## Q13 ########
        # Create the output file name
        file_base_name = os.path.splitext(filename)[0]
        output_file_name_q13 = f"{file_base_name}_Q13a.txt"
        output_file_path_13 = os.path.join("Scenario_5/Answers_Q13", output_file_name_q13)
        
        # Write the response to the output text file
        with open(output_file_path_13, 'w', encoding='utf-8') as output_file:
            output_file.write(responses["q13"])
    
        print(f"The response has been saved to {output_file_path_13}")

        ######## Q14 ########
        # Create the output file name
        file_base_name = os.path.splitext(filename)[0]
        output_file_name_q14 = f"{file_base_name}_Q14a.txt"
        output_file_path_14 = os.path.join("Scenario_5/Answers_Q14", output_file_name_q14)
        
        # Write the response to the output text file
        with open(output_file_path_14, 'w', encoding='utf-8') as output_file:
            output_file.write(responses["q14"])
    
        print(f"The response has been saved to {output_file_path_14}")

print("All files have been processed.")