from httpx import post

chat_id = "999111999112"

url = "http://localhost:8000/chat_completions"
headers = {
    "Authorization": "eyJpZCI6MjF9.ZV9phw.ciF-TuKteRu4K-CPRgj2fACZ0l8",
    "Origin": "https://app.cxsphere.com"
}

clear = post(f"{url}/clear", headers=headers, json={"chat_id": chat_id})


flight_search_test = post(f"{url}", headers=headers, data={
        "chat_id": chat_id,
        "prompt_key": "",
        "message": f"""Hey! Find me a flight from FRA to SFO on 2025-06-14 for 2 adult(s).""",  
        # "message": f"""Find my booking details, pnr number is eJzTd9f3dvaOcPQGAAtDAmM%3D.""",
        # "message": f"""Find my booking details, pnr number is eJzTd9f3dg529HUHAAsyAlw%3D.""",
        "selected_tools": ["amadeus_flight_search"],
        # "selected_tools": ["amadeus_flight_details"],
        # "do_rag": True,
    }, timeout=300)

response = flight_search_test.json()["completion"]
print(response)