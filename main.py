import time
import pandas as pd
from opencage.geocoder import OpenCageGeocode

# Set your OpenCage API Key
OPENCAGE_API_KEY = "0bd1b9d48d474c349aac94318f77eccb"
geocoder = OpenCageGeocode(OPENCAGE_API_KEY)

def get_lat_lon(address, max_retries=3):
    """Fetch latitude and longitude using OpenCage Geocoder with retries."""
    for attempt in range(max_retries):
        try:
            result = geocoder.geocode(address)
            if result:
                return result[0]['geometry']['lat'], result[0]['geometry']['lng']
        except Exception as e:
            print(f"Error on attempt {attempt + 1} for {address}: {e}")
            time.sleep(5)  # Delay to handle rate limits
    return None, None  # Return None if all retries fail

# Load the dataset
df = pd.read_csv("C:/Users/one33/geocoded_addresses_updated.csv")

# Geocode addresses with missing Latitude/Longitude
for index, row in df.iterrows():
    if pd.isnull(row["Latitude"]) or pd.isnull(row["Longitude"]):
        lat, lon = get_lat_lon(row["Full_Address"])
        df.at[index, "Latitude"] = lat
        df.at[index, "Longitude"] = lon

# Save the updated DataFrame
updated_file = "geocoded_addresses_opencage.csv"
df.to_csv(updated_file, index=False)

print(f"✅ Geocoding complete! Updated file saved as: {updated_file}")




import folium
import pandas as pd

# Load the geocoded dataset
df = pd.read_csv("geocoded_addresses_opencage.csv")

# Set default map center (first valid location)
valid_locations = df.dropna(subset=["Latitude", "Longitude"])
if not valid_locations.empty:
    center_lat = valid_locations.iloc[0]["Latitude"]
    center_lon = valid_locations.iloc[0]["Longitude"]
else:
    raise ValueError("No valid geocoded locations found.")

# Create the map
m = folium.Map(location=[center_lat, center_lon], zoom_start=10)

# Add markers for each location
for _, row in valid_locations.iterrows():
    folium.Marker(
        location=[row["Latitude"], row["Longitude"]],
        popup=row["Full_Address"],
        icon=folium.Icon(color="blue", icon="info-sign"),
    ).add_to(m)

# Save the interactive map
map_file = "geocoded_map.html"
m.save(map_file)

print(f"✅ Map generated successfully! Open: {map_file}")

import time
import folium
import pandas as pd
from opencage.geocoder import OpenCageGeocode

# Set your OpenCage API Key
OPENCAGE_API_KEY = "0bd1b9d48d474c349aac94318f77eccb"  # Replace with your API key
geocoder = OpenCageGeocode(OPENCAGE_API_KEY)

def retry_geocode(address, max_retries=3):
    """Fetch latitude and longitude using OpenCage with retries."""
    for attempt in range(max_retries):
        try:
            result = geocoder.geocode(address)
            if result:
                return result[0]['geometry']['lat'], result[0]['geometry']['lng']
        except Exception as e:
            print(f"Error on attempt {attempt + 1} for {address}: {e}")
            time.sleep(5)  # Handle rate limits
    return None, None  # Return None if all retries fail

# Load the geocoded dataset
df = pd.read_csv("geocoded_addresses_opencage.csv")

# List of incorrect addresses with their correct versions
addresses_to_fix = {
    "999 Juniper Rd, Boston, MA 2108": "999 Juniper Rd, Boston, MA 02108",
    "5600 Pinecone Ave, Jersey City, NJ 7302": "5600 Pinecone Ave, Jersey City, NJ 07302",
    "5100 Fir Ave, Newark, NJ 7101": "5100 Fir Ave, Newark, NJ 07101"
}

# Correct each address
for wrong_address, correct_address in addresses_to_fix.items():
    correct_lat, correct_lon = retry_geocode(correct_address)
    if correct_lat is not None and correct_lon is not None:
        df.loc[df['Full_Address'] == wrong_address, ["Latitude", "Longitude"]] = [correct_lat, correct_lon]
        print(f"✅ Corrected: {wrong_address} → {correct_address}")

# Set default map center (first valid location)
valid_locations = df.dropna(subset=["Latitude", "Longitude"])
if not valid_locations.empty:
    center_lat = valid_locations.iloc[0]["Latitude"]
    center_lon = valid_locations.iloc[0]["Longitude"]
else:
    raise ValueError("No valid geocoded locations found.")

# Create the updated map
m = folium.Map(location=[center_lat, center_lon], zoom_start=10)

# Add markers for each location
for _, row in valid_locations.iterrows():
    folium.Marker(
        location=[row["Latitude"], row["Longitude"]],
        popup=row["Full_Address"],
        icon=folium.Icon(color="blue", icon="info-sign"),
    ).add_to(m)

# Save the updated map
updated_map_file = "geocoded_map.html"
m.save(updated_map_file)

print(f"✅ Updated map saved as {updated_map_file}")

