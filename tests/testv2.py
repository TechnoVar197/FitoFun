import requests
import json
import os

leaf_folder = r'A:/AndroidStudio/Android/Leaffy_pro/API/tests/Leafs'
non_leaf_folder = r'A:/AndroidStudio/Android/Leaffy_pro/API/tests/noleaf'
test_folder = r'img'

def folder_reults(leaf_folder):
    # URL of your Flask API endpoint
    #api_url = 'http://127.0.0.1:5000/process-image'
    #api_url = 'http://leafyyapi.azurewebsites.net/process-image'
    api_url = 'http://localhost:5000/detect'
    c=1
    for filename in os.listdir(leaf_folder):
        print(c)
        c+=1
        image_path = os.path.join(leaf_folder, filename)
        print(image_path)
        with open(image_path, 'rb') as image_file:
            # Construct the multipart/form-data request with the image file
            files = {'image': (image_path, image_file)}
            
            # Sending a POST request to the Flask API with the image file
            response = requests.post(api_url, files=files)

        # Checking the response from the server
        if response.status_code == 200:
            print("Successfully sent the image to the API.")
            print("Response from API:", response.json())
        else:
            print(f"Status code: {response.status_code}")
            print("Response:", response.text)

folder_reults(test_folder)