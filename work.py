import os
import time
import subprocess
from shutil import move

# Folder paths
input_folder = r"C:\Users\user\Pictures\Me"  # Raw string to handle backslashes
uploaded_folder = r"C:\Users\user\Pictures\uploaded"  # Raw string

# Upload URL
upload_url = "https://projects.benax.rw/f/o/r/e/a/c/h/p/r/o/j/e/c/t/s/4e8d42b606f70fa9d39741a93ed0356c/iot_testing_202501/upload.php"

# Ensure the "uploaded" folder exists
if not os.path.exists(uploaded_folder):
    os.makedirs(uploaded_folder)

# Function to upload image using curl
def upload_image(image_path):
    try:
        result = subprocess.run(
            ["curl", "-X", "POST", "-F", f"imageFile=@{image_path}", upload_url],
            capture_output=True,
            text=True
        )
        return result.returncode == 0
    except Exception as e:
        print(f"Error uploading {image_path}: {e}")
        return False

# Monitor folder and process images
def monitor_folder():
    while True:
        # Get list of files in the folder
        files = [f for f in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, f))]
        
        for file_name in files:
            file_path = os.path.join(input_folder, file_name)
            
            # Upload the image
            print(f"Uploading {file_name}...")
            if upload_image(file_path):
                print(f"Successfully uploaded {file_name}. Moving to 'uploaded' folder.")
                
                # Move file to "uploaded" folder
                move(file_path, os.path.join(uploaded_folder, file_name))
            else:
                print(f"Failed to upload {file_name}. Retrying later.")
        
        # Wait for 30 seconds before checking again
        time.sleep(30)

if __name__ == "__main__":
    monitor_folder()