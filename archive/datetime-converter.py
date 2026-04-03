from datetime import datetime, timedelta, timezone
import zoneinfo



date_time = '2024-11-13T16:50:00+00:00'

new_date = date_time[0:16]

d1 = datetime.strptime(new_date, "%Y-%m-%dT%H:%M") - timedelta(hours=5, minutes=0)


print(d1)
