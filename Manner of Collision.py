#!/usr/bin/env python
# coding: utf-8

# In[1]:


import csv
import pandas as pd
import numpy as np
from pprint import pprint
from scipy import stats as stats
import matplotlib.pyplot as plt


# In[2]:


person_path = "FARS2017NationalCSV/person.csv"
person_data = pd.read_csv(person_path)
print(person_data.columns)
person_data.head()


# In[3]:


accident_path = "FARS2017NationalCSV/accident.csv"
accident_data = pd.read_csv(accident_path)
print(accident_data.columns)
accident_data.head()


# In[4]:


vehicle_path = "FARS2017NationalCSV/vehicle.csv"
vehicle_data = pd.read_csv(vehicle_path)
print(vehicle_data.columns)
vehicle_data.head()


# In[5]:


common_pv = []
for column in person_data.columns:
    if column in vehicle_data.columns:
        common_pv.append(column)

common_pv


# In[6]:


super_df = pd.merge(vehicle_data, person_data, on=common_pv)
for column in super_df.columns:
    print(column)
super_df.head()


# In[7]:


common_pva = []
for column in accident_data.columns:
    if column in super_df.columns:
        common_pva.append(column)

common_pva


# In[8]:


super_df = pd.merge(super_df, accident_data, on=common_pva)
super_df.head()


# In[9]:


for column in super_df.columns:
    print(column)


# In[10]:


master_df = super_df[["STATE", "ST_CASE", "MAN_COLL", "DAY", "MONTH", "DRINKING", "DR_DRINK", "DRUNK_DR",
                      "AGE", "SEX", "AIR_BAG", "DRUGS", "FATALS", 
                      "HIT_RUN", "EJECTION", "DAY_WEEK", "HOUR", "MINUTE"]]
master_df.head()


# In[11]:


master_case_df = master_df[["STATE", "ST_CASE", "MAN_COLL", "DAY", "MONTH", "DRUNK_DR", "AIR_BAG",
                            "FATALS", "DAY_WEEK", "HOUR", "MINUTE"]].groupby("ST_CASE").median()

for column in master_case_df.columns:
    master_case_df[column] = master_case_df[column].astype(int)
    
master_case_df.head()


# In[12]:


master_person_df = master_df[["ST_CASE", "MAN_COLL", "AGE", "SEX", "DRINKING", "DRUGS", "HIT_RUN", "EJECTION"]]

master_person_df.head()


# In[13]:


#plt.bar(master_case_df["MAN_COLL"], master_case_df["FATALS"])
#plt.title(f"{y} by {x}")
#plt.xlabel(x)
#plt.ylabel(y)
#plt.grid(alpha = 0.25)
#plt.xticks(np.arange(0, 12))
#plt.show()


# In[14]:


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


# In[15]:


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
plt.bar(y_count.index, y_count)


# In[ ]:





# In[39]:


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
sober_bar = plt.bar(y_count.index, x_group["COUNT"]-y_count, bottom = y_count, color = "navy")

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

plt.show()


# In[38]:


#set the bar labels
plt.xticks(rotation="60")

#set the axes labels
plt.ylabel("Alcohol Involved (%)", size = 14)
plt.xlabel("Type of Collision", size = 14)

#set the title
plt.title("Drunk Drivers per Collision Fatality", size = 15)

#establish bars & stack them
percent_bar = plt.bar(y_count.index, percents, color = "crimson")

for bar in percent_bar:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2.0, height + .5, height, ha='center', va='bottom', color = "black")

plt.ylim(0, 40)    

plt.show()


# In[18]:


x_group


# In[19]:


list(df.columns)


# In[ ]:




