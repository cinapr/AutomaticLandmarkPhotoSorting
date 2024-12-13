
### **Automatic Landmark-Based Photo Sorting: Organizing Images by Location and Landmark**

**Automatic Landmark-Based Photo Sorting** is a Python-based tool that automatically categorizes your travel photos by their geographical location. It leverages the GPS metadata embedded in images to sort them into folders based on the city and landmark. This helps you easily organize and retrieve your photos from different locations without the hassle of manually sorting through them.

#### Key Features:

-   **Geotagging Support**: Extracts GPS coordinates from image metadata (EXIF) and uses reverse geocoding to identify the city and landmark.
-   **Automatic Categorization**: Organizes photos into folders for each city, with subfolders for landmarks.
-   **Uncategorized Photos Handling**: Images without GPS data or recognizable landmarks are moved to an "Uncategorized" folder for manual sorting.
-   **Customizable Output**: Easily specify the input and output folder paths to suit your needs.

#### How It Works:

1.  The script reads the EXIF metadata of each image to extract GPS coordinates.
2.  It uses reverse geocoding (via the Geopy API or Google Maps API) to convert coordinates into city and landmark names.
3.  Photos are automatically moved into a folder structure based on the location (e.g., `City -> Landmark -> Photos`).
4.  Images without GPS data are placed in the "Uncategorized" folder.

#### Prerequisites:

-   Python 3.9
-   Required libraries: Pillow, Geopy (install with `pip install Pillow geopy`)

#### Usage:

1.  Install the Required Libraries
`pip install Pillow geopy`

2. Clone or download the repository.

3.  Modify the paths for your input (photos) and output (organized folders).
Configure the Script:
    -   Replace `/path/to/your/images` with the path to your holiday photos folder.
    -   Replace `/path/to/sorted/images` with the desired output folder path for the organized images.

4.  Run the script and let it sort your holiday memories!
Save the script as `organize_photos.py` and execute it:
`python organize_photos.py` 


#### Example Folder Structure:

> City1/
>>     Landmark1/
>>>         photo1.jpg
>>>         photo2.jpg
>>     Landmark2/
>>>        photo3.jpg 
>>     Uncategorized/
>>>     photo4.jpg
>>>     photo5.jpg
> City2/
>>     Landmark3/
>>>         photo6.jpg
>>>         photo7.jpg
>>     Landmark4/
>>>        photo8.jpg 
>>     Uncategorized/
>>>     photo9.jpg
>>>     photo10.jpg

