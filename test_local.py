from httpx import post

chat_id = "999111999366"

url = "http://localhost:8000/chat_completions"
# url = "https://cxml.cxsphere.com/chat_completions"

headers = {
    "Authorization": "eyJpZCI6MjF9.ZV9phw.ciF-TuKteRu4K-CPRgj2fACZ0l8",
    "Origin": "https://app.cxsphere.com"
}

def reset_chat_history():
    
    clear = post(f"{url}/clear", headers=headers, json={"chat_id": chat_id})


flight_search_test = post(f"{url}", headers=headers, data={
        "chat_id": chat_id,
        "prompt_key": "sutherland",
        "message": f"""Hey! Find me a flight from Chennai to Paris on 2025-11-22 for 1 adult(s).""",  
        # "message": f"""Find me a flight from Amsterdam to Muscat on Aug 19th.""",  
        # "message": f"""Find me flight from Doha to Riyadh on 27th September for 1 adult.""",
        # "message": f"""Find my booking details, pnr number is eJzTd9cPDTENCPUDAAuPAnc%3D.""",
        # "message": f"""Get me the flight status for Oman air WY 101 departing on 2025-05-14.""",
        # "message": f"""Get me the flight status for my pnr number eJzTd9cPC3AK8gsGAAuyAoE%3D.""",
        # "message": f"""Show me all Oman air destinations to GB.""",
        # "message": f"""Show me airport code for Mumbai in India.""",
        # "message": f"""Show me airline record for Oman Air.""",
        # "selected_tools": "amadeus_booking_details",
        "selected_tools": ["amadeus_flight_offers", "amadeus_booking_details", "amadeus_cancel_booking", 
                           "amadeus_flight_status", "amadeus_airline_destinations" ],  # "airport_lookup", "airline_lookup"
        # "selected_tools": "amadeus_flight_status_by_pnr",
        # "do_rag": True,
    }, timeout=300)


print(f'response: {flight_search_test}')
response = flight_search_test.json()["completion"]
print(response)