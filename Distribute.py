import csv


def read_csv(filename):
    with open(filename, newline='') as csvfile:
        data = list(csv.reader(csvfile))
    return data


def distribute_assistants(students, assistants):
    assistant_counts = {assistant: 0 for assistant in assistants}
    assignment = {}

    for student in students:
        chosen_assistant = min(assistant_counts, key=assistant_counts.get)
        assignment[student] = chosen_assistant
        assistant_counts[chosen_assistant] += 1

    return assignment, assistant_counts


# Example input data in CSV files: students.csv and assistants.csv
students_data = read_csv("students.csv")
assistants_data = read_csv("assistants.csv")

# Remove the header row from CSV files
students_data.pop(0)
assistants_data.pop(0)

# Extract the student and assistant usernames
students = [row[0] for row in students_data]
assistants = [row[0] for row in assistants_data]

# Apply the algorithm
assignment, assistant_counts = distribute_assistants(students, assistants)

# Create a new CSV file with assistants and their assigned students
assigned_students_by_assistant = {assistant: [] for assistant in assistants}
for student, assistant in assignment.items():
    assigned_students_by_assistant[assistant].append(student)

with open("assistants_with_students.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    # Write header row with assistant usernames
    header_row = ["Assistant"] + assistants
    writer.writerow(header_row)

    # Write students assigned to each assistant
    max_students = max(len(students)
                       for students in assigned_students_by_assistant.values())
    for i in range(max_students):
        row = [assigned_students_by_assistant[assistant][i] if i < len(
            assigned_students_by_assistant[assistant]) else "" for assistant in assistants]
        writer.writerow([f"Student{i+1}"] + row)

# Output results
print("Assignment Results:")
for student, assistant in assignment.items():
    print(f"{student} ----> {assistant}")

print("\nAssistant Counts:")
for assistant, count in assistant_counts.items():
    print(f"{assistant} has {count} assignments")


# # Print all dfs
# print("Students:")
# print(students_df)
# print("\nAssistants:")
# print(assistants_df)
# print("\nInitial Counts:")
# print(initial_counts_df)
# print("\nUpdated Counts:")
# print(updated_counts_df)
# print("\nOutput Data:")
# print(output_data)
# # print assignment
# print("\nAssignment Results:")
# print(assignment)
