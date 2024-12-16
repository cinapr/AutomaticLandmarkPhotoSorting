import googlemaps

# Initialize Google Maps client (requires API key)
gmaps = googlemaps.Client(key='YOUR_GOOGLE_API_KEY')

# Function to return points of interest (POIs) like "Kamppi" from the detailed street addresses.
def get_concise_gmaps_name(latitude, longitude):
    reverse_geocode_result = gmaps.reverse_geocode((latitude, longitude))

    if reverse_geocode_result:
        for result in reverse_geocode_result:
            for component in result['address_components']:
                if 'locality' in component['types']:  # You can choose a more specific type
                    return component['long_name']
    return "Location not found"

# Example use case
latitude = 60.169857  # Kamppi
longitude = 24.938379
print(get_concise_gmaps_name(latitude, longitude))
