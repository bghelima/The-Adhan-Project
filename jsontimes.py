import json
from datetime import datetime, date
import datetime as dt
import requests
from time import sleep
import socket
import os
from os import system as sys
import platform
from math import trunc

def get_key(dicto, val):
    for key, value in dicto.items():
         if val == value:
             return key




now = datetime.now()
year = str(now.year)
today = date.today().strftime('%b %m %a')

# CCM vars for api call
location = "Europe/London"
lat, lon = 52.196830042287, 0.15195596288131316
method = 0
time = 0
both = 0

api_url = f"https://www.moonsighting.com/time_json.php?year={year}&tz={location}&lat={lat}&lon={lon}&method={method}&both={both}&time={time}"
# print(api_url, location, lat, lon)

r = requests.get(api_url)
packages_json = r.json() # dict

def get_prayer(date, debug):
    year = packages_json["times"]
    # print(year) # list
    # times = {}
    for day in year:
        if day["day"] == date:
            if debug:
                print(f"Day '{date}' found. Formatting....")
            times = {}
            times_specific = day["times"]
            # print(times_specific)

            for obj in times_specific:
                times[obj] = times_specific[obj].rstrip()
                # times = {obj, times_specific[obj].rstrip()}
            
            del times["asr_s"]
            del times["asr_h"]
            if debug:
                print(f"Function get_prayer() - {type(times)}:\n{times}\n\n")
            return times 

def nearest_prayer_time(prayers_dict, datetime):
    def nearest_time(prayers_dict, debug, dict_fomat, *delay):
        """
        Returns the closest prayer time given a dictionary with strings inside.
        The default delay value is 5, which means that the script will sleep for 5seconds.
        Delay must be an integer.
        Debug can only be True or False.

        """
        if isinstance(prayers_dict, dict):
            if debug:
                print("Function `nearest_time` called.\nDebug = True")
            pos_times = {}
            for obj in list(prayers_dict):
                current_time = datetime.now()
                xtime = datetime.strptime(prayers_dict[obj], "%H:%M")
                xtime = datetime.combine(date.today(), xtime.time())
                difference = (xtime - current_time).total_seconds()

                pos_times[prayers_dict[obj]] = difference
                pos_times = pos_times
                if debug:
                    print(pos_times)
            pos = all(val < 0 for val in pos_times.values())
            if debug:
                print(pos)
                print(pos_times)
            if pos == True:
                # print(f"All values in argument `pos_times` are positive / negative. Performing call calculation without popping.")
                prayer_name = get_key(prayers_dict, min(pos_times)).title()
                prayer_time = min(pos_times)
            elif pos != True:
                # print(f"Values in argument `pos_times`are not all positive / negative. Popping all negative values in order to isolate the pos'.")
                if debug:
                    print("Not all objects are positive")
                for obj in list(pos_times):
                    if pos_times[obj] < 0:
                        del pos_times[obj]
                if debug:
                    print(pos_times)
                prayer_name = get_key(prayers_dict, min(pos_times)).title()
                prayer_time = min(pos_times)
        
            # print(prayer_name, prayer_time, pos_times)
            if dict_fomat:
                func_return = {
                    prayer_name : prayer_time
                }
            else:
                func_return = prayer_name, prayer_time
        else:
            raise TypeError(f"{prayers_dict} is not a dictionary.")


        if isinstance(delay, int) | isinstance(delay, float):
            sleep(delay)
        else:
            sleep(2)
        return func_return

                                
    if isinstance(prayers_dict, dict):
        # print(f"Function 'nearest_prayer_time' has been initialized. Parsed Time - {datetime}")
        up, upt = nearest_time(prayers_dict, False, False, 100)
        print(f"Upcoming Prayer   ∙   {up}   {upt}")
    return up, upt
            


def main():
    def playsound_os(preference, format):
        if platform.system() == "Linux":
            sys(f"aplay {preference}.{format}")
        else:
            from playsound import playsound
            playsound(f"{preference}.{format}")
        return platform.system()
    o_s = str(platform.system())        
    checking = True
    while checking:
        today = date.today().strftime('%b %d %a')
        up_prayer, up_time = nearest_prayer_time(get_prayer(today, False), now)
        print(up_prayer, up_time)
        upt = datetime.strptime(up_time, "%H:%M")
        upt = datetime.combine(date.today(), dt.time(upt.hour, upt.minute))
        current_time = datetime.now()
        diff = upt - current_time
        trunc_diff_h = trunc(diff.seconds / 3600)
        trunc_diff_s = (diff.seconds // 60) % 60
        print(f"{trunc_diff_h} hours and {trunc_diff_s} minutes until {up_prayer}.");sleep(2)
        playsound_os("Adhan_M.Alafasy", "mp3")


if __name__ == "__main__":
    main()
                

    

