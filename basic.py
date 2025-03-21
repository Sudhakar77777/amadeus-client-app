from amadeus import Client, ResponseError
from basic_logger import logger
from config import config
from utils import pick_random_airports, generate_random_travelers_data

# Print the config for debugging
print(config)

def initialize_amadeus_api():
    try:
        # Initialize the Amadeus client with the logger
        amadeus = Client(
            client_id=config.amadeus_api_key,
            client_secret=config.amadeus_api_secret,
            hostname='test',  # You can change this to 'production' for real data
            # log_level = "debug"  # enable to see API Request & Response
        )
        print("Init success")
        return amadeus
    except ResponseError as error:
        logger.error(f"ResponseError: {error}")  # Log errors using the logger
        print(f"Error: {error}")


def get_flight_search(amadeus: Client, originLocationCode='MAD', destinationLocationCode='ATH', departureDate='2025-11-01', adults=1):
    try:
        response = amadeus.shopping.flight_offers_search.get(
            originLocationCode=originLocationCode,
            destinationLocationCode=destinationLocationCode,
            departureDate=departureDate,
            adults=adults
        )
        print(response.data[0:3])
    except ResponseError as error:
        print(error)

# def get_booking_details(amadeus: Client, booking_id='ABC123'):
#     try:
#         response = amadeus.booking.flight_orders(flight_order_id=booking_id).get()
#         print(response.data)
#     except ResponseError as error:
#         print(error)

def get_booking_details(amadeus: Client, booking_id='ABC123'):
    try:
        # Correct method to get booking details using flight_orders (plural)
        response = amadeus.booking.flight_order(booking_id).get()
        # Print the response data
        print(response.data)
    
    except ResponseError as error:
        # Handle any errors (e.g., invalid booking_id or request failure)
        print(f"Error occurred: {error}")

def get_baggage_details(amadeus: Client, airlineCode='BA'):
    try:
        response = amadeus.get(f'/v1/reference-data/airlines/{airlineCode}/baggage', logger=logger)
        print(response.data)
    except ResponseError as error:
        print(error)

def get_traveler_data():
    traveler = {
    'id': '1',
    'dateOfBirth': '1991-03-07',
    'name': {
        'firstName': 'Sofia',
        'lastName': 'Perez'
    },
    'gender': 'FEMALE',
    'contact': {
        'emailAddress': 'sofia.perez@example.com',
        'phones': [{
            'deviceType': 'MOBILE',
            'countryCallingCode': '81',
            'number': '987654321'
        }]
    },
    'documents': [{
        'documentType': 'PASSPORT',
        'birthPlace': 'Valencia',
        'issuanceLocation': 'Madrid',
        'issuanceDate': '2016-04-03',
        'number': '2345678',
        'expiryDate': '2026-04-03',
        'issuanceCountry': 'ES',
        'validityCountry': 'ES',
        'nationality': 'ES',
        'holder': True
    }]
}
    return traveler


def search_flight(amadeus):
    # Retry until success or valid response is received
    while True:
        try:
            # Pick random airports, date, and number of passengers
            originLocationCode, destinationLocationCode, departureDate, adults = pick_random_airports()
            # Make the flight search API call
            logger.debug(f"Searching for flights from {originLocationCode} to {destinationLocationCode} "
                         f"on {departureDate} for {adults} adult(s)")

            flight_search = amadeus.shopping.flight_offers_search.get(
                originLocationCode=originLocationCode,
                destinationLocationCode=destinationLocationCode,
                departureDate=departureDate,
                adults=adults
            ).data

            # If the response has no errors, log and return the data
            if flight_search:
                logger.info(f"Flight search is successful. Returning match# {len(flight_search)}.")
                return flight_search, adults
            
        except ResponseError as error:
            # Handle specific API errors such as 400 if route doesn't exist
            if error.status_code == 400:
                logger.warning(f"Route not found for {originLocationCode} to {destinationLocationCode}. Retrying...")
            else:
                logger.error(f"An error occurred: {error}")
                break  # Exit the loop on other errors


def place_an_order(amadeus):
    try:
        # Flight Offers Search to find for flights between 2 random airports X to Y
        logger.debug(f"Begin to search for flights.")
        flight_search, traveler_count = search_flight(amadeus)

        # Flight Offers Price to confirm the price of the chosen flight
        logger.debug(f"Selcting and confirming the price for the first result(cheapest).")
        price_confirm = amadeus.shopping.flight_offers.pricing.post(
            flight_search[0]).data
        
        # Book for random passenger data
        logger.debug(f"Get random traveller data.")
        traveler = generate_random_travelers_data(traveler_count)

        # Flight Create Orders to book the flight
        logger.debug(f"Begin to book the selected flight.")
        try:
            booked_flight = amadeus.booking.flight_orders.post(
                flight_search[0], traveler).data
        except ResponseError as error:
            # Log more details about the error
            # Log the full details of the error
            logger.error(f"Amadeus ResponseError occurred: {error.code}")
            logger.error(f"Error Status Code: {error.response.status_code}")
            
            # Log the description for more detailed info
            logger.error(f"Error Description: {error.description()}")
            
            # In case you want to access the errors in the response object
            if 'errors' in error.response.result:
                for e in error.response.result['errors']:
                    logger.error(f"Error Code: {e.get('code')}")
                    logger.error(f"Error Detail: {e.get('detail')}")
            
            # Raise the error after logging it
            raise error
        
        logger.debug(booked_flight)
        logger.debug(booked_flight['id'])
        return booked_flight['id']

    except ResponseError as error:
        raise error


def main():
    logger.debug("Initializing amadeus api")
    amadeus = initialize_amadeus_api()

    # print(amadeus.client_credentials.get_token())
    
    # #1 -- Works, by default gets cheapest flight for the search query
    # logger.debug("Calling Use case #1")
    # get_flight_search(amadeus, 
    #                     originLocationCode='JFK',
    #                     destinationLocationCode='LHR',
    #                     departureDate='2025-06-01',
    #                     adults=1)
    
    # #2 -- Works
    logger.debug("Calling Use case #2")
    booking_id = place_an_order(amadeus)
    logger.debug(f"Booking is complete for PNR# {booking_id}")
    # get_booking_details(amadeus, booking_id)

    # #3 -- Testing?? -- Descoped by client as this Amadeus api no longer exist?
    # logger.debug("Calling Use case #3")
    # get_baggage_details(amadeus, 'BA')


if __name__ == "__main__":
    logger.debug("App begins...")
    main()
