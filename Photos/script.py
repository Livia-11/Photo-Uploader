import os
import time
import shutil
import subprocess
import sys
# Ensure UTF-8 encoding for output
sys.stdout.reconfigure(encoding='utf-8')
# Define folder paths
monitor_folder = r"C:\Users\pc\Pictures\pictures"  #Folder where pictures to upload are stored
uploaded_folder = r"C:\Users\pc\Pictures\uploaded"   #Folder where pictures uploaded are stored    
# Ensure the 'uploaded' folder exists
if not os.path.exists(uploaded_folder):
    os.makedirs(uploaded_folder)
# URL for file upload
upload_url = "https://projects.benax.rw/f/o/r/e/a/c/h/p/r/o/j/e/c/t/s/4e8d42b606f70fa9d39741a93ed0356c/iot_testing_202501/upload.php"
# Allowed file extensions
allowed_extensions = {".jpeg", ".jpg", ".png"}
# Function to upload a file using curl
def upload_file(file_path):
    try:
        # Execute the curl command
        response = subprocess.run(
            ["curl", "-X", "POST", "-F", f"imageFile=@\"{file_path}\"", upload_url],
            capture_output=True,
            text=True,
            shell=True  # Use shell=True on Windows
        )
        # Check if the upload was successful
        if response.returncode == 0:
            print(f"Uploaded successfully: {file_path}")
            return True
        else:
            print(f"Failed to upload {file_path}: {response.stderr}")
            return False
    except Exception as e:
        print(f"Error during upload: {str(e)}")
        return False
# Function to move the file to the 'uploaded' folder
def move_file(file_path, destination_folder):
    try:
        shutil.move(file_path, destination_folder)
        print(f"Moved file to {destination_folder}: {file_path}")
    except Exception as e:
        print(f"Error moving file: {str(e)}")
# Monitor the folder and process new files
def monitor_and_upload():
    print("Monitoring folder for new files...")
    while True:
        # Get list of files in the folder
        files = [f for f in os.listdir(monitor_folder) if os.path.isfile(os.path.join(monitor_folder, f))]
        for file in files:
            file_path = os.path.join(monitor_folder, file)
            print(f"Processing file: {file}")
            # Skip unsupported file formats
            if not os.path.splitext(file_path)[1].lower() in allowed_extensions:
                print(f"Skipping unsupported file: {file}")
                continue
            # Upload the file
            if upload_file(file_path):
                # Move the file to the uploaded folder
                move_file(file_path, uploaded_folder)
            else:
                print(f"Skipping file due to upload failure: {file}")
            # Wait 30 seconds before processing the next file
            time.sleep(30)
        # Wait a bit before checking the folder again
        time.sleep(5)
# Run the script
if __name__ == "__main__":
    try:
        monitor_and_upload()
    except KeyboardInterrupt:
        print("\nStopped by user.")






