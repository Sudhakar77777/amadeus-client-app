import json
import time
from functools import wraps
from datetime import datetime
from amadeus import Client, ResponseError
from base_logger import logger
from base_config import config
from client_api_data_format import convert_flight_details_to_sentences, convert_flight_options_to_sentences, convert_flight_status_to_sentences, convert_airline_destinations_to_sentences, convert_cancellation_response_to_sentences
from utils import pick_random_airports, generate_random_travelers_data
from pprint import pformat
from typing import Optional, Literal


def timeit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.debug(f"➡️: {func.__name__} started...")
        start = time.time()
        try:
            return func(*args, **kwargs)
        finally:
            logger.debug(f"⏱️: {func.__name__} finished in {time.time() - start:.2f}s")
    return wrapper


class AmadeusAPIClient:
    def __init__(self, config):
        try:
            logger.debug(f"{config=}")
            self.client = Client(
                client_id=config.amadeus_api_key,
                client_secret=config.amadeus_api_secret,
                host='test.api.amadeus.com', #Ideally not required has to patch becoz of unknow error scenario
                hostname=config.amadeus_host, # You can change this to 'production' for real data
                log_level = "debug"  # enable to see API Request & Response
            )
            logger.info("✅ Amadeus API initialized.")
            logger.debug(f"{self.client=}")
        except ResponseError as error:
            logger.error(f"❌ Init error: {error}")
            raise

    TravelClass = Literal['ECONOMY', 'PREMIUM_ECONOMY', 'BUSINESS', 'FIRST']

    @timeit
    def get_flight_search(
        self,
        origin: str,
        dest: str,
        date: str,
        adults: int,
        return_date: Optional[str] = None,
        children: Optional[int] = None,
        travel_class: TravelClass = 'ECONOMY',
        included_airline_codes: Optional[str] = 'WY',
        non_stop: bool = False,
        max_results: int = 5
    ) -> str:
        try:
            # Build the request parameters
            non_stop_str = "true" if non_stop else "false"  
            params = {
                'originLocationCode': origin,
                'destinationLocationCode': dest,
                'departureDate': date,
                'adults': adults,
                'travelClass': travel_class,
                'nonStop': non_stop_str,
                'max': max_results,
                'includedAirlineCodes': included_airline_codes
            }

            if return_date:
                params['returnDate'] = return_date
            if children is not None:
                params['children'] = children

            # Perform the API request
            flights = self.client.shopping.flight_offers_search.get(**params).data

            logger.info(f"🛫 Retrieved {len(flights)} flight options.")
            return convert_flight_options_to_sentences(flights)

        except ResponseError as error:
            logger.error(f"❌ Flight search failed: {error}")
            raise


    @timeit
    def search_random_flight(self):
        while True:
            try:
                origin, dest, date, adults = pick_random_airports()
                logger.debug(f"🔍 Random flight: {origin} ➡️ {dest} on {date} [{adults} adult(s)]")
                results = self.client.shopping.flight_offers_search.get(
                    originLocationCode=origin,
                    destinationLocationCode=dest,
                    departureDate=date,
                    adults=adults,
                    includedAirlineCodes='WY'
                ).data
                if results:
                    logger.info(f"✅ Found {len(results)} flight offers.")
                    return results, adults
            except ResponseError as error:
                if error.status_code == 400:
                    logger.warning(f"⚠️ No route from {origin} to {dest}. Retrying...")
                else:
                    logger.error(f"❌ Error: {error}")
                    break

    @timeit
    def confirm_price(self, flight_offer):
        try:
            return self.client.shopping.flight_offers.pricing.post(flight_offer).data
        except ResponseError as error:
            logger.error(f"❌  Price confirmation failed: {error.code} - {error.description()}")
            if 'errors' in error.response.result:
                for e in error.response.result['errors']:
                    logger.error(f"  ⛔ {e.get('code')} - {e.get('detail')}")
            raise

    @timeit
    def book_flight(self, offer, travelers):
        try:
            booking = self.client.booking.flight_orders.post(offer, travelers).data
            logger.info(f"📦 Booking complete. ID: {booking['id']}")
            return booking['id']
        except ResponseError as error:
            logger.error(f"❌ Booking error: {error.code} - {error.description()}")
            if 'errors' in error.response.result:
                for e in error.response.result['errors']:
                    logger.error(f"  ⛔ {e.get('code')} - {e.get('detail')}")
            raise

    @timeit
    def get_booking(self, booking_id):
        try:
            details = self.client.booking.flight_order(booking_id).get().data
            return convert_flight_details_to_sentences(details)
        except ResponseError as error:
            logger.error(f"❌ Booking fetch failed: {error}")
            raise

    @timeit
    def cancel_booking(self, booking_id: str):
        try:
            # Make the API call to cancel the booking
            cancellation_response = self.client.booking.flight_order(booking_id).delete().data
            
            # Check the status code to determine if the cancellation was successful
            if cancellation_response is None:
                logger.info(f"✅ Booking {booking_id} successfully canceled (status 204).")
                return "Booking canceled successfully."
        
        except ResponseError as error:
            logger.error(f"❌ Error Cancel booking failed: {error.response.result}")
            return f"Booking cancellation failed. Details: {error.response.result}"

    @timeit
    def get_flight_status(self, carrier_code, flight_number, scheduled_departure_date):
        try:
            # Construct the flight status request
            flight_details = self.client.schedule.flights.get(
                carrierCode=carrier_code,
                flightNumber=flight_number,
                scheduledDepartureDate=scheduled_departure_date
            ).data

            # Process or return the flight details (you can modify this as per your need)
            # logger.debug(flight_details)
            return convert_flight_status_to_sentences(flight_details)
        except ResponseError as error:
            logger.error(f"❌ Flight schedule fetch failed: {error.response.result}")
            return f"Flight schedule fetch failed: {error.response.result}"
    
    @timeit
    def get_airline_destinations(self, airline_code, arrival_country_code=None, max_results=10):
        try:
            params = {'airlineCode': airline_code, 'max': max_results}
            if arrival_country_code:
                params['arrivalCountryCode'] = arrival_country_code

            # Fetch data from Amadeus API
            destinations = self.client.airline.destinations.get(**params).data
            logger.debug(f"✈️ Destination data: {pformat(destinations)}")

            # Process and return the result
            return convert_airline_destinations_to_sentences(destinations, airline_code)
        except ResponseError as error:
            logger.error(f"❌ Failed to fetch destinations for airline {airline_code}: {error.response.result}")
            return f"Failed to fetch destinations for airline {airline_code}: {error.response.result}"
        except Exception as e:
            logger.error(f"❌ Unexpected error while fetching destinations: {e}")
            raise

    def close(self):
        # Optional teardown method if needed
        pass



def main():
    logger.debug("🚀 Starting Amadeus client...")
    client = AmadeusAPIClient(config)

    # logger.info("🔹 Use Case 1: Flight Search")
    # try:
    #     flights = client.get_flight_search('BOM', 'CDG', '2025-08-10', 1)   # WY202 - BOM to MCT, WY101 - MCT to LHR(London), WY131 - MCT to CDG(Paris)
    #     logger.debug(json.dumps(flights, indent=2))
    # except Exception as e:
    #     logger.error(f"❌ UC1 failed: {e}")

    # logger.info("🔹 Use Case 2: Random Search + Booking")
    # try:
    #     offers, count = client.search_random_flight()
    #     priced_offer = client.confirm_price(offers[0])
    #     travelers = generate_random_travelers_data(count)
    #     booking_id = client.book_flight(offers[0], travelers)
    #     logger.info(f"✅ Booking complete: {booking_id}")
    # except Exception as e:
    #     logger.error(f"❌ UC2 failed: {e}")

    # logger.info("🔹 Use Case 3: Get Booking Details")
    # try:
    #     booking_id = 'eJzTd9cPjfQLMnMCAAvIAmw%3D'
    #     details = client.get_booking(booking_id)
    #     logger.debug(json.dumps(details, indent=2))
    # except Exception as e:
    #     logger.error(f"❌ UC3 failed: {e}")
    
    # logger.info("🔹 Use Case 4: Cancel a Booking")
    # try:
    #     booking_id = 'eJzTd9cPjfQLMnMCAAvIAmw%3D11111'
    #     details = client.cancel_booking(booking_id)
    #     logger.debug(json.dumps(details, indent=2))
    # except Exception as e:
    #     logger.error(f"❌ UC4 failed: {e}")

    # logger.info("🔹 Use Case 5: Get latest flight status or schedule")
    # try:
    #     status = client.get_flight_status('WY', '101', '2025-09-13')
    #     logger.debug(json.dumps(status, indent=2))
    # except Exception as e:
    #     logger.error(f"❌ UC5 failed: {e}")

    # logger.info("🔹 Use Case 6: Get latest flight status or schedule")
    # try:
    #     destinations = client.get_airline_destinations('WY', 'GB', 5)
    #     logger.debug(destinations)
    # except Exception as e:
    #     logger.error(f"❌ UC6 failed: {e}")

    client.close()


if __name__ == "__main__":
    main()

# Booking_id: eJzTd9cPjQz1N4oEAAvqAoM%3D eJzTd9cPjQwN9%2FMAAAwpApY%3D eJzTd9cPjQy1MIoCAAumAm0%3D eJzTd9cPjQyzCDADAAvCAmg%3D eJzTd9cPjQwJCQ8HAAw9Aqo%3D