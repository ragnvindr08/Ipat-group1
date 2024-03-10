from datetime import datetime, timedelta

# Function to calculate total rendered hours
def calculate_rendered_hours(time_in, time_out, break_in, break_out, official_office_in, official_office_out):
    # Convert strings to datetime objects
    time_in = datetime.strptime(time_in, "%Y-%m-%d %H:%M:%S").time()
    time_out = datetime.strptime(time_out, "%Y-%m-%d %H:%M:%S").time()
    break_in = datetime.strptime(break_in, "%Y-%m-%d %H:%M:%S").time()
    break_out = datetime.strptime(break_out, "%Y-%m-%d %H:%M:%S").time()
    official_office_in = datetime.strptime(official_office_in, "%H:%M").time()
    official_office_out = datetime.strptime(official_office_out, "%H:%M").time()
    
    # Calculate the end of break time
    break_starts = official_office_in + timedelta(hours=4)
    break_end = break_starts + timedelta(hours=1)
    return break_end

# Input data
time_in = "2024-03-01 08:15:00"
time_out = "2024-03-01 17:00:00"
break_in = "2024-03-01 12:20:00"
break_out = "2024-03-01 13:20:00"
official_office_in = "8:00"
official_office_out = "17:00"

# Compute end of break time
break_end = calculate_rendered_hours(time_in, time_out, break_in, break_out, official_office_in, official_office_out)
print("End of break time:", break_end.strftime("%Y-%m-%d %H:%M:%S"))
