import random
import pymongo
import json

# Connect to the MongoDB server
client = pymongo.MongoClient("mongodb://localhost:27017/")

# Select the database
db = client["mydatabase"]

    
def get_random_rgbcolor():
    r = random.randint(100,255)
    g = random.randint(100,255)
    b = random.randint(100,255)
    rgb = "rgb" + str((r,g,b))
    return rgb;

def save_into_database():
    # Check if the collection exists
    if 'products' in db.list_collection_names():
        program_collection = db['products']
        program_collection.drop()

    if 'tags' in db.list_collection_names():
        tag_collection = db['tags']
        tag_collection.drop()

    if 'platforms' in db.list_collection_names():
        platform_collection = db['platforms']
        platform_collection.drop()

    if 'geolocations' in db.list_collection_names():
        geolocation_collection = db['geolocations']
        geolocation_collection.drop()

    program_collection = db.create_collection('products')
    tag_collection = db.create_collection('tags')
    platform_collection = db.create_collection('platforms')
    geolocation_collection = db.create_collection('geolocations')

    # Open a file in read mode
    tag_file = open('tags.txt', 'r')

    # Read the lines from the tags file
    for category in tag_file:
        color = get_random_rgbcolor()
        data = {"category": category, "color": color}
        tag_collection.insert_one(data)

    # Close the file
    tag_file.close()

    # Open a file in read mode
    platform_file = open('platforms.txt', 'r')

    # Read the lines from the platform file
    for platform in platform_file:
        data = {"platform" : platform}
        platform_collection.insert_one(data)

    # Close the file
    platform_file.close()

    # Open a file in read mode
    geolocation_file = open('geolocations.txt', 'r',  encoding='utf-8')

    # Read the lines from the geolocation file
    for geolocation in geolocation_file:
        data = {"geolocation" : geolocation}
        geolocation_collection.insert_one(data)

    # Close the file
    geolocation_file.close()

    with open('products.txt', 'r') as file1, open('productlinks_new.txt', 'r') as file2:
        for line1, line2 in zip(file1, file2):
            # Do something with line1 and line2
            program_data = json.loads(line1.strip())
            product_link = line2.strip()
            program_data['product_link'] = product_link
            print(program_data)
            program_collection.insert_one(program_data)
            
    file1.close()
    file2.close()
            
    # Close the file
    # pro_file.close()

def setStatus(status):
    # Find the first document in the collection and update it
    collection = db["schedules"]
    query = {}
    new_values = { "$set": { "running": status } }
    updated_doc = collection.find_one_and_update(query, new_values)
    # Print the updated document
    print(updated_doc)
    
def main():
    save_into_database()
    print("Saved Success")
    setStatus(False)
    
if __name__ == '__main__':
    main()

