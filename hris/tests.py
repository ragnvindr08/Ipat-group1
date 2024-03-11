from datetime import datetime

# Function to rearrange times in ascending order
def rearrange_times(time_in, break_in, break_out, time_out):
    # Create a list of times
    times = [time_in, break_in, break_out, time_out]
    # Sort the times
    times.sort()
    # Assign the sorted times back to the respective variables
    time_in, break_in, break_out, time_out = times
    return time_in, break_in, break_out, time_out

# Original times
time_in =  "17:00:00"
break_in = "13:20:00" 
break_out = "12:20:00"
time_out = "08:15:00"

# Rearrange times
time_in, break_in, break_out, time_out = rearrange_times(time_in, break_in, break_out, time_out)

# Print the rearranged times
print("Rearranged times:")
print("Time in:", time_in)
print("Break in:", break_in)
print("Break out:", break_out)
print("Time out:", time_out)
