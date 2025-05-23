!pip install requests pandas matplotlib openpyxl
import requests
import pandas as pd
from requests.auth import HTTPBasicAuth
import json

# Credentials
JIRA_DOMAIN = "https://#.atlassian.net"
EMAIL = "#@gmail.com"
API_TOKEN = "#"
PROJECT_KEY = "#"

auth = HTTPBasicAuth(EMAIL, API_TOKEN)
headers = {
    "Accept": "application/json"
}

def get_boards():
    url = f"{JIRA_DOMAIN}/rest/agile/1.0/board"
    response = requests.get(url, headers=headers, auth=auth)
    return response.json()

def get_sprints(board_id):
    url = f"{JIRA_DOMAIN}/rest/agile/1.0/board/{board_id}/sprint"
    response = requests.get(url, headers=headers, auth=auth)
    return response.json()

def get_issues(sprint_id):
    url = f"{JIRA_DOMAIN}/rest/agile/1.0/sprint/{sprint_id}/issue"
    response = requests.get(url, headers=headers, auth=auth)
    return response.json()

# Step 1: Get board ID
boards = get_boards()
print("Boards Found:")
for board in boards['values']:
    print(f"Name: {board['name']} - ID: {board['id']}")

# Replace this manually once you know the ID
board_id = int(input("Enter your board ID: "))

# Step 2: Get sprints
sprints = get_sprints(board_id)
print("Sprints Found:")
for sprint in sprints['values']:
    print(f"Sprint Name: {sprint['name']} - ID: {sprint['id']} - State: {sprint['state']}")

# Step 3: Choose latest completed sprint
sprint_id = int(input("Enter a completed sprint ID to analyze: "))

# Step 4: Get issues from that sprint
issues_data = get_issues(sprint_id)

# Step 5: Analyze
issues = issues_data['issues']
backlog = []
done = []

for issue in issues:
    key = issue['key']
    summary = issue['fields']['summary']
    status = issue['fields']['status']['name']
    story_points = issue['fields'].get('customfield_10016', 0)  # Replace with your actual Story Points field ID
    if status.lower() == 'done':
        done.append((key, summary, story_points))
    else:
        backlog.append((key, summary, story_points))

# Convert to DataFrame
df_done = pd.DataFrame(done, columns=["Key", "Summary", "StoryPoints"])
df_backlog = pd.DataFrame(backlog, columns=["Key", "Summary", "StoryPoints"])

# Print summary
print("\n--- Sprint Summary ---")
print(f"Velocity (Story Points Done): {df_done['StoryPoints'].sum()}")
print(f"Backlog (Unfinished Story Points): {df_backlog['StoryPoints'].sum()}")

# Optional: Export to Excel
with pd.ExcelWriter("agile_report.xlsx") as writer:
    df_done.to_excel(writer, sheet_name="Done", index=False)
    df_backlog.to_excel(writer, sheet_name="Backlog", index=False)

#optional - Below code is for visualization
!pip install matplotlib
plt.figure(figsize=(6, 6))
plt.pie([total_done, total_backlog], labels=['Done', 'Backlog'], autopct='%1.1f%%', colors=['#4CAF50', '#F44336'])
plt.title('Sprint Completion Ratio')
plt.show()

# Visualization 2: Bar chart of done issues
plt.figure(figsize=(10, 5))
plt.bar(df_done['Key'], df_done['StoryPoints'], color='#2196F3')
plt.xlabel('Issue Key')
plt.ylabel('Story Points')
plt.title('Story Points Completed per Issue')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
