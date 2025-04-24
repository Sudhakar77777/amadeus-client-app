import re

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
    "eJzTd9cPNzUODjMBAArpAkI%3D",
    "eJzTd9cPNzXxc3YHAArLAj4%3D",
    "eJzTd9cPNzUJcQoBAAroAlA%3D",
    "eJzTd9cPNzUOcDQFAAq3Ais%3D",
    "eJzTd9cPNzVxi4oEAArzAl8%3D",
    "eJzTd9cPNzXxN%2FEBAAq1AjU%3D",
    "eJzTd9cPNzWxdAkFAAqcAjg%3D",
    "eJzTd9cPNzVxNYkAAAqjAjc%3D",
    "eJzTd9cPNzXxNncGAAqmAis%3D",
]

# pattern = re.compile(r"^eJzTd9cP(?:[a-zA-Z0-9]|%[0-9A-Fa-f]{2})+$")
pattern = re.compile(r"^eJz[A-Za-z0-9%]+(%3D){0,2}$")

valid = [bid for bid in booking_ids if pattern.match(bid)]

print(f"✅ Valid Booking IDs: {len(valid)} / {len(booking_ids)}")

invalid = [bid for bid in booking_ids if not pattern.match(bid)]

print("❌ Invalid Booking IDs:")
for bid in invalid:
    print("-", bid)
