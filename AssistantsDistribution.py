import pandas as pd


def distribute_assistants(students, assistants, initial_counts):
    assistant_counts = initial_counts  # Initialize with initial counts
    assignment = {}

    for student in students:
        chosen_assistant = min(assistant_counts, key=assistant_counts.get)
        assignment[student] = chosen_assistant
        assistant_counts[chosen_assistant] += 1

    return assignment, assistant_counts

####################################### Prep Inputs#############################################################


# Read input data from CSV files using Pandas
students_df = pd.read_csv("Inputs\students.csv")
assistants_df = pd.read_csv("Inputs\\assistants.csv")

# Extract usernames and names for students and assistants
students = students_df.set_index("Username")[["Name"]].to_dict()["Name"]
assistants = assistants_df.set_index("Username")[["Name"]].to_dict()["Name"]

# Read the initial counts from the "counts.csv" file
initial_counts_df = pd.read_csv("Inputs\Assistants_counts.csv")
initial_counts = dict(
    zip(initial_counts_df["Username"], initial_counts_df["count"]))

####################################### Apply algo #############################################################

# Apply the algorithm with initial counts
assignment, assistant_counts = distribute_assistants(
    list(students.keys()), list(assistants.keys()), initial_counts)

####################################### Manage Outputs #############################################################


######################## Students With Assistants ########################

# Create a Pandas DataFrame for the output
students_df["Assigned Assistant"] = [assistants[assistant]
                                     for assistant in assignment.values()]

# Sort the DataFrame by the "Assigned Assistant" column
students_df.sort_values(by="Assigned Assistant", inplace=True)

# Write the sorted output to a CSV file with Pandas
students_df.to_csv("Outputs\students_with_assistants_sorted.csv", index=False)

######################## Assistants With Students ########################

# Create a new CSV file with assistants and their assigned students
assigned_students_by_assistant = {assistant: [] for assistant in assistants}
for student, assistant in assignment.items():
    assigned_students_by_assistant[assistant].append(student)

max_students = max(len(students)
                   for students in assigned_students_by_assistant.values())
for assistant in assigned_students_by_assistant:
    while len(assigned_students_by_assistant[assistant]) < max_students:
        assigned_students_by_assistant[assistant].append(None)

output_data = pd.DataFrame(assigned_students_by_assistant)

# Write the output to a CSV file with Pandas
output_data.index.name = "Student"
output_data.columns = [assistants[assistant] for assistant in assistants]

output_data.to_csv("Outputs\\assistants_with_students.csv", index=False)

######################## Update Counts ########################

# Update and save the counts to the "counts.csv" file
updated_counts = assistant_counts

# Create a DataFrame with updated counts
updated_counts_df = pd.DataFrame(
    updated_counts.items(), columns=["Username", "count"])

# Write the updated counts to the "counts.csv" file
updated_counts_df.to_csv("Inputs\Assistants_counts.csv", index=False)
