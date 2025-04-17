import json
import time
from functools import wraps
from datetime import datetime
from amadeus import Client, ResponseError
from base_logger import logger
from base_config import config
from client_api_data_format import convert_flight_details_to_sentences, convert_flight_options_to_sentences
from utils import pick_random_airports, generate_random_travelers_data


def timeit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.debug(f"➡️ {func.__name__} started...")
        start = time.time()
        try:
            return func(*args, **kwargs)
        finally:
            logger.debug(f"⏱️ {func.__name__} finished in {time.time() - start:.2f}s")
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

    @timeit
    def get_flight_search(self, origin, dest, date, adults):
        try:
            flights = self.client.shopping.flight_offers_search.get(
                originLocationCode=origin,
                destinationLocationCode=dest,
                departureDate=date,
                adults=adults
            ).data
            logger.info(f"🛫 Retrieved {len(flights)} flight options.")
            return convert_flight_options_to_sentences(flights[0:3])
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
                    adults=adults
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
            logger.error(f"❌ Price confirmation failed: {error}")
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

    def close(self):
        # Optional teardown method if needed
        pass



def main():
    logger.debug("🚀 Starting Amadeus client...")
    client = AmadeusAPIClient(config)

    # logger.info("🔹 Use Case 1: Direct Flight Search")
    # try:
    #     flights = client.get_flight_search('JFK', 'LHR', '2025-09-01', 1)
    #     logger.debug(json.dumps(flights, indent=2))
    # except Exception as e:
    #     logger.error(f"❌ UC1 failed: {e}")

    logger.info("🔹 Use Case 2: Random Search + Booking")
    try:
        offers, count = client.search_random_flight()
        priced_offer = client.confirm_price(offers[0])
        travelers = generate_random_travelers_data(count)
        booking_id = client.book_flight(offers[0], travelers)
        logger.info(f"✅ Booking complete: {booking_id}")
        # details = client.get_booking(booking_id)
        # logger.debug(json.dumps(details, indent=2))
    except Exception as e:
        logger.error(f"❌ UC2 failed: {e}")

    client.close()


if __name__ == "__main__":
    main()
