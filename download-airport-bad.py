import csv
import requests
from io import StringIO

# URL of the CSV file
url = 'https://datahub.io/core/airport-codes/_r/-/data/airport-codes.csv'

# Fetch the CSV content
response = requests.get(url)
response.raise_for_status()  # Ensure we notice bad responses

# Read the CSV content
csv_file = StringIO(response.text)
reader = csv.DictReader(csv_file)

# Define the headers for the output
headers = ["name", "iso_country", "iso_region", "iata_code"] #, "gps_code", "local_code"]

# Initialize the list with headers
large_airports = [headers]

# Filter and append large airports
for row in reader:
    if row['type'] == 'large_airport':
        large_airports.append([row[h] for h in headers])

# Output the result
for airport in large_airports[:6]:  # Display first 5 records plus header
    print(airport)

# Optionally, write to a Python file
with open('large_airports.py', 'w', encoding='utf-8') as f:
    f.write('large_airports = [\n')
    for airport in large_airports:
        f.write(f'    {airport},\n')
    f.write(']\n')