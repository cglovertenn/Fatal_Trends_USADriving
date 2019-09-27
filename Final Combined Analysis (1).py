#!/usr/bin/env python
# coding: utf-8

# In[57]:


import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pprint import pprint


# In[58]:




person_path = "FARS2017NationalCSV/person.csv"
person_data = pd.read_csv(person_path)
print(person_data.columns)
person_data.head()


# In[59]:


accident_path = "FARS2017NationalCSV/accident.csv"
accident_data = pd.read_csv(accident_path)
print(accident_data.columns)
accident_data.head()


# In[60]:




vehicle_path = "FARS2017NationalCSV/vehicle.csv"
vehicle_data = pd.read_csv(vehicle_path)
print(vehicle_data.columns)
vehicle_data.head()


# In[61]:




common_pv = []
for column in person_data.columns:
    if column in vehicle_data.columns:
        common_pv.append(column)

common_pv


# In[62]:




super_df = pd.merge(vehicle_data, person_data, on=common_pv)
for column in super_df.columns:
    print(column)
super_df.head()


# In[63]:




common_pva = []
for column in accident_data.columns:
    if column in super_df.columns:
        common_pva.append(column)

common_pva


# In[64]:




super_df = pd.merge(super_df, accident_data, on=common_pva)
super_df.head()


# In[65]:




for column in super_df.columns:
    print(column)


# In[66]:


master_df = super_df[["DAY", "STATE", "ST_CASE", "DAY", "MONTH", "MAKE", "MODEL", "DEATHS", "DR_DRINK", 
                      "AGE", "SEX", "AIR_BAG", "DRINKING", "DRUGS", "HOSPITAL", "DOA", "DEATH_MO", "DEATH_YR", 
                      "CITY", "YEAR", "LATITUDE", "LONGITUD", "WEATHER1", "WEATHER2", "WEATHER", "FATALS", 
                      "DRUNK_DR", "MOD_YEAR", "ROLLOVER", "DR_ZIP", "DR_HGT", "DR_WGT", "PREV_DWI", "SEAT_POS", 
                      "EJECTION", "DAY_WEEK", "REST_USE", "LGT_COND", "MAN_COLL", "REST_MIS"]]
master_df.head()


# In[67]:


master_newage = master_df.loc[master_df["AGE"] <= 110]
master_newage.head()


# In[68]:


fatals_count = master_newage["DEATHS"].sum()
fatals_count


# In[69]:


master_abbr = master_newage 

master_group = master_abbr.groupby("AGE")
fatals_count = master_group["DEATHS"].sum()

plt.title("Fatal Accident Driver by Age")
plt.xlabel("Age")
plt.ylabel("Fatal Accident Involvement")
plt.grid()
plt.plot(fatals_count)
plt.tight_layout
plt.savefig("fatal_age_fig2")
plt.show()


# In[70]:


drinking_count = master_newage["DR_DRINK"].sum()
drinking_count


# In[71]:


drinking_abbr = master_newage

drinking_group = drinking_abbr.groupby("AGE")
drinking_count = drinking_group["DR_DRINK"].sum()

plt.title("Fatal Accident Drunk Driver by Age")
plt.xlabel("Age")
plt.xlim(0, 110)
plt.ylabel("Drunk Drivers Involved")
plt.grid()
plt.plot(drinking_count)
plt.tight_layout
plt.savefig("fatal_drunk_fig2")
plt.show()


# In[72]:


gender_abbr = master_newage[master_newage["SEX"].isin([1,2])]

gender_group = gender_abbr.groupby("SEX")
gender_count = gender_group["DR_DRINK"].sum()
gender_count.head()


# In[73]:


x_axis = [1, 2]
plt.bar(x_axis, gender_count)
sex_mf = ["Male", "Female"]

plt.title("Fatal Accident Drunk Driver by Gender")
plt.ylabel("Drunk Drivers Involved")
plt.xlim(0, 3)
plt.xticks(np.arange(0,3,1))
plt.xlabel(['Male', 'Female'])
plt.tight_layout
plt.savefig("drunk_gender_fig2")
plt.show()


# In[74]:


crashes_data =  master_df
crashes_by_weather = crashes_data[["ST_CASE","LGT_COND","WEATHER","FATALS"]]
light_condition = {1: "Daylight",
                  2: "Dark but Lighted",
                  3: "Dark",
                  4: "Dawn or Dusk",
                  5: "Unknown",
                  6: "Dark - Unknown Lighting",
                  7: "Other",
                  8: "Not Reported",
                  9: "Unknown"}
weather_condition = {1:"Clear",
                    2:"Rain",
                    10: "Cloudy",
                    99: "Unknown",
                    5: "Fog",
                    4: "Snow",
                    3: "Sleet or Hail",
                    12: "Freezing Rain",
                    11: "Blowing Snow",
                    98: "Not Reported",
                    7: "Blowing Sand",
                    6: "Severe Crosswinds",
                    8: "Other"}
# convert weather condition dictionary into a Dataframe
weather_condition_df= pd.DataFrame(list(weather_condition.items()), columns=["WEATHER","Weather Condition"])
# merge weather condition Dataframe with crashes_by_weather DataFrame
weather_merged = pd.merge(crashes_by_weather, weather_condition_df, on="WEATHER", how="outer")
# drop duplicate data
weather_merged = weather_merged.drop_duplicates()
# rename LGT_COND column to Light Condition
weather_merged = weather_merged.rename(columns={"LGT_COND":"Light Condition"})
weather_merged["WEATHER"].head(10)
#weather_merged = weather_merged[weather_merged.WEATHER==1]
weather_merged = weather_merged.loc[(weather_merged["WEATHER"]==1) |
                           (weather_merged["WEATHER"]==2) |
                           (weather_merged["WEATHER"]==10) |
                           (weather_merged["WEATHER"]==5) |
                           (weather_merged["WEATHER"]==4)
                          ]

# group the dataframe based on light condition and weather condition
weather_merged_group = pd.DataFrame(weather_merged.groupby(["Light Condition","Weather Condition"], as_index=False)["FATALS"].sum())
#weather_merged_group = pd.DataFrame(weather_merged.groupby(["Light Condition","Weather Condition"], as_index=False).agg(["FATALS"].sum())
weather_merged_reduced = weather_merged_group.loc[lambda weather_merged_group: weather_merged_group['Light Condition'] <=4]
#display the Data Horizontally
weather_merged_df = weather_merged_reduced.pivot_table(weather_merged_reduced, index=["Weather Condition"], columns=["Light Condition"])
weather_merged_df[weather_merged_df["FATALS"] == "Weather Condition"]
#rename the columns(light condition code) in the pivot table to its corresponding description from the light_condition dictionary
for condition in light_condition:
  new_name= light_condition[condition]
  weather_merged_df = weather_merged_df.rename(columns={condition : new_name})
wea_cond = weather_merged_df["FATALS"].index.values
tick_locations=[]
for desc in wea_cond:
   tick_locations.append(desc)
tick_locations
x_axis = tick_locations
plt.figure(figsize=(16,8))
plt.title("Fatal Crashes by Weather Condition and Light Condition\n 2017")
plt.ylabel("Number of Fatalities")
plt.xlabel("Weather Condition")
plt.plot(x_axis, weather_merged_df["FATALS"]["Daylight"], "ro", linestyle="solid")
plt.plot(x_axis, weather_merged_df["FATALS"]["Dark but Lighted"], "b^", linestyle="solid")
plt.plot(x_axis, weather_merged_df["FATALS"]["Dark"], "kd", linestyle="solid")
plt.plot(x_axis, weather_merged_df["FATALS"]["Dawn or Dusk"], "gs", linestyle="solid")
plt.legend(loc='best', fontsize=12, fancybox=True)
plt.grid()
plt.savefig("WeathLightCond.png")
plt.show()
#plt.xticks(locations, labels)
weather_merged_df
weather_merged_reduced
df = weather_merged_reduced.groupby(["Light Condition", "Weather Condition"])["FATALS"].sum()
result = pd.DataFrame(df)
result = result.reset_index()
result["FATALS"]
plt.figure(figsize=(16,8))
plt.title("Fatal Crashes by Weather Condition and Light Condition\n2017")
plt.xlabel("Light Condition")
plt.ylabel("Weather Condition")
x = np.random.rand(20)
plt.scatter(result["Light Condition"], result["Weather Condition"],result["FATALS"],c=x, alpha=0.5, edgecolors="black", linewidth=2)
x,y= result["Light Condition"],result["Weather Condition"]
for i, txt in enumerate(result["FATALS"]):
   plt.annotate(txt, (x[i], y[i]))
#legend
fatalities_list=list(result["FATALS"])
plt.xticks(np.arange(1,5,1), ('Daylight', 'Dark but Lighted', 'Dark', 'Dawn'))
#plt.grid()
plt.savefig("BubblePlot.png")
plt.show()


# In[3]:


master_case_df = master_df[["STATE", "ST_CASE", "MAN_COLL", "DAY", "MONTH", "DRUNK_DR", "AIR_BAG",
                            "FATALS", "DAY_WEEK", "HOUR", "MINUTE"]].groupby("ST_CASE").median()

for column in master_case_df.columns:
    master_case_df[column] = master_case_df[column].astype(int)
    
master_case_df.head()

master_person_df = master_df[["ST_CASE", "MAN_COLL", "AGE", "SEX", "DRINKING", "DRUGS", "HIT_RUN", "EJECTION"]]

master_person_df.head()

#copy the dataframe up to persnickety rows
df = master_case_df.copy()

#add column for counting
df["COUNT"] = 1

#remove unreported and unknown values
sub_set = df.loc[df["MAN_COLL"] < 88]

#rename "manner of collision" values for easy reading
sub_set = sub_set.replace({"MAN_COLL": {0:"No Other Car", 1:"Front-to-Rear", 2:"Front-to-Front", 6:"Angle",
                                        7:"Sideswipe (Same Dir.)", 8:"Sideswipe (Opp. Dir.)", 9:"Rear-to-Side",
                                        10:"Rear-to-Rear", 11:"Other"}})

df.head()

#sum totals by manner of collision
x_group = sub_set.groupby("MAN_COLL").sum()

#select column to compare
y_count = x_group["FATALS"]

#set the bar labels
plt.xticks(rotation="60")

#set the axes labels
plt.ylabel("Fatalities", size = 16)
plt.xlabel("Type of Collision", size = 16)

#set the title
plt.title("Fatalities by Collision Type", size = 20)

#show the thing
fatals_bar = plt.bar(y_count.index, y_count)

#add numbers above bars
for bar in fatals_bar:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2.0, height + 250, height, ha='center', va='bottom', color = "black")

#set your dimensions
plt.tight_layout()

#make room
plt.ylim(0, 25000)

#save it
plt.savefig("Fatals_per_Col_Type")

#sum totals by manner of collision
x_group = sub_set.groupby("MAN_COLL").sum()

#select column to compare
y_count = x_group["DRUNK_DR"]

#set the bar labels
plt.xticks(rotation="60")

#set the axes labels
plt.ylabel("Drunk Drivers", size = 14)
plt.xlabel("Type of Collision", size = 14)

#set the title
plt.title("Drunk Drivers per Collision Fatality", size = 15)

#establish bars & stack them
drunk_bar = plt.bar(y_count.index, y_count, color = "crimson")
sober_bar = plt.bar(y_count.index, x_group["COUNT"]-y_count, bottom = y_count)

#get the values of each full bar
sober_height = []
for bar in sober_bar:
    sober_height.append(int(bar.get_height()))

percents = []

#calculate percentages & overlay text on graph
sob_num = 0
for bar in drunk_bar:
    height = bar.get_height()
    prcnt = round(height/(sober_height[sob_num]+height)*100, 1)
    percents.append(prcnt)
    #overlay percentages over graph with appropriate colors
    if height >= 500:
        plt.text(bar.get_x() + bar.get_width()/2.0, height + 200, height, ha='center', va='bottom', color = "white")
    else:
        plt.text(bar.get_x() + bar.get_width()/2.0, 700, height, ha='center', va='bottom', color = "black")
    sob_num += 1

plt.legend((sober_bar[0], drunk_bar[0]), ('Total wrecks', 'Alcohol involved'))

#set your dimensions
plt.tight_layout()

#save it
plt.savefig("Num_Drunk_per_Col_Type")

#show the thing
plt.show()

#set the bar labels
plt.xticks(rotation="60")

#set the axes labels
plt.ylabel("Alcohol Involved (%)", size = 14)
plt.xlabel("Type of Collision", size = 14)

#set the title
plt.title("Drunk Drivers per Collision Fatality", size = 15)

#establish bars & stack them
percent_bar = plt.bar(y_count.index, percents, color = "crimson")

#add numbers above bars
for bar in percent_bar:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2.0, height + .5, height, ha='center', va='bottom', color = "black")

#make room for numbers
plt.ylim(0, 40)

#set your dimensions
plt.tight_layout()

#save it
plt.savefig("Prcnt_Drunk_per_Col_Type")

#show the thing
plt.show()

#print for visualization
x_group

#print list for visualization
list(df.columns)


# In[14]:


mastersex = master_df[["TIME","DAY_WEEK","SEX","FATALS"]]
master_sex=mastersex.loc[mastersex["TIME"] <= 24]
master_sex["TIME"] = master_sex["TIME"].astype(int)
master_sex = master_sex[master_sex["SEX"].isin([1,2])]

sunday = master_sex[master_sex["DAY_WEEK"] == 1].groupby("TIME")["FATALS"].sum()
monday = master_sex[master_sex["DAY_WEEK"] == 2].groupby("TIME")["FATALS"].sum()
tuesday = master_sex[master_sex["DAY_WEEK"] == 3].groupby("TIME")["FATALS"].sum()
wednesday = master_sex[master_sex["DAY_WEEK"] == 4].groupby("TIME")["FATALS"].sum()
thursday = master_sex[master_sex["DAY_WEEK"] == 5].groupby("TIME")["FATALS"].sum()
friday = master_sex[master_sex["DAY_WEEK"] == 6].groupby("TIME")["FATALS"].sum()
saturday = master_sex[master_sex["DAY_WEEK"] == 7].groupby("TIME")["FATALS"].sum()
male = master_sex[master_sex["SEX"] == 1].groupby("TIME")["FATALS"].sum()
female = master_sex[master_sex["SEX"] == 2].groupby("TIME")["FATALS"].sum()

master = master_sex.groupby("TIME")
fatals_count = master["FATALS"].sum()
plt.clf()
plt.rcParams["figure.figsize"]=20,20
plt.plot(male.index.values, male, label = "Male", color = "blue", linestyle='dashed')
plt.plot(female.index.values, female, label = "Female", color = "pink", linestyle='dashed')
plt.title("Involved in Fatal Accident by Time of Day")
plt.xlabel("Hour of Day in Military Time")
plt.ylabel("Fatal Crash Involving by Sex")
plt.xlim(0,24)
plt.xticks(np.arange(0, 25, 1))
plt.legend()
plt.grid()
plt.savefig('gendertime')
plt.show()

master = master_sex.groupby("DAY_WEEK")
fatals_count = master["FATALS"].sum()
plt.clf()
plt.rcParams["figure.figsize"]=20,20
plt.plot(male.index.values, male, label = "Male", color = "blue", linestyle='dashed')
plt.plot(female.index.values, female, label = "Female", color = "pink", linestyle='dashed')
plt.title("Involved in Fatal Accident by Day of Week")
plt.xlabel("Day of Week")
plt.ylabel("Fatal Crash Involving by Sex")
plt.legend()
plt.grid()
plt.savefig('genderday')
plt.show()

master = master_sex.groupby("TIME")
fatals_count = master["FATALS"].sum()
plt.clf()
plt.rcParams["figure.figsize"]=20,20
plt.plot(sunday.index.values, sunday, label = "Sunday", color = "purple")
plt.plot(monday.index.values, monday, label = "Monday", alpha = .3, color = "darkblue", marker="x")
plt.plot(tuesday.index.values, tuesday, label = "Tuesday", alpha = .3, color = "black", marker="x")
plt.plot(wednesday.index.values, wednesday, label = "Wednesday", alpha = .3, color = "orange", marker="x")
plt.plot(thursday.index.values, thursday, label = "Thursday", alpha = .3, color = "yellow", marker="x")
plt.plot(friday.index.values, friday, label = "Friday", color = "green")
plt.plot(saturday.index.values, saturday, label = "Saturday", color = "red")
plt.plot(male.index.values, male, label = "Male", color = "blue", linestyle='dashed')
plt.plot(female.index.values, female, label = "Female", color = "pink", linestyle='dashed')
plt.title("Involved in Fatal Accident by Time of Day")
plt.xlabel("Hour of Day in Military Time")
plt.ylabel("Fatal Crash Involving by Sex")
plt.xlim(0,24)
plt.xticks(np.arange(0, 25, 1))
plt.legend()
plt.grid()
plt.savefig('genderdaytime')
plt.show()

masterdrug = master_df[["TIME","DAY_WEEK","DRUGS","FATALS"]]
master_drug = masterdrug.loc[masterdrug["TIME"] <= 24]
master_drug["TIME"] = master_drug["TIME"].astype(int)
master_drug = master_drug[master_drug["DRUGS"].isin([1])]
master_drug.head()

sunday = master_drug[master_drug["DAY_WEEK"] == 1].groupby("TIME")["FATALS"].sum()
monday = master_drug[master_drug["DAY_WEEK"] == 2].groupby("TIME")["FATALS"].sum()
tuesday = master_drug[master_drug["DAY_WEEK"] == 3].groupby("TIME")["FATALS"].sum()
wednesday = master_drug[master_drug["DAY_WEEK"] == 4].groupby("TIME")["FATALS"].sum()
thursday = master_drug[master_drug["DAY_WEEK"] == 5].groupby("TIME")["FATALS"].sum()
friday = master_drug[master_drug["DAY_WEEK"] == 6].groupby("TIME")["FATALS"].sum()
saturday = master_drug[master_drug["DAY_WEEK"] == 7].groupby("TIME")["FATALS"].sum()
sunday.head()

master_drugs = master_drug  #[:1000]
master = master_drugs.groupby("TIME")
fatals_count = master["FATALS"].sum()
plt.clf()
plt.rcParams["figure.figsize"]=20,20
plt.plot(sunday.index.values, sunday, label = "Sunday", color = "purple")
plt.plot(monday.index.values, monday, label = "Monday", alpha = .3, color = "darkblue", marker="x")
plt.plot(tuesday.index.values, tuesday, label = "Tuesday", alpha = .3, color = "black", marker="x")
plt.plot(wednesday.index.values, wednesday, label = "Wednesday", alpha = .3, color = "orange", marker="x")
plt.plot(thursday.index.values, thursday, label = "Thursday", alpha = .3, color = "yellow", marker="x")
plt.plot(friday.index.values, friday, label = "Friday", color = "green")
plt.plot(saturday.index.values, saturday, label = "Saturday", color = "red")
plt.title("Involved in Fatal Accident by Time of Day")
plt.xlabel("Hour of Day in Military Time")
plt.ylabel("Fatal Crash Involving Drugs")
plt.xlim(0,24)
plt.xticks(np.arange(0, 25, 1))
plt.legend()
plt.grid()
plt.savefig('drugtime')
plt.show()

mastertime = master_df[["TIME","DAY_WEEK","DR_DRINK","FATALS"]]
master_time=mastertime.loc[mastertime["TIME"] <= 24]
master_time["TIME"] = master_time["TIME"].astype(int)
master_time= master_time[master_time["DR_DRINK"] != 0]

sunday = master_time[master_time["DAY_WEEK"] == 1].groupby("TIME")["FATALS"].sum()
monday = master_time[master_time["DAY_WEEK"] == 2].groupby("TIME")["FATALS"].sum()
tuesday = master_time[master_time["DAY_WEEK"] == 3].groupby("TIME")["FATALS"].sum()
wednesday = master_time[master_time["DAY_WEEK"] == 4].groupby("TIME")["FATALS"].sum()
thursday = master_time[master_time["DAY_WEEK"] == 5].groupby("TIME")["FATALS"].sum()
friday = master_time[master_time["DAY_WEEK"] == 6].groupby("TIME")["FATALS"].sum()
saturday = master_time[master_time["DAY_WEEK"] == 7].groupby("TIME")["FATALS"].sum()
sunday.head()

master_clock = master_time  #[:1000]
mastergroup = master_clock.groupby("TIME")
fatals_count = mastergroup["FATALS"].sum()
plt.clf()
plt.rcParams["figure.figsize"]=20,20
plt.plot(sunday.index.values, sunday, label = "Sunday", color = "purple")
plt.plot(monday.index.values, monday, label = "Monday", alpha = .3, color = "darkblue", marker="x")
plt.plot(tuesday.index.values, tuesday, label = "Tuesday", alpha = .3, color = "black", marker="x")
plt.plot(wednesday.index.values, wednesday, label = "Wednesday", alpha = .3, color = "orange", marker="x")
plt.plot(thursday.index.values, thursday, label = "Thursday", alpha = .3, color = "yellow", marker="x")
plt.plot(friday.index.values, friday, label = "Friday", color = "green")
plt.plot(saturday.index.values, saturday, label = "Saturday", color = "red")
plt.title("Involved in Fatal Accident by Time of Day")
plt.xlabel("Hour of Day in Military Time")
plt.ylabel("Fatal Crash Involving Alcohol")
plt.xlim(0,24)
plt.xticks(np.arange(0, 25, 1))
plt.legend()
plt.grid()
plt.savefig('alcoholtime')
plt.show()



# In[ ]:




