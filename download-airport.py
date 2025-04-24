import csv
import requests
import json

# Fetch data from OpenFlights
url = 'https://raw.githubusercontent.com/jpatokal/openflights/master/data/airports.dat'
response = requests.get(url)
response.raise_for_status()
lines = response.content.decode('utf-8').splitlines()

# Parse with CSV reader
reader = csv.reader(lines)

# Define output list with header
airports_data = [["airport_name", "city", "country", "iata_code", "timezone"]]

# Process each line
for row in reader:
    name = row[1]
    city = row[2]
    country = row[3]
    iata_code = row[4]
    timezone = row[11] if row[11] != '\\N' else ''

    if iata_code and len(iata_code) == 3 and iata_code.isalpha():
        # Clean escaped apostrophes
        cleaned_row = [
            name.replace("\\'", "'"),
            city.replace("\\'", "'"),
            country.replace("\\'", "'"),
            iata_code,
            timezone.replace("\\'", "'")
        ]
        airports_data.append(cleaned_row)

# Save with double quotes
with open('data_airports.py', 'w', encoding='utf-8') as f:
    f.write('data_airports = [\n')
    for airport in airports_data:
        f.write('    ' + json.dumps(airport, ensure_ascii=False) + ',\n')
    f.write(']\n')