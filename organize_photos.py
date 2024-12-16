# Automatic Landmark-Based Photo Sorting: Organizing Images by Location and Landmark

# Automatic Landmark-Based Photo Sorting is a Python-based tool 
# that automatically categorizes your travel photos by 
# their geographical location. 
# It leverages the GPS metadata embedded in images to sort them into folders 
# based on the city and landmark. 
# This helps you easily organize 
# and retrieve your photos from different locations 
# without the hassle of manually sorting through them.

# DEPENDENCIS : pip install Pillow geopy pillow-heif pyheif

import os
import shutil
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from geopy.geocoders import Nominatim
from PIL import Image
import pillow_heif

# Enable HEIC support
pillow_heif.register_heif_opener()

# Function to extract GPS info from image metadata
def get_gps_info(image_path):
    try:
        img = Image.open(image_path)
        exif_data = img._getexif()
        if not exif_data:
            return None
        gps_info = {}
        for tag, value in exif_data.items():
            decoded = TAGS.get(tag, tag)
            if decoded == "GPSInfo":
                for t in value:
                    sub_decoded = GPSTAGS.get(t, t)
                    gps_info[sub_decoded] = value[t]
        if not gps_info:
            return None

        def convert_to_degrees(value):
            d = value[0][0] / value[0][1]
            m = value[1][0] / value[1][1]
            s = value[2][0] / value[2][1]
            return d + (m / 60.0) + (s / 3600.0)

        lat = convert_to_degrees(gps_info['GPSLatitude'])
        if gps_info['GPSLatitudeRef'] != 'N':
            lat = -lat
        lon = convert_to_degrees(gps_info['GPSLongitude'])
        if gps_info['GPSLongitudeRef'] != 'E':
            lon = -lon

        return lat, lon
    except Exception as e:
        print(f"Error extracting GPS info: {e}")
        return None

# Function to get location details using Geopy
def get_location_details(lat, lon):
    geolocator = Nominatim(user_agent="image_location_sorter")
    location = geolocator.reverse((lat, lon), exactly_one=True)
    if location:
        address = location.raw.get('address', {})
        return address.get('city', 'Unknown City'), address.get('attraction', location.address)
    return 'Unknown City', 'Unknown Landmark'

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
