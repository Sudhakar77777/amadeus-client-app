import urllib.parse
import base64
import zlib

booking_ids = [
    "eJzTd9cPiwrx8bEEAAv8Ans%3D",
    "eJzTd9cPiwp1drMAAAvYAmw%3D",
    "eJzTd9cPiwpxdgsFAAvxAog%3D",
    "eJzTd9cPiwqJCAgGAAxCAqU%3D",
    "eJzTd9cPiwrx9zIDAAv%2BAnk%3D",
    "eJzTd9cPiwr1cjcBAAvrAnA%3D",
    "eJzTd9cPiwrx9YkAAAweAps%3D",
    "eJzTd9cPiwrxMnICAAvLAmg%3D",
    "eJzTd9cPiwr1NDIBAAu%2BAlo%3D",
    "eJzTd9cPiwoJDw8GAAxNAqs%3D",
    "eJzTd9cPiwqJ8o0CAAxJAqs%3D",
    "eJzTd9cPiwp19g8FAAwHApI%3D",
    "eJzTd9cPiwo18wwCAAvRAnw%3D",
    "eJzTd9cPiwoJM%2FUCAAv9An8%3D",
    "eJzTd9cPiwoxCXIEAAvIAnE%3D",
    "eJzTd9cPiwoJDg4AAAw2AqA%3D",
    "eJzTd9cPiwrx9wkBAAwgApk%3D",
    "eJzTd9cPiwo1czICAAujAlU%3D",
    "eJzTd9cPiwqJ8vcFAAxAAqA%3D",
    "eJzTd9cPiwo1izQCAAvRAmw%3D",
    "eJzTd9cPiwox9g8BAAvSAoA%3D",
    "eJzTd9cPiwrxcPMGAAv2AoM%3D",
    "eJzTd9cPiwoJMg0DAAv9Aoc%3D",
    "eJzTd9cPiwoJ9%2FMDAAw2Ap0%3D",
    "eJzTd9cPiwrxinIGAAwcApE%3D",
]

def decode_booking_id(encoded_id):
    try:
        # Step 1: URL decode
        url_decoded = urllib.parse.unquote(encoded_id)

        # Step 2: Base64 decode
        raw_bytes = base64.b64decode(url_decoded)

        # Step 3: Attempt zlib decompression
        try:
            decompressed = zlib.decompress(raw_bytes)
            return decompressed.decode("utf-8")
        except zlib.error:
            # Not compressed, try as plain base64
            return raw_bytes.decode("utf-8")
    except Exception as e:
        return f"❌ Error decoding: {e}"

# Process and print all booking IDs
print("🔎 Decoded Booking IDs:")
for i, bid in enumerate(booking_ids, start=1):
    decoded = decode_booking_id(bid)
    print(f"{i:02d}: {decoded}")
