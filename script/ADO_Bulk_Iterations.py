import requests
import pandas as pd
from datetime import datetime
import base64

# Azure DevOps details
organization = "abodowood"  # For example abodowood
pat_token = "Ck3lFLa4g442hQdzIsJyxIDksz5nudiMamAPEw75qjzXJliZLcEiJQQJ99BAACAAAAAFR26XAAASAZDOcZKE"  # Replace this with your actual PAT
encoded_pat = base64.b64encode(bytes(f":{pat_token}", 'utf-8')).decode('utf-8')

# Project name
project_name = "Abodo"  # Replace with your actual project name such as Abodo

# CSV file path
spreadsheet_path = r"C:\temp\scripts\Automated-Iteration-Dates.csv"  # Replace with the location of your CSV

# Headers for API requests
headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Basic {encoded_pat}'
}

# Create iterations from CSV
def create_iteration(name, start_date, end_date):
    url = f"https://dev.azure.com/{organization}/{project_name}/_apis/wit/classificationnodes/Iterations?api-version=6.0"
    payload = {
        "name": name,
        "attributes": {
            "startDate": start_date,
            "finishDate": end_date
        }
    }
    response = requests.post(url, json=payload, headers=headers, verify=False)
    if response.status_code in [200, 201]:
        print(f"Successfully created iteration: {name}")
    else:
        print(f"Failed to create iteration: {name}. Error: {response.text}")

# Process CSV to create iterations
def process_csv():
    iterations_df = pd.read_csv(spreadsheet_path)
    for index, row in iterations_df.iterrows():
        iteration_name = row['Iteration Name']
        start_date_str = f"{row['Start date']} 00:00"  # Append time
        end_date_str = f"{row['End date']} 00:00"      # Append time
        start_date = datetime.strptime(start_date_str, '%d/%m/%Y %H:%M').isoformat()  # Adjust date format
        end_date = datetime.strptime(end_date_str, '%d/%m/%Y %H:%M').isoformat()      # Adjust date format
        
        # Create iteration
        create_iteration(iteration_name, start_date, end_date)

if __name__ == "__main__":
    process_csv()
