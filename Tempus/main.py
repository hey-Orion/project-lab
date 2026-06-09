import time
from datetime import datetime

def to_30_hour_clock_ampm(dt):
    total_minutes = dt.hour * 60 + dt.minute + dt.second / 60

    # Convert to 30-hour system
    new_hour = int(total_minutes // 48)
    remaining_minutes = total_minutes % 48

    new_minute = int((remaining_minutes / 48) * 60)
    new_second = int((((remaining_minutes / 48) * 60) - new_minute) * 60)

    # AM / PM logic
    if new_hour < 15:
        period = "AM"
        display_hour = 12 if new_hour == 0 else new_hour
    else:
        period = "PM"
        display_hour = 12 if new_hour == 15 else new_hour - 15

    return f"{display_hour:02d}:{new_minute:02d}:{new_second:02d} {period}"

try:
    while True:
        now = datetime.now()
        clock_30 = to_30_hour_clock_ampm(now)

        print(f"\rproto Clock → {clock_30}", end="")
        time.sleep(1)

except KeyboardInterrupt:
    print("\nClock stopped.")