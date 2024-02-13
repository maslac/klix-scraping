from datetime import datetime
import pandas as pd
import os
from datetime import datetime
import streamlit as st
import nivo_chart as nc

df = pd.read_csv('https://raw.githubusercontent.com/maslac/klix-scraping/main/webscraping-klix_ViK/klix_ViK.csv?raw=true')

def convert_to_unix(date_str):
    # The date format seems to be 'dd.mm.yyyy. u HH:MM'
    # We need to handle the '1 dan' case differently, so let's check for that
    if date_str.strip() == '1 dan':
        # Handle the '1 dan' case, perhaps by returning None or some default date
        return (int(datetime.now().timestamp()))
    elif date_str.strip() == '2 dana':
        return (int(datetime.now().timestamp() - 86400)) # take away 24 hours
    else:
        # Convert to datetime object
        date_time_obj = datetime.strptime(date_str, '%d.%m.%Y. u %H:%M')
        # Convert to UNIX timestamp
        timestamp = (int(date_time_obj.timestamp()))
        return timestamp

df.loc[:, 'unix_timestamp'] = df['Datum objave vijesti'].apply(convert_to_unix)

# Assuming you have a pandas DataFrame df with a column 'unix_timestamp' for dates

def convert_timestamp_to_date(unix_timestamp):
    """Converts UNIX timestamp to a date string in YYYY-MM-DD format."""
    return datetime.fromtimestamp(unix_timestamp).strftime('%Y-%m-%d')

# First, convert UNIX timestamps to human-readable dates
df.loc[:, 'day'] = df['unix_timestamp'].apply(convert_timestamp_to_date)

# Group by the 'day' column and count the number of articles per day
# Then multiply by 100 to assign points to each article
grouped_data = df.groupby('day').size() * 100

# Convert the grouped data into the required calendar_chart format
calendar_chart = [{"value": value, "day": day} for day, value in grouped_data.items()]

# The 'calendar_chart' variable now contains the data in the required format
print(calendar_chart)

chart_options =  {
        "title": "Calendar Heatmap",
        "type": "calendar",
        "height": 1200,
        "width": 600,
        "from": "2015-03-01",
        "to": "2024-02-13",
        "emptyColor": "#eeeeee",
        "colors": ["#61cdbb", "#97e3d5", "#e8c1a0", "#f47560"],
        "margin": {"top": 40, "right": 40, "bottom": 40, "left": 40},
        "yearSpacing": 40,
        "monthBorderColor": "#ffffff",
        "dayBorderWidth": 2,
        "dayBorderColor": "#ffffff",
        "legends": [
            {
                "anchor": "bottom-right",
                "direction": "row",
                "translateY": 36,
                "itemCount": 4,
                "itemWidth": 42,
                "itemHeight": 36,
                "itemsSpacing": 14,
                "itemDirection": "right-to-left",
            }
        ],
    }

nc.nivo_chart(data=calendar_chart, layout=chart_options, key="calendar_chart")
