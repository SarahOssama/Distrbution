import pandas as pd


def distribute_staff(students, staff, initial_counts):
    staff_counts = initial_counts  # Initialize with initial counts
    assignment = {}

    for student in students:
        chosen_staff = min(staff_counts, key=staff_counts.get)
        assignment[student] = chosen_staff
        staff_counts[chosen_staff] += 1

    return assignment, staff_counts


def initialize_counts(dataframe):
    initial_counts = dict(zip(dataframe["Username"], dataframe["count"]))
    return initial_counts

####################################### Manage Inputs #############################################################


# Read input data from CSV files using Pandas
students_df = pd.read_csv("Inputs/students.csv")
assistants_df = pd.read_csv("Inputs/assistants.csv")
reviewers_df = pd.read_csv("Inputs/reviewers.csv")

# Extract usernames and names for students, assistants, and reviewers
students = students_df.set_index("Username")[["Name"]].to_dict()["Name"]
assistants = assistants_df.set_index("Username")[["Name"]].to_dict()["Name"]
reviewers = reviewers_df.set_index("Username")[["Name"]].to_dict()["Name"]

# Read the initial counts for assistants and reviewers
initial_assistants_counts_df = pd.read_csv("Inputs/Assistants_counts.csv")
initial_reviewers_counts_df = pd.read_csv("Inputs/Reviewers_counts.csv")

initial_assistants_counts = initialize_counts(initial_assistants_counts_df)
initial_reviewers_counts = initialize_counts(initial_reviewers_counts_df)

####################################### Distribute #############################################################

# Apply the algorithm for assigning assistants
assignment_assistants, assistant_counts = distribute_staff(
    list(students.keys()), list(assistants.keys()), initial_assistants_counts)

# Apply the algorithm for assigning reviewers
assignment_reviewers, reviewer_counts = distribute_staff(
    list(students.keys()), list(reviewers.keys()), initial_reviewers_counts)

####################################### Manage Outputs #############################################################

######################## Students With Assistants and Reviewers ########################

# Create a Pandas DataFrame for the output
students_df["Assigned Assistant"] = [assistants[assistant]
                                     for assistant in assignment_assistants.values()]
students_df["Assigned Reviewer"] = [reviewers[reviewer]
                                    for reviewer in assignment_reviewers.values()]

# Sort the DataFrame by the "Assigned Assistant" and "Assigned Reviewer" columns
students_df.sort_values(
    by=["Assigned Assistant", "Assigned Reviewer"], inplace=True)

# Write the sorted output to a CSV file with Pandas
students_df.to_csv(
    "Outputs/students_with_assistants_and_reviewers_sorted.csv", index=False)

######################## Assistants and Reviewers With Students ########################

# Create a new CSV file with assistants and their assigned students
assigned_students_by_assistant = {assistant: [] for assistant in assistants}
for student, assistant in assignment_assistants.items():
    assigned_students_by_assistant[assistant].append(student)

# Create a new CSV file with reviewers and their assigned students
assigned_students_by_reviewer = {reviewer: [] for reviewer in reviewers}
for student, reviewer in assignment_reviewers.items():
    assigned_students_by_reviewer[reviewer].append(student)

# Find the maximum number of students assigned to any staff
max_students = max(max(len(students) for students in assigned_students_by_assistant.values()),
                   max(len(students) for students in assigned_students_by_reviewer.values()))

# Ensure that all DataFrames have the same number of rows
for staff_data in (assigned_students_by_assistant, assigned_students_by_reviewer):
    for staff_member in staff_data:
        while len(staff_data[staff_member]) < max_students:
            staff_data[staff_member].append(None)

# Create DataFrames for assistants and reviewers
output_data_assistants = pd.DataFrame(assigned_students_by_assistant)
output_data_reviewers = pd.DataFrame(assigned_students_by_reviewer)

# Write the output to CSV files with Pandas
output_data_assistants.index.name = "Student"
output_data_assistants.columns = [
    assistants[assistant] for assistant in assistants]
output_data_assistants.to_csv(
    "Outputs/assistants_with_students.csv", index=False)

output_data_reviewers.index.name = "Student"
output_data_reviewers.columns = [reviewers[reviewer] for reviewer in reviewers]
output_data_reviewers.to_csv(
    "Outputs/reviewers_with_students.csv", index=False)

######################## Update Counts for Assistants and Reviewers ########################

# Update and save the counts to the "Assistants_counts.csv" file
updated_assistants_counts = assistant_counts

# Update and save the counts to the "Reviewers_counts.csv" file
updated_reviewers_counts = reviewer_counts

# Create DataFrames with updated counts for assistants and reviewers
updated_assistants_counts_df = pd.DataFrame(
    updated_assistants_counts.items(), columns=["Username", "count"])

updated_reviewers_counts_df = pd.DataFrame(
    updated_reviewers_counts.items(), columns=["Username", "count"])

# Write the updated counts to CSV files with Pandas
updated_assistants_counts_df.to_csv(
    "Inputs/Assistants_counts.csv", index=False)
updated_reviewers_counts_df.to_csv("Inputs/Reviewers_counts.csv", index=False)
