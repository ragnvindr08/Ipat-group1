from datetime import datetime, timedelta

# Function to compute the time difference
def compute_time_difference(time_in, time_out,
                            break_in, break_out,
                            official_office_in,
                            official_office_out,
                            surplusHour_time_in,
                            surplusHour_time_out,
                            official_honorarium_time_in,
                            official_honorarium_time_out,
                            official_servicecredit_time_in,
                            official_servicecredit_time_out,
                            official_overtimet_time_in,
                            official_overtime_time_out,
                            employment_status,
                            ):
    # Convert strings to datetime objects if they are not empty
    if time_in:
        time_in = datetime.strptime(time_in, "%Y-%m-%d %H:%M:%S").time()
    else:
        time_in = datetime.strptime("00:00", "%H:%M").time()
        
    if time_out:
        time_out = datetime.strptime(time_out, "%Y-%m-%d %H:%M:%S").time()
    else:
        time_out = datetime.strptime("00:00", "%H:%M").time()
        
    if break_in:
        break_in = datetime.strptime(break_in, "%Y-%m-%d %H:%M:%S").time()
    else:
        break_in = datetime.strptime("00:00", "%H:%M").time()
        
    if break_out:
        break_out = datetime.strptime(break_out, "%Y-%m-%d %H:%M:%S").time()
    else:
        break_out = datetime.strptime("00:00", "%H:%M").time()
        
    if surplusHour_time_in:
        surplusHour_time_in = datetime.strptime(surplusHour_time_in, "%Y-%m-%d %H:%M:%S").time()
    else:
        surplusHour_time_in = datetime.strptime("00:00", "%H:%M").time()
        
    if surplusHour_time_out:
        surplusHour_time_out = datetime.strptime(surplusHour_time_out, "%Y-%m-%d %H:%M:%S").time()
    else:
        surplusHour_time_out = datetime.strptime("00:00", "%H:%M").time()

    # Ensure official office times are in datetime format
    official_office_in = datetime.strptime(official_office_in, "%H:%M").time()
    official_office_out = datetime.strptime(official_office_out, "%H:%M").time()
    official_honorarium_time_in = datetime.strptime(official_honorarium_time_in, "%H:%M").time()
    official_honorarium_time_out = datetime.strptime(official_honorarium_time_out, "%H:%M").time()
    official_servicecredit_time_in = datetime.strptime(official_servicecredit_time_in, "%H:%M").time()
    official_servicecredit_time_out = datetime.strptime(official_servicecredit_time_out, "%H:%M").time()
    official_overtimet_time_in = datetime.strptime(official_overtimet_time_in, "%H:%M").time()
    official_overtime_time_out = datetime.strptime(official_overtime_time_out, "%H:%M").time()
    
    if employment_status == "JO":
        official_office_in_datetime = datetime.combine(datetime.today(), official_office_in)
        # Calculate the end of break time
        break_starts = official_office_in_datetime + timedelta(hours=4)
        break_end = break_starts + timedelta(hours=1)

        # Check if time_in is before official_office_in
        if time_in < official_office_in:
            time_in = official_office_in

        # Check if break_in is after break_starts
        if break_in  >= break_starts.time():
            break_in = break_starts.time()

        # Check if break_out is before break_end
        if break_out  < break_end.time():
            break_out = break_end.time()

        # Check if time_out is after official_office_out
        if time_out  > official_office_out:
            time_out = official_office_out

        # Calculate the difference
        if break_in:
            difference_morning = datetime.combine(datetime.today(), break_in) - datetime.combine(datetime.today(), time_in)
            print(difference_morning)
        else:
            difference_morning = timedelta(0)
        if break_in:
            difference_afternoon = datetime.combine(datetime.today(), time_out) - datetime.combine(datetime.today(), break_out)
        else:
            difference_afternoon = timedelta(0)
            
        
        # Extract hours and minutes from the timedelta
        if difference_morning == timedelta(0):
            difference_hours_morning = 0
            difference_minutes_morning = 0
            
        else:
            difference_hours_morning = difference_morning.total_seconds() // 3600
            difference_minutes_morning = (difference_morning.total_seconds() % 3600) // 60
        if difference_afternoon == timedelta(0): 
            difference_hours_afternoon = 0
            difference_minutes_afternoon = 0
        else:
            difference_hours_afternoon = difference_afternoon.total_seconds() // 3600
            difference_minutes_afternoon = (difference_afternoon.total_seconds() % 3600) // 60
            
        
        if difference_hours_morning >= 4:
            difference_minutes_morning = 0
        if difference_hours_afternoon >= 4:
            difference_minutes_afternoon = 0

        total_hours = difference_hours_morning + difference_hours_afternoon + (difference_minutes_morning + difference_minutes_afternoon) // 60
        total_minutes = (difference_minutes_morning + difference_minutes_afternoon) % 60
        
        return difference_hours_morning, difference_hours_afternoon, difference_minutes_morning, difference_minutes_afternoon, total_hours, total_minutes
       
    else:
        if (time_out == "00:00" and time_in == "00:00") or (time_out == "00:00" and time_in != "00:00")or (time_out != "00:00" and time_in == "00:00"):
        # if (time_out == "00:00" and time_in != "00:00"):
            time_out = "00:00"
            time_in = "00:00"
        #     print(time_out)
        #     print(time_in)
        # elif (time_out != "00:00" and time_in == "00:00"):
        #     time_out = "00:00"
        #     time_in = "00:00"
        #     print(time_out)
        #     print(time_in)
        # elif (time_out == "00:00" and time_in == "00:00"):
        #     time_out = "00:00"
        #     time_in = "00:00" 
        #     print(time_out)
        #     print(time_in)
           
           
           
            # difference_regular = datetime.combine(datetime.today(), time_out) - datetime.combine(datetime.today(), time_in)
            # difference_hours_regular = difference_regular.total_seconds() // 3600
            # difference_minutes_regular = (difference_regular.total_seconds() % 3600) // 60
            
            print(time_out)
            print(time_in)
            difference_regular = 0
            difference_hours_regular = 0
            difference_minutes_regular = 0
            
            return difference_hours_regular, difference_minutes_regular
        else:
            print(time_out)
            print(time_in)
            difference_regular = datetime.combine(datetime.today(), time_out) - datetime.combine(datetime.today(), time_in)
            difference_hours_regular = difference_regular.total_seconds() // 3600
            difference_minutes_regular = (difference_regular.total_seconds() % 3600) // 60

            return difference_hours_regular, difference_minutes_regular
    
# Input times
time_in = ""
break_in = "2024-03-01 12:20:00"
break_out = "2024-03-01 13:20:00"
time_out = "2024-03-01 17:00:00"
surplusHour_time_in = "2024-03-01 17:30:00"
surplusHour_time_out = "2024-03-01 21:00:00"
official_office_in = "8:00"
official_office_out = "17:00"
official_honorarium_time_in = "18:00"
official_honorarium_time_out = "21:00"
official_servicecredit_time_in = "00:00"
official_servicecredit_time_out = "00:00"
official_overtimet_time_in = "00:00"
official_overtime_time_out = "00:00"
employment_status = "FACULTY"

# Compute the time difference
if employment_status == "JO":
    difference_hours_morning, difference_hours_afternoon, difference_minutes_morning, difference_minutes_afternoon, total_hours, total_minutes = compute_time_difference(time_in, time_out,
                            break_in, break_out,
                            official_office_in,
                            official_office_out,
                            surplusHour_time_in,
                            surplusHour_time_out,
                            official_honorarium_time_in,
                            official_honorarium_time_out,
                            official_servicecredit_time_in,
                            official_servicecredit_time_out,
                            official_overtimet_time_in,
                            official_overtime_time_out,
                            employment_status,)
    
    # Print the difference for JO
    print("Morning Difference:", difference_hours_morning, "hours and", difference_minutes_morning, "minutes while the Afternoon Difference: ", difference_hours_afternoon,  "Hours and", difference_minutes_afternoon, "minutes")
    print("Total time worked: {} hours and {} minutes".format(total_hours, total_minutes))
else:
    difference_hours_regular, difference_minutes_regular = compute_time_difference(time_in, time_out,
                            break_in, break_out,
                            official_office_in,
                            official_office_out,
                            surplusHour_time_in,
                            surplusHour_time_out,
                            official_honorarium_time_in,
                            official_honorarium_time_out,
                            official_servicecredit_time_in,
                            official_servicecredit_time_out,
                            official_overtimet_time_in,
                            official_overtime_time_out,
                            employment_status,)
    # Print the difference for non-JO
    print("The Total time worked: {} hours and {} minutes".format(difference_hours_regular, difference_minutes_regular))
