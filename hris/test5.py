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
 



    # Convert strings to datetime objects
    time_in = datetime.strptime(time_in, "%Y-%m-%d %H:%M:%S").time()
    time_out = datetime.strptime(time_out, "%Y-%m-%d %H:%M:%S").time()
    break_in = datetime.strptime(break_in, "%Y-%m-%d %H:%M:%S").time()
    break_out = datetime.strptime(break_out, "%Y-%m-%d %H:%M:%S").time()
    surplusHour_time_in= datetime.strptime(surplusHour_time_in, "%Y-%m-%d %H:%M:%S").time()
    surplusHour_time_out= datetime.strptime(surplusHour_time_out, "%Y-%m-%d %H:%M:%S").time()
    # Ensure official office times are in datetime format
    
    official_office_in = datetime.strptime(official_office_in, "%H:%M").time()
    official_office_out = datetime.strptime(official_office_out, "%H:%M").time()
    official_honorarium_time_in = datetime.strptime(official_honorarium_time_in, "%H:%M").time()
    official_honorarium_time_out = datetime.strptime(official_honorarium_time_out, "%H:%M").time()
    official_servicecredit_time_in = datetime.strptime(official_servicecredit_time_in, "%H:%M").time()
    official_servicecredit_time_out = datetime.strptime(official_servicecredit_time_out, "%H:%M").time()
    official_overtimet_time_in = datetime.strptime(official_overtimet_time_in, "%H:%M").time()
    official_overtime_time_out = datetime.strptime(official_overtime_time_out, "%H:%M").time()
    # Convert official_office_in to a datetime object for addition with timedelta
    
    

    
    if employment_status == "JO":
        official_office_in_datetime = datetime.combine(datetime.today(), official_office_in)
        # Calculate the end of break time
        break_starts = official_office_in_datetime + timedelta(hours=4)
        # print(break_starts)
        break_end = break_starts + timedelta(hours=1)

        # Check if time_in is before official_office_in
        if time_in < official_office_in:
            time_in = official_office_in

        # Check if break_in is after break_starts
        if break_in >= break_starts.time():
            break_in = break_starts.time()

        # Check if break_out is before break_end
        if break_out < break_end.time():
            break_out = break_end.time()

        # Check if time_out is after official_office_out
        if time_out > official_office_out:
            time_out = official_office_out

        # Calculate the difference
        difference_morning = datetime.combine(datetime.today(), break_in) - datetime.combine(datetime.today(), time_in)
        difference_afternoon = datetime.combine(datetime.today(), time_out) - datetime.combine(datetime.today(), break_out)
        # Extract hours and minutes from the timedelta
        difference_hours_morning = difference_morning.total_seconds() // 3600
        difference_hours_afternoon = difference_afternoon.total_seconds() // 3600
        difference_minutes_morning  = (difference_morning.total_seconds() % 3600) // 60
        difference_minutes_afternoon = (difference_afternoon.total_seconds() % 3600) // 60
        if difference_hours_morning >= 4:
            difference_minutes_morning = 0
        if difference_hours_afternoon >= 4:
            difference_minutes_afternoon = 0

        total_hours = difference_hours_morning + difference_hours_afternoon + (difference_minutes_morning + difference_minutes_afternoon) // 60
        total_minutes = (difference_minutes_morning + difference_minutes_afternoon) % 60
        return difference_hours_morning, difference_hours_afternoon, difference_minutes_morning, difference_minutes_afternoon, total_hours, total_minutes
       
    else:
        difference_regular = datetime.combine(datetime.today(), time_out) - datetime.combine(datetime.today(), time_in)
        print(difference_regular)
        difference_hours_regular = difference_regular.total_seconds() // 3600
        difference_minutes_regular  = (difference_regular.total_seconds() % 3600) // 60

        return difference_hours_regular, difference_minutes_regular
    
    # Return the difference in hours and minutes
   

# Input times
time_in = "2024-03-01 08:15:00"
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
employment_status = "JO"
# Compute the time difference
difference_minutes_regular, difference_hours_regular, difference_hours_morning, difference_hours_afternoon, difference_minutes_morning, difference_minutes_afternoon, total_hours, total_minutes = compute_time_difference(time_in, time_out,
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

# Print the difference
print("Morning Difference:", difference_hours_morning, "hours and", difference_minutes_morning, "minutes while the Afternoon Difference: ", difference_hours_afternoon,  "and", difference_minutes_afternoon, "minutes")
print("Total time worked: {} hours and {} minutes".format(total_hours, total_minutes))
print("Total time worked: {} hours and {} minutes".format(difference_hours_regular, difference_minutes_regular))