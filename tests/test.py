import requests

# URL of your Flask API endpoint
#api_url = 'http://fofapi.azurewebsites.net/detect' # Make sure this matches the URL your Flask app is running on
api_url = 'http://localhost:8000/detect'  # Make sure this matches the URL your Flask app is running on
# Path to the image file you want to send for object detection
image_path = 'A:/AndroidStudio/Android/diet_Api/tests/id.jpg'  # Update this to the path of your image

# Open the image file in binary mode
with open(image_path, 'rb') as image_file:
    # Construct the multipart/form-data request with the image file
    files = {'image': (image_path, image_file)}
    
    # Sending a POST request to the Flask API with the image file
    response = requests.post(api_url, files=files)

# Check the response from the server
if response.status_code == 200:
    print("Successfully sent the image to the API.")
    # Parse the JSON response from the API
    response_data = response.json()
    print("Response from API:", response_data)
else:
    print(f"Failed to send the image. Status code: {response.status_code}")
    print("Response:", response.text)


