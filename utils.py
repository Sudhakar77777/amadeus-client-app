import random
from faker import Faker
from datetime import datetime, timedelta, date

def pick_random_airports():
    # Major European airport hubs
    european_airports = [
        "AMS",  # Amsterdam Schiphol, Netherlands
        "CDG",  # Charles de Gaulle, France
        "FRA",  # Frankfurt Airport, Germany
        "LHR",  # London Heathrow, United Kingdom
        "MUC",  # Munich Airport, Germany
        "MAD",  # Madrid Barajas, Spain
        "ZRH",  # Zurich Airport, Switzerland
        "VIE",  # Vienna International, Austria
        "FCO",  # Leonardo da Vinci International, Rome, Italy
        "BCN",  # Barcelona El Prat, Spain
        "DUB",  # Dublin Airport, Ireland
        "OSL",  # Oslo Gardermoen, Norway
    ]

    # Major USA airport hubs
    usa_airports = [
        "ATL",  # Hartsfield-Jackson Atlanta, Georgia
        "LAX",  # Los Angeles International, California
        "ORD",  # O'Hare International, Chicago, Illinois
        "JFK",  # John F. Kennedy International, New York
        "DFW",  # Dallas/Fort Worth International, Texas
        "DEN",  # Denver International, Colorado
        "SFO",  # San Francisco International, California
        "SEA",  # Seattle-Tacoma International, Washington
        "MIA",  # Miami International, Florida
        "EWR",  # Newark Liberty International, New Jersey
        "LGA",  # LaGuardia Airport, New York
        "PHX",  # Phoenix Sky Harbor International, Arizona
    ]
    
    # Select one random airport from each list
    european_airport = random.choice(european_airports)
    usa_airport = random.choice(usa_airports)

    # Override with both europe airport codes for testing
    # european_airport, usa_airport = random.sample(european_airports, 2)

    # Calculate the departure date range
    today = date.today()
    min_days = 30
    max_days = 180
    
    # Random number of days to add between 30 and 180
    random_days = random.randint(min_days, max_days)
    
    # Calculate the departure date
    departure_date = today + timedelta(days=random_days)
    
    # Random number of adult passengers between 1 and 2
    number_of_passengers = random.randint(1, 2)

    return european_airport, usa_airport, departure_date, number_of_passengers

# Example usage:
european_airport, usa_airport, departure_date, number_of_passengers = pick_random_airports()
# print(f"Random European Airport: {european_airport}")
# print(f"Random USA Airport: {usa_airport}")
# print(f"Random Departure Date: {departure_date}")
# print(f"Number of Adult Passengers: {number_of_passengers}")


# Initialize Faker to generate random data
faker = Faker()

def generate_random_travelers_data(passenger_count):
    travelers = []
    
    # Generate 'passenger_count' number of traveler records
    for passenger_id in range(1, passenger_count + 1):
        # Generate random name, email, and phone number using Faker
        first_name = faker.first_name()
        last_name = faker.last_name()
        email_address = faker.email()
        country_calling_code = faker.random_int(min=1, max=999)  # Random country calling code
        phone_number = faker.random_number(digits=9)  # Ensure only digits for the phone number
        
        # Convert to a string and ensure it's a valid phone number
        phone_number_str = str(phone_number).zfill(9)  # Ensure it's 9 digits (if necessary)
        
        # Randomly choose a birth date between 18 and 50 years ago
        birth_date = faker.date_of_birth(minimum_age=18, maximum_age=50)
        birth_date_str = birth_date.strftime("%Y-%m-%d")
        
        # Random gender (choose between 'MALE' or 'FEMALE')
        gender = random.choice(['MALE', 'FEMALE'])

        # Random Passport document generation (validity until 10 years from issuance)
        # Ensure the issuance date is within the last 8 years but at least 1 year ago
        current_date = datetime.now()
        min_issuance_date = current_date - timedelta(days=365*8)  # 8 years ago
        max_issuance_date = current_date - timedelta(days=365)  # 1 year ago
        
        # Generate issuance date in this range (within the last 8 years, but at least 1 year ago)
        issuance_date = faker.date_between(start_date=min_issuance_date, end_date=max_issuance_date)
        
        # Expiry date should be 10 years after the issuance date
        expiry_date = issuance_date + timedelta(days=365*10)  # Passport expires 10 years after issuance
        document_number = faker.bothify(text='#######')  # Random document number format
        
        
        # Create the traveler record
        traveler = {
            'id': str(passenger_id),  # Sequential ID starting from 1
            'dateOfBirth': birth_date_str,
            'name': {
                'firstName': first_name,
                'lastName': last_name
            },
            'gender': gender,
            'contact': {
                'emailAddress': email_address,
                'phones': [{
                    'deviceType': 'MOBILE',
                    'countryCallingCode': str(country_calling_code),
                    'number': phone_number_str  # Phone number with digits only
                }]
            },
            'documents': [{
                'documentType': 'PASSPORT',
                'birthPlace': faker.city(),
                'issuanceLocation': faker.city(),
                'issuanceDate': issuance_date.strftime("%Y-%m-%d"),
                'number': document_number,
                'expiryDate': expiry_date.strftime("%Y-%m-%d"),
                'issuanceCountry': 'ES',  # Assuming Spain for simplicity
                'validityCountry': 'ES',  # Assuming Spain for simplicity
                'nationality': 'ES',  # Assuming Spain for simplicity
                'holder': True
            }]
        }
        
        # Append the traveler to the list
        travelers.append(traveler)
    
    # Print generated records
    for traveler in travelers:
        print(traveler)
    
    return travelers


# Example usage:
# passenger_count = 3  # Example: Generate 3 random traveler records
# random_travelers = generate_random_travelers_data(passenger_count)

# # Print generated records
# for traveler in random_travelers:
#     print(traveler)
