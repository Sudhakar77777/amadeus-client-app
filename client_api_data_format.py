from datetime import datetime


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
