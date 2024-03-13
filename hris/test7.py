from datetime import datetime, timedelta, time

# Function to compute the time difference
def compute_time_difference(time_in, time_out,
                            break_in, break_out,
                            official_office_in,
                            official_office_out,
                            official_honorarium_time_in,
                            official_honorarium_time_out,
                            official_servicecredit_time_in,
                            official_servicecredit_time_out,
                            official_overtime_time_in,
                            official_overtime_time_out,
                            employment_status,
                            ):
    #DEFAULT TIME
    timeref = datetime.strptime("00:00", "%H:%M").time()
    
    # Convert strings to datetime objects if they are not empty
    if time_in:
        time_in = datetime.strptime(time_in, "%Y-%m-%d %H:%M:%S").time()
    else:
        time_in = datetime.strptime("00:00", "%H:%M").time()
        
        
    if time_out:
        time_out = datetime.strptime(time_out, "%Y-%m-%d %H:%M:%S").time()
    else:
        time_out = datetime.strptime("00:00", "%H:%M").time()
        
        #----------------HONO----SC-------OT----------------------------------------------------------------
   
    if time_in > timeref:
        time_in_hn = time_in
    else:
        time_in_hn = datetime.strptime("00:00", "%H:%M").time()
       
        
    if time_out > timeref:
        time_out_hn = time_out
    else:
        time_out_hn = datetime.strptime("00:00", "%H:%M").time()   
        
        
        #----------------HONO----SC-------OT-----------------END--------------------------------------------
        #----------------HONO----SC-------OT----------------------------------------------------------------
   
    if time_in  > timeref:
        time_in_sc = time_in
    else:
        time_in_sc = datetime.strptime("00:00", "%H:%M").time()
       
        
    if time_out:
        time_out_sc = time_out
    else:
        time_out_sc = datetime.strptime("00:00", "%H:%M").time()   
        
        
        #----------------HONO----SC-------OT-----------------END--------------------------------------------
        #----------------HONO----SC-------OT----------------------------------------------------------------
   
    if time_in  > timeref:
        time_in_ot = time_in
    else:
        time_in_ot = datetime.strptime("00:00", "%H:%M").time()
           
    if time_out > time_out:
        time_out_ot = time_out
    else:
        time_out_ot = datetime.strptime("00:00", "%H:%M").time()   
        
        
        #----------------HONO----SC-------OT-----------------END--------------------------------------------     
        
        
    if break_in:
        break_in = datetime.strptime(break_in, "%Y-%m-%d %H:%M:%S").time()
    else:
        break_in = datetime.strptime("00:00", "%H:%M").time()
        
    if break_out:
        break_out = datetime.strptime(break_out, "%Y-%m-%d %H:%M:%S").time()
    else:
        break_out = datetime.strptime("00:00", "%H:%M").time()
        
    # if surplusHour_time_in:
    #     surplusHour_time_in = datetime.strptime(surplusHour_time_in, "%Y-%m-%d %H:%M:%S").time()
    # else:
    #     surplusHour_time_in = datetime.strptime("00:00", "%H:%M").time()
        
    # if surplusHour_time_out:
    #     surplusHour_time_out = datetime.strptime(surplusHour_time_out, "%Y-%m-%d %H:%M:%S").time()
    # else:
    #     surplusHour_time_out = datetime.strptime("00:00", "%H:%M").time()

    # Ensure official office times are in datetime format
    official_office_in = datetime.strptime(official_office_in, "%H:%M").time()
    official_office_out = datetime.strptime(official_office_out, "%H:%M").time()
    official_honorarium_time_in = datetime.strptime(official_honorarium_time_in, "%H:%M").time()
    official_honorarium_time_out = datetime.strptime(official_honorarium_time_out, "%H:%M").time()
    official_servicecredit_time_in = datetime.strptime(official_servicecredit_time_in, "%H:%M").time()
    official_servicecredit_time_out = datetime.strptime(official_servicecredit_time_out, "%H:%M").time()
    official_overtime_time_in = datetime.strptime(official_overtime_time_in, "%H:%M").time()
    official_overtime_time_out = datetime.strptime(official_overtime_time_out, "%H:%M").time()
    timeref = datetime.strptime("00:00", "%H:%M").time()
    
    
    if employment_status == "JO":
        official_office_in_datetime = datetime.combine(datetime.today(), official_office_in)
        # Calculate the end of break time
        break_starts = official_office_in_datetime + timedelta(hours=4)
        break_end = break_starts + timedelta(hours=1)

        # Check if time_in is before official_office_in
        if time_in < official_office_in and time_in != timeref:
            time_in = official_office_in

        # Check if break_in is after break_starts
        if break_in  >= break_starts.time():
            break_in = break_starts.time()

        # Check if break_out is before break_end
        if break_out  < break_end.time():
            break_out = break_end.time()

        # Check if time_out is after official_office_out
        if time_out  > official_office_out and time_out != timeref:
            time_out_office = official_office_out
            
       #--------HONORARIUM-------------------------------------------------------------------
       # Check if time_in is before official_office_in
        if time_in_hn != timeref:
            time_in_hn = official_honorarium_time_in

        # Check if time_out is after official_office_out
        if time_out_hn  > official_honorarium_time_out and time_out_hn != timeref:
            time_out_hn = official_honorarium_time_out          
        #------------------------------------------------------------------------------------    
        
        
        #--------SERVICE CREDIT-------------------------------------------------------------------
       # Check if time_in is before official_office_in
        if time_in != timeref:
            time_in_sc = official_servicecredit_time_in

        # Check if time_out is after official_office_out
        if time_out_sc  > official_servicecredit_time_out and time_out_sc != timeref:
            time_out_sc = official_servicecredit_time_out 
        else:
            time_out_sc = time_out               
        #------------------------------------------------------------------------------------   
        
       #--------OVER TIME-------------------------------------------------------------------
       # Check if time_in is before official_office_in
        if time_in != timeref:
            time_in_ot = official_overtime_time_in
        # Check if time_out is after official_office_out
        if time_out_ot  > official_overtime_time_out:
            time_out_ot = official_overtime_time_out    
        else:
            time_out_ot = time_out         
        #------------------------------------------------------------------------------------   

        # Calculate the difference
        if break_in and time_in != timeref:
            difference_morning = datetime.combine(datetime.today(), break_in) - datetime.combine(datetime.today(), time_in)
            # print(difference_morning)
        else:
            difference_morning = timeref
            
        if break_in and time_out_office != timeref:
            difference_afternoon = datetime.combine(datetime.today(), time_out_office) - datetime.combine(datetime.today(), break_out)
        else:
            difference_afternoon = timeref
            
        
        # Extract hours and minutes from the morning session
        if difference_morning == timeref:
            difference_hours_morning = 0
            difference_minutes_morning = 0
        else:
            difference_hours_morning = difference_morning.total_seconds() // 3600
            difference_minutes_morning = (difference_morning.total_seconds() % 3600) // 60
            
         # Extract hours and minutes from the afternoon session   
        if difference_afternoon == timeref: 
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
        
        
     

        
        #----------------------------------------COMPUTE HONORARIUM----------------------------
       
        if (time_out_hn > timeref and time_in_hn == timeref) or (time_out_hn == timeref and time_in_hn > timeref) or (time_out_hn == timeref and time_in_hn == timeref):
            
            difference_regular_hn = 0
            difference_hours_regular_hn = 0
            difference_minutes_regular_hn = 0
    
        else:
            difference_regular_hn = datetime.combine(datetime.today(), time_out_hn) - datetime.combine(datetime.today(), time_in_hn)
            difference_hours_regular_hn = difference_regular_hn.total_seconds() // 3600
            difference_minutes_regular_hn = (difference_regular_hn.total_seconds() % 3600) // 60

        #----------------------------------------COMPUTE HONORARIUM----------------------------
        
        #----------------------------------------COMPUTE SERVICE CREDIT----------------------------
         
        if (time_out_sc > timeref and time_in_sc == timeref) or (time_out_sc== timeref and time_in_sc > timeref) or (time_out_sc == timeref and time_in_sc == timeref):

            difference_regular_sc = 0
            difference_hours_regular_sc = 0
            difference_minutes_regular_sc = 0
    
        else:
            print(time_out)
            print(time_in)
            print("hello")
            difference_regular_sc = datetime.combine(datetime.today(), time_out_sc) - datetime.combine(datetime.today(), time_in_sc)
            difference_hours_regular_sc = difference_regular_sc.total_seconds() // 3600
            difference_minutes_regular_sc = (difference_regular_sc.total_seconds() % 3600) // 60

        #----------------------------------------COMPUTE SERVICE CREDIT----------------------------
      
        print(official_honorarium_time_in)
        print("hello")
        #----------------------------------------COMPUTE OVERTIME----------------------------
         
        if (time_out_ot > official_overtime_time_in and time_in_ot != timeref):

            # Inside the COMPUTE OVERTIME block
            difference_regular_ot = datetime.combine(datetime.today(), time_out_ot) - datetime.combine(datetime.today(), time_in_ot)

            difference_hours_regular_ot = difference_regular_ot.total_seconds() // 3600
            difference_minutes_regular_ot = (difference_regular_ot.total_seconds() % 3600) // 60
            
        
        else:

            difference_regular_ot = 0
            difference_hours_regular_ot = 0
            difference_minutes_regular_ot = 0


            



        #----------------------------------------COMPUTE OVERTIME----------------------------
        
        
        
        return difference_minutes_regular_ot,difference_hours_regular_ot, difference_minutes_regular_sc, difference_hours_regular_sc, difference_minutes_regular_hn, difference_hours_regular_hn, difference_hours_morning, difference_hours_afternoon, difference_minutes_morning, difference_minutes_afternoon, total_hours, total_minutes
        
    else:
        if (time_out > timeref and time_in == timeref) or (time_out == timeref and time_in > timeref) or (time_out == timeref and time_in == timeref):
            difference_regular = 0
            difference_hours_regular = 0
            difference_minutes_regular = 0
    
            return difference_hours_regular, difference_minutes_regular
        else:
            print(time_out)
            print(time_in)
            difference_regular = datetime.combine(datetime.today(), time_out_office) - datetime.combine(datetime.today(), time_in)
            difference_hours_regular = difference_regular.total_seconds() // 3600
            difference_minutes_regular = (difference_regular.total_seconds() % 3600) // 60

            return difference_hours_regular, difference_minutes_regular
    
# Input times
time_in = "2024-03-01 8:00:00"
break_in = "2024-03-01 12:20:00"
break_out = "2024-03-01 13:20:00"
time_out = "2024-03-01 23:00:00"
surplusHour_time_in = "2024-03-01 17:30:00"
surplusHour_time_out = "2024-03-01 21:00:00"
official_office_in = "8:00"
official_office_out = "17:00"
official_honorarium_time_in = "18:00"
official_honorarium_time_out = "22:35"
official_servicecredit_time_in = "12:00"
official_servicecredit_time_out = "13:30"
official_overtime_time_in = "18:20"
official_overtime_time_out = "21:00"
employment_status = "JO"

# Compute the time difference
if employment_status == "JO":
    difference_minutes_regular_ot,difference_hours_regular_ot, difference_minutes_regular_sc, difference_hours_regular_sc, difference_minutes_regular_hn, difference_hours_regular_hn,difference_hours_morning, difference_hours_afternoon, difference_minutes_morning, difference_minutes_afternoon, total_hours, total_minutes = compute_time_difference(time_in, time_out,
                            break_in, break_out,
                            official_office_in,
                            official_office_out,
                            official_honorarium_time_in,
                            official_honorarium_time_out,
                            official_servicecredit_time_in,
                            official_servicecredit_time_out,
                            official_overtime_time_in,
                            official_overtime_time_out,
                            employment_status,)
    
    # Print the difference for JO
    print("Morning Difference:", difference_hours_morning, "hours and", difference_minutes_morning, "minutes while the Afternoon Difference: ", difference_hours_afternoon,  "Hours and", difference_minutes_afternoon, "minutes")
    print("Total time worked: {} hours and {} minutes".format(total_hours, total_minutes))
    print("The TOTAL HONORARIUM time worked: {} hours and {} minutes".format(difference_hours_regular_hn, difference_minutes_regular_hn))
    print("The TOTAL SERVICE CREDIT time worked: {} hours and {} minutes".format(difference_hours_regular_sc, difference_minutes_regular_sc))
    print("The TOTAL OVERTIME time worked: {} hours and {} minutes".format(difference_hours_regular_ot, difference_minutes_regular_ot))
else:
    difference_minutes_regular_ot,difference_hours_regular_ot, difference_minutes_regular_sc, difference_hours_regular_sc, difference_minutes_regular_hn, difference_hours_regular_hn,difference_hours_regular, difference_minutes_regular = compute_time_difference(time_in, time_out,
                            break_in, break_out,
                            official_office_in,
                            official_office_out,
                            official_honorarium_time_in,
                            official_honorarium_time_out,
                            official_servicecredit_time_in,
                            official_servicecredit_time_out,
                            official_overtime_time_in,
                            official_overtime_time_out,
                            employment_status,)
    # Print the difference for non-JO
    print("The Total time worked: {} hours and {} minutes".format(difference_hours_regular, difference_minutes_regular))
    print("The Total Honorarium time worked: {} hours and {} minutes".format(difference_hours_regular_hn, difference_minutes_regular_hn))
    print("The Total Service Credit time worked: {} hours and {} minutes".format(difference_hours_regular_sc, difference_minutes_regular_sc))
    print("The Total Overtime time worked: {} hours and {} minutes".format(difference_hours_regular_ot, difference_minutes_regular_ot))