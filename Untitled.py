#!/usr/bin/env python
# coding: utf-8

# In[14]:


import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pprint import pprint


# In[15]:


person_path = "FARS2017NationalCSV/person.csv"
person_data = pd.read_csv(person_path)
print(person_data.columns)
person_data.head()


# In[16]:


accident_path = "FARS2017NationalCSV/accident.csv"
accident_data = pd.read_csv(accident_path)
print(accident_data.columns)
accident_data.head()


# In[17]:


vehicle_path = "FARS2017NationalCSV/vehicle.csv"
vehicle_data = pd.read_csv(vehicle_path)
print(vehicle_data.columns)
vehicle_data.head()


# In[18]:


common_pv = []
for column in person_data.columns:
    if column in vehicle_data.columns:
        common_pv.append(column)

common_pv


# In[19]:


super_df = pd.merge(vehicle_data, person_data, on=common_pv)
for column in super_df.columns:
    print(column)
super_df.head()


# In[20]:


common_pva = []
for column in accident_data.columns:
    if column in super_df.columns:
        common_pva.append(column)

common_pva


# In[21]:


super_df = pd.merge(super_df, accident_data, on=common_pva)
super_df.head()


# In[22]:


for column in super_df.columns:
    print(column)


# In[23]:


master_df = super_df[["DAY", "STATE", "ST_CASE", "DAY", "MONTH", "MAKE", "MODEL", "DEATHS", "DR_DRINK", 
                      "AGE", "SEX", "AIR_BAG", "DRINKING", "DRUGS", "HOSPITAL", "DOA", "DEATH_MO", "DEATH_YR", 
                      "CITY", "YEAR", "LATITUDE", "LONGITUD", "WEATHER1", "WEATHER2", "WEATHER", "FATALS", 
                      "DRUNK_DR", "MOD_YEAR", "ROLLOVER", "DR_ZIP", "DR_HGT", "DR_WGT", "PREV_DWI", "SEAT_POS", 
                      "EJECTION", "DAY_WEEK", "REST_USE", "REST_MIS"]]
master_df.head()


# In[24]:


master_newage = master_df.loc[master_df["AGE"] <= 110]
master_newage.head()


# In[26]:


master_abbr = master_newage  #[:1000]

master_group = master_abbr.groupby("AGE")

fatals_count = master_group["FATALS"].sum()

plt.title("Involved in Fatal Accident by Age")
plt.xlabel("Age")
plt.ylabel("Fatal Crash Involvement")
plt.grid()
plt.plot(fatals_count)
plt.show()


# In[13]:


drinking_abbr = master_newage #[:1000]

drinking_group = drinking_abbr.groupby("ST_CASE")
drinking_age = drinking_group["AGE"].sum()
drinking_count = drinking_group["DRUNK_DR"].sum()

plt.title("Drunk Driving Accident by Age")
plt.xlabel("Age")
plt.ylabel("Drunk Driver Involved")
plt.grid()
plt.plot(drinking_count)
plt.show()


# In[14]:


gender_abbr = master_newage[:1000]

gender_group = gender_abbr.groupby("SEX")

gender_count = gender_group["DRUNK_DR"].sum()

x_axis = [1, 2]
plt.bar(x_axis, gender_count)
sex_mf = ["Male", "Female"]

plt.title("Drunk Driving Accident by Gender")
plt.ylabel("Drunk Driver Involved")
plt.xlim(0, 3)
plt.xticks(np.arange(0,3,1))
plt.xlabel(['Male', 'Female'])
plt.show()


# In[239]:


### Function that creates a bar chart comparing Columns X and Y of Dataframe DF
### by performing Method on the values of Y and assigning them to X
def any_bar(df, x, y, method):
    df = df[:2583].copy()
    x_group = df.groupby(x)
    if method == "sum":
        y_count = x_group[y].sum()
    elif method == "mean":
        y_count = x_group[y].mean()
    elif method == "median":
        y_count = x_group[y].median()
    limiter = df[x].nunique()+1
    plt.bar(np.arange(1, limiter, 1), y_count)
    plt.title(y + " by " + x)
    plt.ylabel(y)
    plt.xlim(df[x].min()-.5, df[x].max()+.5)
    plt.xticks(df[x].unique())
    plt.xlabel(x)
    #plt.savefig(y + "_by_" + x".png")


# In[240]:


master_newage.columns


# In[241]:


#Test function
any_bar(master_newage, "DAY_WEEK", "DRUNK_DR", "sum")


# In[160]:


#print the first row where things fall apart
master_newage.iloc[2583]
#still can't figure it out


# In[85]:


### Function that returns a scatter plot charting values of Column X
### for each unique value in Column Y of dataframe DF
### by the chosen method: mean, median, or sum
def scatterer(df, x, y, method):
    df = df.copy()
    grouping = df.groupby(x)
    if method == "mean":
        final = grouping[y].mean()
    elif method == "sum":
        final = grouping[y].sum()
    elif method == "median":
        final = grouping[y].median()
    plt.title(f"{y} by {x}")
    plt.xlabel(x)
    plt.ylabel(y)
    plt.grid(alpha = 0.25)
    plt.plot(final)
    plt.show()
    #plt.savefig(f"Scatterplot_total_{y}_by_{x}.png")


# In[93]:


#Test the above function
scatterer(master_newage, "AGE", "FATALS", "sum")


# In[ ]:




