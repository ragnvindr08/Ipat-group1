from datetime import datetime, time, timedelta

# Define the times
time_in_time = time(12, 16, 0)
break_in_time = time(12, 0, 0)
official_time = time(8, 0, 0)

# Calculate the late time relative to the official start time
actual_time_in = datetime.combine(datetime.today(), time_in_time)
official_time_in = datetime.combine(datetime.today(), official_time)
late_time = actual_time_in - official_time_in
print(late_time)
# Subtract the break time from the late time if applicable
if actual_time_in.time() >= break_in_time:
    print(late_time)
    late_time -= timedelta(hours=break_in_time.hour, minutes=break_in_time.minute, seconds=break_in_time.second)

# Ensure late_time is not negative
if late_time.total_seconds() < 0:
    late_time = timedelta(0)

# Print the total late time
print("Total late time:", late_time)
