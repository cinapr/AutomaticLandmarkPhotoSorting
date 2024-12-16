# Automatic Landmark-Based Photo Sorting: Organizing Images by Location and Landmark

# Automatic Landmark-Based Photo Sorting is a Python-based tool 
# that automatically categorizes your travel photos by 
# their geographical location. 
# It leverages the GPS metadata embedded in images to sort them into folders 
# based on the city and landmark. 
# This helps you easily organize 
# and retrieve your photos from different locations 
# without the hassle of manually sorting through them.

# DEPENDENCIS : pip install Pillow geopy pillow-heif piexif googlemaps
# pip install pyheif (SKIP)

import os
import shutil
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from geopy.geocoders import Nominatim
from PIL import Image
import pillow_heif
from pillow_heif import HeifImageFile
import piexif
import googlemaps

# Enable HEIC support
pillow_heif.register_heif_opener()

# Function to extract the numerator and denominator from the tuples and then perform the division.
def convert_to_degrees(value):
    """Converts GPS coordinates stored as [(num1, den1), (num2, den2), (num3, den3)]
    into decimal degrees."""
    d = value[0][0] / value[0][1]  # Degrees
    m = value[1][0] / value[1][1]  # Minutes
    s = value[2][0] / value[2][1]  # Seconds
    return d + (m / 60.0) + (s / 3600.0)



# Function to extract GPS info from image metadata
def get_gps_info(image_path):
    try:
        img = Image.open(image_path)
        gps_info = {}

        if isinstance(img, HeifImageFile):
            exif_data = img.info.get("exif", None)
            if not exif_data:
                print(f"No EXIF metadata found in HEIC file: {image_path}")
                return None

            decoded_exif = piexif.load(exif_data)
            gps_data = decoded_exif.get("GPS", {})
            if not gps_data:
                print(f"No GPS metadata found in HEIC file: {image_path}")
                return None

            lat = convert_to_degrees(gps_data[piexif.GPSIFD.GPSLatitude])
            if gps_data[piexif.GPSIFD.GPSLatitudeRef] != b'N':
                lat = -lat
            lon = convert_to_degrees(gps_data[piexif.GPSIFD.GPSLongitude])
            if gps_data[piexif.GPSIFD.GPSLongitudeRef] != b'E':
                lon = -lon

            return lat, lon

        exif_data = img._getexif()
        if not exif_data:
            return None

        for tag, value in exif_data.items():
            decoded = TAGS.get(tag, tag)
            if decoded == "GPSInfo":
                for t in value:
                    sub_decoded = GPSTAGS.get(t, t)
                    gps_info[sub_decoded] = value[t]
        if not gps_info:
            return None

        lat = convert_to_degrees(gps_info['GPSLatitude'])
        if gps_info['GPSLatitudeRef'] != 'N':
            lat = -lat
        lon = convert_to_degrees(gps_info['GPSLongitude'])
        if gps_info['GPSLongitudeRef'] != 'E':
            lon = -lon

        return lat, lon

    except KeyError as e:
        print(f"Missing expected GPS field: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error extracting GPS info: {e}")
        return None




    


# Function to get location details using Geopy
def get_location_details_addressGeopy(lat, lon):
    geolocator = Nominatim(user_agent="image_location_sorter")
    location = geolocator.reverse((lat, lon), exactly_one=True)
    if location:
        address = location.raw.get('address', {})
        return address.get('city', 'Unknown City'), address.get('attraction', location.address)
    return 'Unknown City', 'Unknown Landmark'




# Function to return concise names (points of interest or locality) from coordinates
# Function to return concise names using Google Maps API
def get_concise_gmaps_name(latitude, longitude):
    # Initialize the Google Maps client
    gmaps = googlemaps.Client(key='YOUR_API_KEY')  # Replace 'YOUR_API_KEY' with your actual Google Maps API key.

    # Get reverse geocode result
    # Reverse Geocoding: You are using the gmaps.reverse_geocode() function to retrieve information about a specific latitude and longitude.
    reverse_geocode_result = gmaps.reverse_geocode((latitude, longitude), result_type='point_of_interest')

    # Check if any results are returned
    if reverse_geocode_result:
        for result in reverse_geocode_result:
            # Look for 'point_of_interest' or similar components
            # address_components: Each result contains a list of address components like locality, neighborhood, city, etc. You can modify the code to extract the exact level of detail you want (e.g., landmark, locality).
            for component in result['address_components']:
                # result_type='point_of_interest': This parameter ensures that the result will focus on Points of Interest (POIs), which typically includes landmarks or specific locations instead of a detailed address.
                if 'point_of_interest' in result['types']:  # Check for POIs
                    return result['formatted_address']
                # Optionally, return the locality if point of interest is not found
                if 'locality' in component['types']:
                    return component['long_name']
    return "Location not found"

def get_location_details(lat, lon):
    # Use the concise name function to get a simplified address or landmark
    concise_name = get_concise_gmaps_name(lat, lon)
    if concise_name != "Location not found":
        return concise_name, concise_name  # You can modify how you return the name if needed
    else:
        return 'Unknown Location', 'Unknown Landmark'
    


# Organize images into folders
def organize_images(image_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for image_file in os.listdir(image_folder):
        image_path = os.path.join(image_folder, image_file)
        if not os.path.isfile(image_path):
            continue

        print(f"Processing {image_path}")
        
        gps_info = get_gps_info(image_path)
        if gps_info:
            lat, lon = gps_info
            city, landmark = get_location_details(lat, lon)
        else:
            city, landmark = "Uncategorized", "Uncategorized"

        # Create directory structure
        city_folder = os.path.join(output_folder, city)
        if not os.path.exists(city_folder):
            os.makedirs(city_folder)

        landmark_folder = os.path.join(city_folder, landmark)
        if not os.path.exists(landmark_folder):
            os.makedirs(landmark_folder)

        # Move image
        shutil.move(image_path, os.path.join(landmark_folder, image_file))



# Main execution
if __name__ == "__main__":
    #image_folder = "/path/to/your/images"  # Replace with your image folder path
    #output_folder = "/path/to/sorted/images"  # Replace with your desired output folder path

    image_folder = "C:/Users/Asus/Documents/GitHub/AutomaticLandmarkPhotoSorting/INPUT"
    output_folder = "C:/Users/Asus/Documents/GitHub/AutomaticLandmarkPhotoSorting/OUTPUT"
    organize_images(image_folder, output_folder)
