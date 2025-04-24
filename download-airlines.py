import csv
import requests
import json

# Safe cleaner: fix escaped apostrophes and double backslashes
def clean(text):
    return text.replace('\\\\', '\\').replace("\\'", "'").replace('\u0000', '').strip()

# URL to airlines.dat
url = 'https://raw.githubusercontent.com/jpatokal/openflights/master/data/airlines.dat'

# Request data
response = requests.get(url)
response.raise_for_status()

# Decode content
lines = response.content.decode('utf-8').splitlines()
reader = csv.reader(lines)

# Build list with selected fields
airlines_data = [["airline_name", "alias", "iso_country", "iata_code"]]

for row in reader:
    if len(row) < 8:
        continue

    name = clean(row[1])
    alias = clean(row[2]) if row[2] != '\\N' else ''
    country = clean(row[6])
    iata = row[3] if row[3] != '\\N' else ''

    if iata and len(iata) == 2:
        airlines_data.append([name, alias, country, iata])

# Save with proper double quotes and Unicode preserved
with open('data_airlines.py', 'w', encoding='utf-8') as f:
    f.write('data_airlines = [\n')
    for airline in airlines_data:
        f.write('    ' + json.dumps(airline, ensure_ascii=False) + ',\n')
    f.write(']\n')
