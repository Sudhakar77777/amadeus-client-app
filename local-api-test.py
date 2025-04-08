import httpx
import time
from functools import wraps

# Config
chat_id = "999111999222"
urls = {
    "test": "http://localhost:8000/chat_completions",
    "prod": "https://cxml.cxsphere.com/chat_completions"
}
headers = {
    "Authorization": "eyJpZCI6MjF9.ZV9phw.ciF-TuKteRu4K-CPRgj2fACZ0l8",
    "Origin": "https://app.cxsphere.com"
}
messages = {
    "flight_search": "Hey! Find me a flight from FRA to SFO on 2025-06-14 for 2 adult(s).",
    "booking_details": "Find my booking details, pnr number is eJzTd9cPcffyNfMBAAtTAlo%3D."
}

# Timeit decorator
def timeit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"➡️ {func.__name__} started...")
        start = time.time()
        try:
            return func(*args, **kwargs)
        finally:
            print(f"⏱️ {func.__name__} finished in {time.time() - start:.2f}s")
    return wrapper

class SimpleAPIClient:
    def __init__(self, base_url: str, headers: dict):
        self.base_url = base_url
        self.headers = headers
        self.client = httpx.Client(timeout=300)

    @timeit
    def reset_chat_history(self, chat_id: str):
        try:
            url = f"{self.base_url}/clear"
            print(f"🔄 Resetting chat history for chat_id={chat_id}")
            res = self.client.post(url, headers=self.headers, json={"chat_id": chat_id})
            res.raise_for_status()
            print(f"✅ Chat history cleared.")
        except Exception as e:
            print(f"❌ Error resetting chat: {e}")

    @timeit
    def send_chat(self, chat_id: str, message: str, selected_tools: list):
        try:
            print(f"✉️ Sending message: {message}")
            payload = {
                "chat_id": chat_id,
                "prompt_key": "",
                "message": message,
                "selected_tools": selected_tools,
                # "do_rag": True,  # Optional
            }
            res = self.client.post(self.base_url, headers=self.headers, data=payload, timeout=180)
            res.raise_for_status()
            print(f"✅ Message sent. Status: {res.status_code}")
            json_data = res.json()
            print(f"🧠 Completion:\n{json_data.get('completion', '[no completion]')}")
        except Exception as e:
            print(f"❌ Chat error: {e}")

    def close(self):
        self.client.close()

# 👇 Usage
if __name__ == "__main__":
    client = SimpleAPIClient(base_url=urls.get('test'), headers=headers)
    
    client.reset_chat_history(chat_id)

    client.send_chat(
        chat_id=chat_id,
        message=messages.get("flight_search"),
        # message=messages.get("booking_details"),
        selected_tools=["amadeus_flight_search", "amadeus_flight_details"]
    )

    client.close()
