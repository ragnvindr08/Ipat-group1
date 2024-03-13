from datetime import datetime

# Time data
time_in = "8:17 am"
break_in = "8:51 pm"
break_out = ""
time_out = ""
overtime_in = ""
overtime_out = ""

# Function to convert time to 24-hour format
def convert_to_24hr(time_str):
    if time_str:
        return datetime.strptime(time_str, "%I:%M %p").strftime("%H:%M")
    else:
        return "00:00"

# Convert time strings to 24-hour format
time_in = convert_to_24hr(time_in)
break_in = convert_to_24hr(break_in)
break_out = convert_to_24hr(break_out)
time_out = convert_to_24hr(time_out)
overtime_in = convert_to_24hr(overtime_in)
overtime_out = convert_to_24hr(overtime_out)

# Sort time data
time_entries = [
    ("time_in", time_in),
    ("break_in", break_in),
    ("break_out", break_out),
    ("time_out", time_out),
    ("overtime_in", overtime_in),
    ("overtime_out", overtime_out)
]

sorted_entries = sorted(time_entries, key=lambda x: x[1])

# Print sorted data in the desired format
print(f"{sorted_entries[0][0].ljust(12)}= {sorted_entries[0][1]}")
print(f"{sorted_entries[1][0].ljust(12)}= {sorted_entries[1][1]}")
print(f"{sorted_entries[2][0].ljust(12)}= {sorted_entries[2][1]}")
print(f"{sorted_entries[3][0].ljust(12)}= {sorted_entries[3][1]}")
print(f"{sorted_entries[4][0].ljust(12)}= {sorted_entries[4][1]}")
print(f"{sorted_entries[5][0].ljust(12)}= {sorted_entries[5][1]}")
