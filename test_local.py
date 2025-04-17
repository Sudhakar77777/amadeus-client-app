from httpx import post

chat_id = "999111999222"

# url = "http://localhost:8000/chat_completions"
url = "https://cxml.cxsphere.com/chat_completions"

headers = {
    "Authorization": "eyJpZCI6MjF9.ZV9phw.ciF-TuKteRu4K-CPRgj2fACZ0l8",
    "Origin": "https://app.cxsphere.com"
}

def reset_chat_history():
    
    clear = post(f"{url}/clear", headers=headers, json={"chat_id": chat_id})


flight_search_test = post(f"{url}", headers=headers, data={
        "chat_id": chat_id,
        "prompt_key": "sutherland",
        # "message": f"""Hey! Find me a flight from FRA to SFO on 2025-09-14 for 2 adult(s).""",  
        "message": f"""Find me flight from Doha to Riyadh on 27th September for 1 adult.""",
        # "message": f"""Find my booking details, pnr number is eJzTd9cPDTENCPUDAAuPAnc%3D.""",
        "selected_tools": ["amadeus_flight_search", "amadeus_flight_details"],
        # "selected_tools": "amadeus_flight_details",
        # "do_rag": True,
    }, timeout=300)


print(f'response: {flight_search_test}')
response = flight_search_test.json()["completion"]
print(response)