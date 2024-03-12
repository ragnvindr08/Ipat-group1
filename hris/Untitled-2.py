if (time_out == "00:00" and time_in != "00:00"):
    time_out = 0
    time_in = 0
elif (time_out != "00:00" and time_in == "00:00"):
    time_out = 0
    time_in = 0
elif (time_out == "00:00" and time_in == "00:00"):
    time_out = 0
    time_in = 0