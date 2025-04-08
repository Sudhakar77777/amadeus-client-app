from amadeus import Client, ResponseError
from basic_logger import logger
from config import config
from utils import pick_random_airports, generate_random_travelers_data
import json
from datetime import datetime

# Print the config for debugging
print(config)

def initialize_amadeus_api():
    try:
        logger.info(config)
        # Initialize the Amadeus client with the logger
        amadeus = Client(
            client_id=config.amadeus_api_key,
            client_secret=config.amadeus_api_secret,
            hostname=config.amadeus_host,  # You can change this to 'production' for real data
            # log_level = "debug"  # enable to see API Request & Response
        )
        print("Init success")
        return amadeus
    except ResponseError as error:
        logger.error(f"ResponseError: {error}")  # Log errors using the logger
        print(f"Error: {error}")


def extract_flight_options(data):
    flight_options = []
    
    for offer in data:
        offer_id = offer['id']
        offer_type = offer['type']
        total_price = offer['price']['total']
        base_price = offer['price']['base']
        currency = offer['price']['currency']
        last_ticketing_date = offer['lastTicketingDate']
        number_of_seats = offer['numberOfBookableSeats']
        
        traveler_pricing = offer['travelerPricings'][0]  # Assuming one traveler pricing
        fare_option = traveler_pricing['fareOption']
        traveler_type = traveler_pricing['travelerType']
        total_travel_price = traveler_pricing['price']['total']
        
        # Extracting itinerary details (simplified for brevity)
        itineraries = []
        for itinerary in offer['itineraries']:
            itinerary_duration = itinerary['duration']
            segments = []
            for segment in itinerary['segments']:
                departure_time = segment['departure']['at']
                arrival_time = segment['arrival']['at']
                segments.append({
                    'departure_time': departure_time,
                    'arrival_time': arrival_time,
                    'flight_number': segment['number'],
                    'carrier_code': segment['carrierCode'],
                })
            itineraries.append({
                'duration': itinerary_duration,
                'segments': segments
            })
        
        flight_options.append({
            'offer_id': offer_id,
            'offer_type': offer_type,
            'total_price': total_price,
            'base_price': base_price,
            'currency': currency,
            'last_ticketing_date': last_ticketing_date,
            'number_of_seats': number_of_seats,
            'fare_option': fare_option,
            'traveler_type': traveler_type,
            'total_travel_price': total_travel_price,
            'itineraries': itineraries
        })
    
    return flight_options


def extract_flight_options2(data):
    flight_options = []
    
    for offer in data:
        offer_id = offer['id']
        offer_type = offer['type']
        total_price = offer['price']['total']
        base_price = offer['price']['base']
        currency = offer['price']['currency']
        last_ticketing_date = offer['lastTicketingDate']
        number_of_seats = offer['numberOfBookableSeats']
        
        traveler_pricing = offer['travelerPricings'][0]  # Assuming one traveler pricing
        fare_option = traveler_pricing['fareOption']
        traveler_type = traveler_pricing['travelerType']
        total_travel_price = traveler_pricing['price']['total']
        
        # Extracting itinerary details (simplified for brevity)
        itineraries = []
        for itinerary in offer['itineraries']:
            itinerary_duration = itinerary['duration']
            segments = []
            
            first_departure_time = None
            last_arrival_time = None
            
            for segment in itinerary['segments']:
                departure_time = segment['departure']['at']
                arrival_time = segment['arrival']['at']
                segment_duration = segment['duration']  # Add the segment duration here
                flight_number = segment['number']
                carrier_code = segment['carrierCode']
                segments.append({
                    'departure_time': departure_time,
                    'arrival_time': arrival_time,
                    'flight_number': flight_number,
                    'carrier_code': carrier_code,
                    'duration': segment_duration  # Add the segment duration to each segment
                })
                
                # Track the first departure and last arrival times
                if not first_departure_time:
                    first_departure_time = departure_time
                last_arrival_time = arrival_time  # Update last arrival time with each segment
            
            # Calculate total trip duration (from first departure to last arrival)
            if first_departure_time and last_arrival_time:
                first_departure = datetime.fromisoformat(first_departure_time)
                last_arrival = datetime.fromisoformat(last_arrival_time)
                total_trip_duration = last_arrival - first_departure
            else:
                total_trip_duration = None

            itineraries.append({
                'duration': itinerary_duration,
                'segments': segments,
                'total_trip_duration': str(total_trip_duration) if total_trip_duration else 'N/A'
            })
        
        flight_options.append({
            'offer_id': offer_id,
            'offer_type': offer_type,
            'total_price': total_price,
            'base_price': base_price,
            'currency': currency,
            'last_ticketing_date': last_ticketing_date,
            'number_of_seats': number_of_seats,
            'fare_option': fare_option,
            'traveler_type': traveler_type,
            'total_travel_price': total_travel_price,
            'itineraries': itineraries
        })
    
    return flight_options


def convert_flight_to_string(flight_data):
    """
    Convert the flight data into a human-readable string.
    """
    flight_options = extract_flight_options2(flight_data)

    # Printing formatted output
    for option in flight_options:
        total_trip_duration = option['itineraries'][0].get('total_trip_duration', 'N/A')

        # Formatted string with total trip duration added after the price
        print(f"Flight Offer ID: {option['offer_id']}")
        print(f"Offer Type: {option['offer_type']}")
        print(f"The total price for this flight is {option['total_price']} {option['currency']}, "
              f"with a total trip duration of {total_trip_duration}.")
        print(f"Base Price: {option['base_price']} {option['currency']}")
        print(f"Last Ticketing Date: {option['last_ticketing_date']}")
        print(f"Available Seats: {option['number_of_seats']}")
        print(f"Fare Option: {option['fare_option']}")
        print(f"Traveler Type: {option['traveler_type']}")
        print(f"Traveler Total Price: {option['total_travel_price']} {option['currency']}")
        print("Itineraries:")

        for itinerary in option['itineraries']:
            print(f"  This itinerary has {len(itinerary['segments'])} segment(s).")
            for idx, segment in enumerate(itinerary['segments'], start=1):
                print(f"  Segment {idx}: Flight {segment['flight_number']} departs from {segment['departure_time']} "
                      f"and arrives at {segment['arrival_time']}. The duration of this segment is {segment['duration']}.")
        print("\n")


def convert_flight_to_string2(flight_data):
    """
    Convert the flight data into a human-readable string.
    """
    flight_options = extract_flight_options2(flight_data)
    human_readable_flights = []
    
    for option in flight_options:
        flight_info = []

        # Flight offer summary
        flight_info.append(f"Flight Offer ID: {option['offer_id']}")
        # flight_info.append(f"Offer Type: {option['offer_type']}")
        total_trip_duration = option['itineraries'][0].get('total_trip_duration', 'N/A')

        # Price information
        flight_info.append(f"The total price for this flight is {option['total_price']} {option['currency']}, "
                           f"with a total trip duration of {total_trip_duration}."
                           f"with a base price of {option['base_price']} {option['currency']}.")

        flight_info.append(f"Tickets must be booked by {option['last_ticketing_date']}.")
        flight_info.append(f"There are {option['number_of_seats']} available seats for this offer.")
        flight_info.append(f"The selected fare option is {option['fare_option']}.")

        # Traveler pricing information
        flight_info.append(f"For an adult traveler, the total price is {option['total_travel_price']} {option['currency']}.")

        # Itinerary details
        itinerary_details = []
        for itinerary in option['itineraries']:
            itinerary_segments = []
            num_segments = len(itinerary['segments'])
            itinerary_segments.append(f"This itinerary has {num_segments} segments.")
            for i, segment in enumerate(itinerary['segments'], start=1):
                departure = segment['departure_time']
                arrival = segment['arrival_time']
                flight_number = segment['flight_number']
                departure_airport = segment['departure_time'].split('T')[0]  # Extracting the date for simplicity
                arrival_airport = segment['arrival_time'].split('T')[0]  # Extracting the date for simplicity
                segment_duration = segment['duration']

                # Segment duration included
                segment_text = (f"Segment {i}: Flight {flight_number} departs from {departure_airport} at {departure} "
                                f"and arrives at {arrival_airport} at {arrival}. The duration of this segment is {segment_duration}.")
                itinerary_segments.append(segment_text)
            
            itinerary_details.append(" ".join(itinerary_segments))

        # Combine itinerary information
        flight_info.append("This flight includes the following itineraries: " + " | ".join(itinerary_details))

        # Add the human-readable flight details to the list
        human_readable_flights.append(" ".join(flight_info))

    print(type(human_readable_flights))
    print(len(human_readable_flights))
    print(human_readable_flights)
    # Join all flights into one string and return it
    return "\n\n".join(human_readable_flights)


def get_flight_search(amadeus: Client, originLocationCode='MAD', destinationLocationCode='ATH', departureDate='2025-11-01', adults=1):
    try:
        response = amadeus.shopping.flight_offers_search.get(
            originLocationCode=originLocationCode,
            destinationLocationCode=destinationLocationCode,
            departureDate=departureDate,
            adults=adults
        )
        # print(response.data[0:3])
        # print(json.dumps(response.data[0:1], indent=4))
        print(len(response.data))
        response_data = convert_flight_to_string2(response.data[0:3])
        print(type(response_data))
        print(response_data)
    except ResponseError as error:
        print(error)


def convert_flight_details_to_sentences(booking_data):
    # Parse basic flight order information
    flight_order_id = booking_data['id']
    flight_offer = booking_data['flightOffers'][0]
    
    # Prepare the flight details
    itineraries = flight_offer['itineraries']
    segments = []
    
    for itinerary in itineraries:
        for segment in itinerary['segments']:
            departure = segment['departure']
            arrival = segment['arrival']
            
            # Handle missing terminal information
            departure_terminal = departure.get('terminal', 'N/A')
            arrival_terminal = arrival.get('terminal', 'N/A')
            
            # Format dates and times
            departure_time = datetime.fromisoformat(departure['at']).strftime("%B %d, %Y at %H:%M")
            arrival_time = datetime.fromisoformat(arrival['at']).strftime("%B %d, %Y at %H:%M")
            
            # Build segment description
            segment_info = (
                f"Flight {segment['number']} from {departure['iataCode']} (Terminal {departure_terminal}) "
                f"to {arrival['iataCode']} (Terminal {arrival_terminal}) "
                f"departing on {departure_time} and arriving at {arrival_time}."
            )
            segments.append(segment_info)
    
    # Price details
    total_price = flight_offer['price']['total']
    currency = flight_offer['price']['currency']
    
    # Collect traveler details
    traveler_details = []
    for traveler in booking_data['travelers']:
        traveler_name = traveler['name']['firstName'] + ' ' + traveler['name']['lastName']
        traveler_price = flight_offer['travelerPricings'][0]['price']['total']  # Assuming equal pricing for all passengers ## Validate this assumption
        traveler_details.append(f"{traveler_name} has booked this flight for {traveler_price} {currency}.")
    
    # Constructing final sentence for travelers
    traveler_info = "\n".join(traveler_details)

    # Construct the final sentence for the entire booking
    flight_details = f"Booking Reference: {flight_order_id}\n{traveler_info}\nThe flight details are as follows:\n"
    flight_details += "\n".join(segments)  # Add all segments dynamically
    flight_details += f"\nThe total price for the flight is {total_price} {currency}.\n"
    
    return {f"Booking_data for {flight_order_id}": str(flight_details)}


def format_flight_booking2(data):
    # Parse basic flight order information
    flight_order_id = data['id']
    flight_offer = data['flightOffers'][0]
    
    # Prepare the flight details
    itineraries = flight_offer['itineraries']
    first_leg = itineraries[0]['segments'][0]
    second_leg = itineraries[0]['segments'][1]
    
    departure_1 = first_leg['departure']
    arrival_1 = first_leg['arrival']
    departure_2 = second_leg['departure']
    arrival_2 = second_leg['arrival']
    
    # Handle missing terminal information
    departure_1_terminal = departure_1.get('terminal', 'N/A')
    arrival_1_terminal = arrival_1.get('terminal', 'N/A')
    departure_2_terminal = departure_2.get('terminal', 'N/A')
    arrival_2_terminal = arrival_2.get('terminal', 'N/A')
    
    # Format dates and times
    departure_1_time = datetime.fromisoformat(departure_1['at']).strftime("%B %d, %Y at %H:%M")
    arrival_1_time = datetime.fromisoformat(arrival_1['at']).strftime("%B %d, %Y at %H:%M")
    departure_2_time = datetime.fromisoformat(departure_2['at']).strftime("%B %d, %Y at %H:%M")
    arrival_2_time = datetime.fromisoformat(arrival_2['at']).strftime("%B %d, %Y at %H:%M")
    
    # Flight segments description
    first_segment_info = (
        f"Flight {first_leg['number']} from {departure_1['iataCode']} (Terminal {departure_1_terminal}) "
        f"to {arrival_1['iataCode']} (Terminal {arrival_1_terminal}) "
        f"departing on {departure_1_time} and arriving at {arrival_1_time}."
    )
    
    second_segment_info = (
        f"Flight {second_leg['number']} from {departure_2['iataCode']} (Terminal {departure_2_terminal}) "
        f"to {arrival_2['iataCode']} (Terminal {arrival_2_terminal}) "
        f"departing on {departure_2_time} and arriving at {arrival_2_time}."
    )
    
    # Price details
    total_price = flight_offer['price']['total']
    currency = flight_offer['price']['currency']
    
    # Collect traveler details
    traveler_details = []
    for traveler in data['travelers']:
        traveler_name = traveler['name']['firstName'] + ' ' + traveler['name']['lastName']
        traveler_price = flight_offer['travelerPricings'][0]['price']['total']  # Assuming equal pricing for all passengers
        traveler_details.append(f"{traveler_name} has booked this flight for {traveler_price} {currency}.")
    
    # Constructing final sentence for travelers
    traveler_info = "\n".join(traveler_details)

    # Construct the final sentence for the entire booking
    flight_details = f"Booking Reference: {flight_order_id}\n{traveler_info}\n\nThe flight details are as follows:\n"
    flight_details += f"{first_segment_info}\n{second_segment_info}\n"
    flight_details += f"The total price for the flight is {total_price} {currency}.\n"
    
    return {f"Booking_data for {flight_order_id}": str(flight_details)}


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
        # print(response.data)
        # print(json.dumps(response.data, indent=4))
        print(convert_flight_details_to_sentences(response.data))
    
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
    # booking_id = 'eJzTd9cPcffyNfMBAAtTAlo%3D'
    logger.debug(f"Booking is complete for PNR# {booking_id}")
    get_booking_details(amadeus, booking_id)

    # #3 -- Testing?? -- Descoped by client as this Amadeus api no longer exist?
    # logger.debug("Calling Use case #3")
    # get_baggage_details(amadeus, 'BA')


if __name__ == "__main__":
    logger.debug("App begins...")
    main()
