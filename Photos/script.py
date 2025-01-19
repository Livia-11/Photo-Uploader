import os
import time
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess

# Configuration constants
SOURCE_DIR = "C:\Users\pc\Documents\Embedded\Photos"
PROCESSED_DIR = os.path.join(SOURCE_DIR, "uploaded")  # Storage for processed images
API_ENDPOINT = "https://projects.benax.rw/f/o/r/e/a/c/h/p/r/o/j/e/c/t/s/4e8d42b66f70fa9d39741a93ed0356c/iot_testing_202501/upload.php"

# Initialize storage directory
os.makedirs(PROCESSED_DIR, exist_ok=True)

def transmit_image(image_path):
    """Transmit image file to remote server using curl."""
    try:
        print(f"Initiating transfer for {image_path}...")
        response = subprocess.run(
            ["curl", "-X", "POST", "-F", f"imageFile=@{image_path}", API_ENDPOINT],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if response.returncode == 0:
            print(f"Transfer successful: {image_path}")
            return True
        else:
            print(f"Transfer failed for {image_path}: {response.stderr.decode()}")
            return False
    except Exception as error:
        print(f"Transfer error for {image_path}: {error}")
        return False

class MediaMonitor(FileSystemEventHandler):
    """Handler for monitoring and processing new media files."""
    
    def on_created(self, event):
        if event.is_directory:
            return
            
        source_path = event.src_path
        if source_path.lower().endswith((".jpg", ".png", ".jpeg")):
            time.sleep(30)  # Delay processing for 30 seconds
            
            if transmit_image(source_path):
                # Relocate processed file
                destination_path = os.path.join(PROCESSED_DIR, os.path.basename(source_path))
                shutil.move(source_path, destination_path)
                print(f"File relocated to {destination_path}")

def main():
    """Main execution function."""
    monitor = Observer()
    handler = MediaMonitor()
    monitor.schedule(handler, SOURCE_DIR, recursive=False)
    print("Initiating file monitoring...")
    monitor.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        monitor.stop()
    monitor.join()

if __name__ == "__main__":
    main()