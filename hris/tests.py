from datetime import datetime, timedelta

# Function to compute the time difference
def compute_time_difference(time1_str, time2_str):
    
    
    # Convert time1_str to datetime object
    


    time1 = datetime.strptime(time1_str, "%H:%M")
    time2 = datetime.strptime(time2_str, "%H:%M")
    # Check if time1 is before 1:00 PM
    if time1.time() < datetime.strptime("13:00", "%H:%M").time():
        time1 = datetime.strptime("13:00", "%H:%M")

    if time2.time() >= datetime.strptime("17:00", "%H:%M").time():
        time2 = datetime.strptime("17:00", "%H:%M")

    # Calculate the difference
    difference = time2 - time1

    # Extract hours and minutes from the timedelta
    difference_hours = difference // timedelta(hours=1)

    difference_minutes = (difference % timedelta(hours=1)).seconds // 60

    # Return the difference in hours and minutes
    return difference_hours, difference_minutes

# Input times
time1_str = "2024-03-01 08:15:00"
time2_str = "2024-03-01 17:00:00"

# Compute the time difference
difference_hours, difference_minutes = compute_time_difference(time1_str, time2_str)

# Print the difference
print("Difference:", difference_hours, "hours and", difference_minutes, "minutes")
