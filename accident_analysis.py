# ================================
# PRODIGY DS TASK 05
# Traffic Accident Analysis Project
# ================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from folium.plugins import HeatMap
import os

print("Libraries Loaded Successfully")

# ================================
# CREATE OUTPUT FOLDER
# ================================
if not os.path.exists("outputs"):
    os.makedirs("outputs")
    print("Outputs folder created")
else:
    print("Outputs folder already exists")

# ================================
# LOAD DATASET
# ================================
print("Loading Dataset...")
df = pd.read_csv("US_Accidents_March23.csv")
print("Dataset Loaded!")
print("Shape:", df.shape)

# ================================
# SELECT REQUIRED COLUMNS
# ================================
df = df[['Start_Time','Weather_Condition','Severity','Start_Lat','Start_Lng']]

# ================================
# DATA PREPROCESSING (FIXED)
# ================================
print("Preprocessing Data...")

# Fix timestamp issue
df['Start_Time'] = pd.to_datetime(df['Start_Time'], format='mixed', errors='coerce')

# Remove invalid time rows
df = df.dropna(subset=['Start_Time'])

# Extract Hour & Day
df['Hour'] = df['Start_Time'].dt.hour
df['Day'] = df['Start_Time'].dt.day_name()

# Drop remaining missing values
df.dropna(inplace=True)

print("Preprocessing Done")
print("Cleaned Shape:", df.shape)

# ================================
# VISUALIZATION 1: Accidents by Hour
# ================================
plt.figure(figsize=(10,5))
sns.histplot(df['Hour'], bins=24, kde=True)
plt.title("Accidents by Hour of Day")
plt.xlabel("Hour")
plt.ylabel("Accident Count")
plt.savefig("outputs/accidents_by_hour.png")
plt.close()

# ================================
# VISUALIZATION 2: Accidents by Day
# ================================
plt.figure(figsize=(10,5))
sns.countplot(x='Day', data=df,
              order=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'])
plt.title("Accidents by Day of Week")
plt.xticks(rotation=45)
plt.savefig("outputs/accidents_by_day.png")
plt.close()

# ================================
# VISUALIZATION 3: Weather Analysis
# ================================
weather_counts = df['Weather_Condition'].value_counts().head(10)

plt.figure(figsize=(12,6))
weather_counts.plot(kind='bar')
plt.title("Top Weather Conditions During Accidents")
plt.xlabel("Weather")
plt.ylabel("Accident Count")
plt.savefig("outputs/weather_conditions.png")
plt.close()

# ================================
# VISUALIZATION 4: Severity Analysis
# ================================
plt.figure(figsize=(8,5))
sns.countplot(x='Severity', data=df)
plt.title("Accident Severity Distribution")
plt.savefig("outputs/severity_distribution.png")
plt.close()

# ================================
# VISUALIZATION 5: Severity vs Time
# ================================
plt.figure(figsize=(10,5))
sns.boxplot(x='Severity', y='Hour', data=df)
plt.title("Severity vs Time of Day")
plt.savefig("outputs/severity_vs_time.png")
plt.close()

# ================================
# VISUALIZATION 6: Severity by Day
# ================================
plt.figure(figsize=(10,5))
sns.boxplot(x='Day', y='Severity', data=df)
plt.title("Severity by Day")
plt.xticks(rotation=45)
plt.savefig("outputs/severity_by_day.png")
plt.close()

# ================================
# HOTSPOT MAP
# ================================
print("Creating Hotspot Map...")

map_data = df[['Start_Lat','Start_Lng']].sample(5000)

m = folium.Map(location=[39.5, -98.35], zoom_start=4)
HeatMap(map_data).add_to(m)

m.save("outputs/accident_hotspots.html")

print("Hotspot Map Saved in outputs folder")
print("PROJECT COMPLETED SUCCESSFULLY")