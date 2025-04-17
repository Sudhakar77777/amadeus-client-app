from datetime import datetime
from base_logger import logger
from pprint import pformat

def extract_flight_options_data(data) -> list[dict]:
    flight_options = []

    for offer in data:
        offer_id = offer["id"]
        offer_type = offer["type"]
        total_price = offer["price"]["total"]
        base_price = offer["price"]["base"]
        currency = offer["price"]["currency"]
        last_ticketing_date = offer["lastTicketingDate"]
        number_of_seats = offer["numberOfBookableSeats"]

        traveler_pricing = offer["travelerPricings"][0]  # Assuming one traveler pricing
        fare_option = traveler_pricing["fareOption"]
        traveler_type = traveler_pricing["travelerType"]
        total_travel_price = traveler_pricing["price"]["total"]

        # Extracting itinerary details (simplified for brevity)
        itineraries = []
        for itinerary in offer["itineraries"]:
            itinerary_duration = itinerary["duration"]
            segments = []

            first_departure_time = None
            last_arrival_time = None

            for segment in itinerary["segments"]:
                departure_airport = segment["departure"]["iataCode"]
                departure_terminal = segment["departure"].get("terminal", "TBD")
                departure_time = segment["departure"]["at"]
                arrival_airport = segment["arrival"]["iataCode"]
                arrival_terminal = segment["arrival"].get("terminal", "TBD")
                arrival_time = segment["arrival"]["at"]
                segment_duration = segment["duration"]  # Add the segment duration here
                flight_number = segment["number"]
                carrier_code = segment["carrierCode"]
                segments.append(
                    {
                        "departure_airport": departure_airport,
                        "departure_terminal": departure_terminal,
                        "departure_time": departure_time,
                        "arrival_airport": arrival_airport,
                        "arrival_terminal": arrival_terminal,
                        "arrival_time": arrival_time,
                        "flight_number": flight_number,
                        "carrier_code": carrier_code,
                        "duration": segment_duration,  # Add the segment duration to each segment
                    }
                )

                # Track the first departure and last arrival times
                if not first_departure_time:
                    first_departure_time = departure_time
                last_arrival_time = (
                    arrival_time  # Update last arrival time with each segment
                )

            # Calculate total trip duration (from first departure to last arrival)
            if first_departure_time and last_arrival_time:
                first_departure = datetime.fromisoformat(first_departure_time)
                last_arrival = datetime.fromisoformat(last_arrival_time)
                total_trip_duration = last_arrival - first_departure
            else:
                total_trip_duration = None

            itineraries.append(
                {
                    "duration": itinerary_duration,
                    "segments": segments,
                    "total_trip_duration": str(total_trip_duration)
                    if total_trip_duration
                    else "N/A",
                }
            )

        flight_options.append(
            {
                "offer_id": offer_id,
                "offer_type": offer_type,
                "total_price": total_price,
                "base_price": base_price,
                "currency": currency,
                "last_ticketing_date": last_ticketing_date,
                "number_of_seats": number_of_seats,
                "fare_option": fare_option,
                "traveler_type": traveler_type,
                "total_travel_price": total_travel_price,
                "itineraries": itineraries,
            }
        )

    return flight_options


def convert_flight_options_to_sentences(flight_data) -> str:
    """
    Convert the flight data into a human-readable string.
    """
    flight_options = extract_flight_options_data(flight_data)
    human_readable_flights = []

    for option in flight_options:
        flight_info = [f"Flight Offer ID: {option['offer_id']}"]

        # Flight offer summary
        # flight_info.append(f"Offer Type: {option['offer_type']}")
        total_trip_duration = option["itineraries"][0].get("total_trip_duration", "N/A")

        # Price information
        flight_info.append(
            f"The total price for this flight is {option['total_price']} {option['currency']}, "
            f"with a total trip duration of {total_trip_duration}."
        )

        flight_info.append(
            f"Tickets must be booked by {option['last_ticketing_date']}."
        )
        flight_info.append(
            f"There are {option['number_of_seats']} available seats for this offer."
        )
        flight_info.append(f"The selected fare option is {option['fare_option']}.")

        # Traveler pricing information
        flight_info.append(
            f"For an adult traveler, the total price is {option['total_travel_price']} {option['currency']}."
        )

        # Itinerary details
        itinerary_details = []
        for itinerary in option["itineraries"]:
            itinerary_segments = []
            num_segments = len(itinerary["segments"])
            itinerary_segments.append(f"This itinerary has {num_segments} segments.")
            for i, segment in enumerate(itinerary["segments"], start=1):
                carrier_code = segment["carrier_code"]
                flight_number = segment["flight_number"]
                departure_airport = segment["departure_airport"]
                departure_terminal = segment["departure_terminal"]
                departure_datetime = segment["departure_time"].split("T")
                departure_date = departure_datetime[0]
                departure_time = departure_datetime[1]
                arrival_airport = segment["arrival_airport"]
                arrival_terminal = segment["arrival_terminal"]
                arrival_datetime = segment["arrival_time"].split("T")
                arrival_date = arrival_datetime[0]
                arrival_time = arrival_datetime[1]
                segment_duration = segment["duration"]

                # Segment duration included
                segment_text = (
                    f"Segment {i}: Flight {carrier_code}{flight_number} from {departure_airport}(Terminal {departure_terminal}) to {arrival_airport}(Terminal {arrival_terminal}) "
                    f"departing on {departure_date} at {departure_time} and arriving on {arrival_date} at {arrival_time}. The duration of this segment is {segment_duration}."
                )
                itinerary_segments.append(segment_text)

            itinerary_details.append(" ".join(itinerary_segments))

        # Combine itinerary information
        flight_info.append(
            "This flight includes the following itineraries: "
            + " | ".join(itinerary_details)
        )

        # Add the human-readable flight details to the list
        human_readable_flights.append(" ".join(flight_info))

    # Join all flights into one string and return it
    return human_readable_flights  # "\n\n".join(human_readable_flights)


def convert_flight_details_to_sentences(booking_data):
    # Parse basic flight order information
    flight_order_id = booking_data["id"]
    flight_offer = booking_data["flightOffers"][0]

    # Prepare the flight details
    itineraries = flight_offer["itineraries"]
    segments = []

    for itinerary in itineraries:
        for segment in itinerary["segments"]:
            departure = segment["departure"]
            arrival = segment["arrival"]

            # Handle missing terminal information
            departure_terminal = departure.get("terminal", "N/A")
            arrival_terminal = arrival.get("terminal", "N/A")

            # Format dates and times
            departure_time = datetime.fromisoformat(departure["at"]).strftime(
                "%B %d, %Y at %H:%M"
            )
            arrival_time = datetime.fromisoformat(arrival["at"]).strftime(
                "%B %d, %Y at %H:%M"
            )

            # Build segment description
            segment_info = (
                f"Flight {segment['carrierCode']}{segment['number']} from {departure['iataCode']}(Terminal {departure_terminal}) "
                f"to {arrival['iataCode']}(Terminal {arrival_terminal}) "
                f"departing on {departure_time} and arriving on {arrival_time}."
            )
            segments.append(segment_info)

    # Price details
    total_price = flight_offer["price"]["total"]
    currency = flight_offer["price"]["currency"]

    # Collect traveler details
    traveler_details = []
    for traveler in booking_data["travelers"]:
        traveler_name = (
            traveler["name"]["firstName"] + " " + traveler["name"]["lastName"]
        )
        traveler_price = flight_offer["travelerPricings"][0]["price"][
            "total"
        ]  # Assuming equal pricing for all passengers ## Validate this assumption
        traveler_details.append(
            f"{traveler_name} has booked this flight for {traveler_price} {currency}."
        )

    # Constructing final sentence for travelers
    traveler_info = "\n".join(traveler_details)

    # Construct the final sentence for the entire booking
    flight_details = f"Booking Reference: {flight_order_id}\n{traveler_info}\nThe flight details are as follows:\n"
    flight_details += "\n".join(segments)  # Add all segments dynamically
    flight_details += f"\nThe total price for the flight is {total_price} {currency}.\n"

    return {f"Booking_data for {flight_order_id}": str(flight_details)}

def parse_flight_status(response):
    flight_details = {
        'scheduledDepartureDate': 'Unknown',
        'carrierCode': 'Unknown',
        'flightNumber': 'Unknown',
        'departurePoint': 'Unknown',
        'arrivalPoint': 'Unknown',
        'departureTime': 'Unknown',
        'arrivalTime': 'Unknown',
        'aircraftType': 'Unknown',
        'flightDuration': 'Unknown',
        'operatingCarrierCode': 'Unknown',
        'operatingFlightNumber': 'Unknown'
    }

    if isinstance(response, list) and len(response) > 0:
        flight_record = response[0]

        # Basic info
        flight_details['scheduledDepartureDate'] = flight_record.get('scheduledDepartureDate', 'Unknown')
        flight_designator = flight_record.get('flightDesignator', {})
        flight_details['carrierCode'] = flight_designator.get('carrierCode', 'Unknown')
        flight_details['flightNumber'] = flight_designator.get('flightNumber', 'Unknown')

        # Flight points
        flight_points = flight_record.get('flightPoints', [])
        if len(flight_points) >= 2:
            flight_details['departurePoint'] = flight_points[0].get('iataCode', 'Unknown')
            departure_timings = flight_points[0].get('departure', {}).get('timings', [{}])
            flight_details['departureTime'] = departure_timings[0].get('value', 'Unknown')

            flight_details['arrivalPoint'] = flight_points[1].get('iataCode', 'Unknown')
            arrival_timings = flight_points[1].get('arrival', {}).get('timings', [{}])
            flight_details['arrivalTime'] = arrival_timings[0].get('value', 'Unknown')
        else:
            logger.warning("⚠️ Incomplete flightPoints data.")

        # Aircraft info
        legs = flight_record.get('legs', [])
        if legs:
            leg = legs[0]
            flight_details['aircraftType'] = leg.get('aircraftEquipment', {}).get('aircraftType', 'Unknown')

        # Segment duration and codeshare
        segments = flight_record.get('segments', [])
        if segments:
            segment = segments[0]
            flight_details['flightDuration'] = segment.get('scheduledSegmentDuration', 'Unknown')

            operating_flight = segment.get('partnership', {}).get('operatingFlight', {})
            flight_details['operatingCarrierCode'] = operating_flight.get('carrierCode', 'Unknown')
            flight_details['operatingFlightNumber'] = operating_flight.get('flightNumber', 'Unknown')

        return flight_details
    else:
        logger.error("❌ No valid flight record found in response.")
        return None
    

def convert_flight_status_to_sentences(details):
    details = parse_flight_status(details)
    sentence = (
        f"Flight {details['carrierCode']} {details['flightNumber']} is scheduled to depart from "
        f"{details['departurePoint']} at {details['departureTime']} and arrive at "
        f"{details['arrivalPoint']} at {details['arrivalTime']}."
    )

    # Add flight duration if available
    if details['flightDuration'] != 'Unknown':
        # Convert ISO 8601 duration to readable format if needed
        duration = details['flightDuration'].replace('PT', '').lower()
        sentence += f" The flight duration is {duration}."

    # Add operating carrier info if it’s a codeshare
    if (details['operatingCarrierCode'] != 'Unknown' and 
        (details['operatingCarrierCode'] != details['carrierCode'] or 
         str(details['operatingFlightNumber']) != str(details['flightNumber']))):
        sentence += f" It is operated by {details['operatingCarrierCode']} as flight {details['operatingFlightNumber']}."

    # Add aircraft type if available
    if details['aircraftType'] != 'Unknown':
        sentence += f" The aircraft type is {details['aircraftType']}."

    return sentence

def convert_airline_destinations_to_sentences(destinations, airline_code):
    if not destinations:
        return f"No destination data available for airline {airline_code}."

    lines = [f"✈️ Destinations served by {airline_code}:\n"]

    for dest in destinations:
        name = dest.get('name', 'Unknown City')
        airport = dest.get('iataCode', 'Unknown Airport')
        country = dest.get('address', {}).get('countryName', 'Unknown Country')
        state = dest.get('address', {}).get('stateCode')

        state_info = f", {state}" if state else ""
        lines.append(f"• {name} ({airport}), {country}{state_info}")

    return "\n".join(lines)
