# Data Pre-processing
# process.py
# Created by Mauro J. Pappaterra on 19 of October 2018.
import os.path as p
import codecs
import time
import sys

# Ask user to enter path to external file
if (len(sys.argv) == 1):
    path = input("\nEnter path to 'LAPD Normalized Dataset.csv':")
else:
    path = sys.argv[1]

if (path!= ""):
    print ("\nUsing path: " + path)

months = {'1':'January', '2':'February', '3':'March', '4':'April', '5':'May', '6':'June', '7':'July', '8':'August', '9':'September', '10':'October', '11':'November', '12':'December'}

violent = ["murder", "assault", "battery", "weapon", "deadly", "violent", "kidnapping", "abuse",
           "sexual", "sex", "lynching", "rape", "riot", "aggravated", "manslaughter", "homicide"]

counter_in = 0
counter_out = 0

start = time.clock() # start clock
file_content = ""

def get_date_label (date):
    return months[date[:2].replace("0","").replace("/","")]

def get_time_label(time):

    if (len(time) == 3):
        time = '0' + time
    elif (len(time) == 2):
        time += '00'
    elif (len(time) == 1):
        time = '0' + time + '00'

    if (int(time)< 600):
        return "Night"
    elif (600 <= int(time) and int(time)< 1200):
        return "Morning"
    elif (1200 <= int(time) and int(time)< 1700):
        return "Afternoon"
    elif (1700 <= int(time) and int(time)< 2000):
        return "Evening"
    else:
        return "Night"

def get_age_label(age):

    if (int(age) <= 12):
        return "Child"
    elif (int(age) <= 21):
        return "Adolescent"
    elif (int(age) <= 35):
        return "Young Adult"
    elif (int(age) <= 64):
        return "Adult"
    else:
        return "Eldery"

def get_gender_label(gender):

    if (gender == "M"):
        return "Male"
    elif (gender == "F"):
        return "Female"
    else:
        return "Other"

def get_race_label(race):

    race = race.replace("\r","").replace("\n","")

    if (race == "W"):
        return "Caucasian"
    elif (race == "B"):
        return "African American"
    elif (race == "A" or race == "C" or race == "J" or race == "K" or race == "L"
          or race == "V" or race == "Z" or race == "F" or race == "D"):
        return "Asian"
    elif (race == "I"):
        return "Native American"
    elif (race == "G" or race == "P" or race == "S" or race == "U"):
        return "Pacific Islander"
    elif (race == "H"):
        return "Hispanic/Latino"
    else:
        return "Other"

def fix_crime_description (crime_description):

    return crime_description.title()\
        .replace("\"","")\
        .replace(" Oth 0007=02","")\
        .replace("0060","")\
        .replace("($400 & Over","($400 & Over)")\
        .replace("Crm Agnst Chld","Crime Against Child")\
        .replace("Excpt - Guns - Fowl - Livestk - Prod0036","")\
        .replace(" All Church Vandalisms) 0114","All Church Vandalism")

def fix_weapon_description (weapon_description):

    return weapon_description.title()\
        .replace("\"","")\
        .replace("Strong-Arm (Hands -  Fist -  Feet Or Bodily Force)","Strong Bodily Force")

def classify(description):

    for word in description.split():
        if (word.lower() in violent):
            return "Violent Crime"
    return "Non-Violent Crime"

with codecs.open(path + "LAPD Modified Dataset.csv", 'r', encoding='utf8') as myFile:
    file_content = myFile.readline().replace("\r","").replace("\n","") #+ ", Classification" # first line

    labels = file_content.split(',')
    print(labels)

    data = myFile.readlines()  # saves each line of the text into a list

    for entry in data:

        print("\n>INPUT => " + entry)

        entry_data = entry.split(',')

        if (not(entry_data[9] == "" or entry_data[10] == "" or entry_data[11] == "")):

            # Label Date January to December
            date_label = get_date_label(entry_data[1])
            #print (entry_data[1] + " => " + date_label)

            # Label Time Occurred
            time_label = get_time_label(entry_data[2])
            #print (entry_data[2] + " => " + time_label)

            # Correct Case Crime description
            crime_description = fix_crime_description(entry_data[6])
            #print (crime_description)

            # Correct Weapon Description
            weapon_description = fix_weapon_description(entry_data[8])
            #print (weapon_description)

            # Classify Violent/Non-Violent
            #classification = classify(entry_data[6])
            #print (classification)

            # Label Victim's Age
            age_label =  get_age_label(entry_data[9])
            #print (entry_data[9] + " => " + age_label)

            # Label Victim's Gender
            gender_label = get_gender_label(entry_data[10])
            #print (entry_data[10] + " => " + gender_label)

            # Label Victim's Race
            race_label = get_race_label(entry_data[11])
            #print(entry_data[11] + " => " + race_label)

            output = "\n" + entry_data[0] + "," + date_label + "," + time_label + "," + entry_data[3] + "," + entry_data[4] + "," \
                     + entry_data[5] + "," + crime_description + "," + entry_data[7] + "," + weapon_description + "," \
                     + age_label + "," + gender_label  + "," + race_label #+ "," + classification\


            file_content += output

            print("<OUTPUT => " + output)
            counter_in += 1

        else:
            #print("str(entry_data))
            print("<OUTPUT => Entry filtered out due to missing information!")
            counter_out += 1

# Save to disk
with open (path + "output.csv", 'w') as file:
    file.write (file_content)

# Print in Console
print ("\n::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::\nData Processing Completed in " + str(round((time.clock() - start),2)) + " seconds!")
print ("\nTotal entries read: " + str(counter_in + counter_out) + "\n-------------------------")
print ("Total entries added -> " + str(counter_in))
print ("Total entries filtered out -> " + str(counter_out))
