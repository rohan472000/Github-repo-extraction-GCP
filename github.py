import requests
from datetime import datetime
from google.cloud import bigquery
from google.oauth2 import service_account

# Make a request to the GitHub API to get the 100 most rated public repositories
response = requests.get('https://api.github.com/search/repositories?q=stars:>0&sort=stars&per_page=100')

# Convert the response data to JSON format
data = response.json()

# Create a list to store the repository data
repos_data = []

# Loop through each repository in the response data
for repo in data['items']:
    # Extract the repository data we want
    name = repo['name']
    description = repo['description']
    stars = repo['stargazers_count']
    forks = repo['forks_count']
    language = repo['language']
    created_date = datetime.strptime(repo['created_at'], '%Y-%m-%dT%H:%M:%SZ').date()

    # Add the repository data to the list
    repos_data.append((name, description, stars, forks, language, created_date))

# Initialize the BigQuery client
credentials = service_account.Credentials.from_service_account_file
              ('/home/service.json')

client = bigquery.Client(credentials=credentials, project='clean-phone-438712')


# Define the BigQuery table schema
schema = [
    bigquery.SchemaField('name', 'STRING'),
    bigquery.SchemaField('description', 'STRING'),
    bigquery.SchemaField('stars', 'INTEGER'),
    bigquery.SchemaField('forks', 'INTEGER'),
    bigquery.SchemaField('language', 'STRING'),
    bigquery.SchemaField('created_date', 'DATE')
]

# Define the BigQuery table reference
table_ref = client.dataset('earthquake').table('table_m')

# Create the BigQuery table if it doesn't exist
try:
    client.get_table(table_ref)
except:
    client.create_table(bigquery.Table(table_ref, schema=schema))

# Insert the repository data into the BigQuery table
table = client.get_table(table_ref)
rows_to_insert = [list(repo_data[0:5]) + [repo_data[5].strftime('%Y-%m-%d')] 
                  for repo_data in repos_data]
errors = client.insert_rows(table, rows_to_insert)

if errors == []:
    print('Data inserted into BigQuery successfully!')
else:
    print(f'Errors occurred while inserting data into BigQuery: {errors}')
