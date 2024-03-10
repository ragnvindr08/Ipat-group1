from datetime import datetime, timedelta

# Function to compute the time difference
def compute_time_difference(time_in, time_out, break_in, break_out, official_office_in, official_office_out):
    # Convert time1_str to datetime object


    time_in = datetime.strptime(time_in, "%Y-%m-%d %H:%M:%S")
    time_out = datetime.strptime(time_out, "%Y-%m-%d %H:%M:%S")
    break_in = datetime.strptime(break_in, "%Y-%m-%d %H:%M:%S")
    break_out = datetime.strptime(break_out, "%Y-%m-%d %H:%M:%S")
    official_office_in = datetime.strptime(official_office_in, "%H:%M")
    official_office_out = datetime.strptime(official_office_out, "%H:%M")




    time1 = datetime.strptime(time1_str, "%H:%M")

    # Check if time1 is before 1:00 PM
    if time1.time() < datetime.strptime("13:00", "%H:%M").time():
        time1 = datetime.strptime("13:00", "%H:%M")

    # Parse the times and create datetime objects
    time1 = datetime.strptime(time1_str, "%H:%M")
    time2 = datetime.strptime(time2_str, "%H:%M")

    # Calculate the difference
    difference = time2 - time1

    # Extract hours and minutes from the timedelta
    difference_hours = difference // timedelta(hours=1)

    # Return the difference in hours
    return difference_hours

# Input times
time_in = "2024-03-01 08:15:00"
time_out = "2024-03-01 17:00:00"
break_in = "2024-03-01 12:20:00"
break_out = "2024-03-01 13:20:00"
official_office_in = "8:00"
official_office_out = "17:00"
time1_str = "12:45"
time2_str = "17:00"


# Compute the time difference
difference_hours = compute_time_difference(time1_str, time2_str)

# Print the difference
print("Difference:", difference_hours, "hours")
