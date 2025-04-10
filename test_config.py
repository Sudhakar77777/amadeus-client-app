from config import Settings

try:
    config = Settings()
    print(config.dict())  # Should display all loaded variables
except Exception as e:
    print(f"Error: {e}")
