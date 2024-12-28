import pandas as pd
from geopy.distance import geodesic



def validate_coordinates(coord):
    try:
        lat, lng = map(float, coord)
        return -90 <= lat <= 90 and -180 <= lng <= 180
    except ValueError:
        return False
    

def DistanceCalculator(origin, destination):
    return geodesic(origin, destination).kilometers


def locationCoordinatesExtractor(locationUrl):
    coordinates = None
    if '/@' in locationUrl:
        first_split = locationUrl.split('/@')
        coordinates = first_split[1].split(',')[0:2]
    else:
        coordinates = locationUrl.split(',')
    if coordinates and validate_coordinates(coordinates):
        coordinates = tuple(map(float, coordinates))
        return coordinates

    return None













# Load the two Excel files
file1_path = "centers.xlsx"  # Path to Excel file 1
file2_path = "PlaceToEat.xlsx"  # Path to Excel file 2


# Read Excel files into DataFrames
df1 = pd.read_excel(file1_path)  # Excel file 1
df2 = pd.read_excel(file2_path)  # Excel file 2

# Merge data based on similarity of placeToEat in df1 and id in df2
result_data = []
for index, center in df1.iterrows():
    location_id = center['id']  # Assuming the second file has an 'ID' column
    if pd.notna(center['location']):
        location_coords = locationCoordinatesExtractor(center['location'])
    

        distances=[]
        for _, placetoeat in df2.iterrows():
            placetoeat_coords = placetoeat['coordinates']  
            distance = round(DistanceCalculator(location_coords, placetoeat_coords),2)
            distances.append((placetoeat['topic'], distance))
    # Save the updated data to a new Excel file
        # distances.sort(key=lambda x: x[1])  # Sort by distance
        # top_3 = distances[:3]

        # Add top 3 distances to the result_data
        # for topic_id, distance in top_3:
            result_data.append({"center_id":center['id']} | {
                                                            'placeToEat': placetoeat['id']
                                                             ,'topic': placetoeat['topic']
                                                             ,'distance': distance
                                                             ,"name":placetoeat['name']
                                                             ,"contact":placetoeat['contact']
                                                             ,"address":placetoeat['address']
                                                             ,"city":placetoeat['city']
                                                             ,"working_hours":placetoeat['working_hours']
                                                             ,"price":placetoeat['price']
                                                             ,"location":placetoeat['location']
                                                             ,"coordinates":placetoeat['coordinates']
                                                             ,"link":placetoeat['link']
                                                             ,"status":placetoeat['status']
                                                             ,"description":placetoeat['description']
                                                             ,"main_image_url":placetoeat['main_image_url']
                                                             ,"slider_images_urls":placetoeat['slider_images_urls']
                                                             
                                                             })

# Step 4: Convert the result data into a DataFrame
df = pd.DataFrame(result_data)
df = (
    df
    .sort_values(by=['center_id','topic','distance'])  # Sort by center, topic, and distance
    .groupby(['center_id', 'topic'])  # Group by center and topic
    .head(3)  # Take the top 2 nearest stations for each center-topic group
)
df.to_excel('output_with_distances.xlsx', index=False)
# df.to_excel('output_with_distances.xlsx', index=False)








# merged_df = df1.merge(df2, how='left', left_on='placeToEat', right_on='id', suffixes=('', '_new'))

# # Fill in the missing columns in Excel file 1 with data from Excel file 2
# for column in df2.columns:
#     if column not in ['id']:  # Avoid overwriting ID column
#         merged_df[column] = merged_df[column].combine_first(merged_df[column + '_new'])

# # Drop the extra columns created during merging
# merged_df = merged_df[df1.columns]