import subprocess
import os
import shlex
import shutil
from multiprocessing import Pool

# Function to monitor and copy/delete files for a single source-destination pair
def monitor_and_copy(src, dest):
    print(f"Monitoring {src} and copying to {dest}")
    
    while True:
        cmd = f'watchman-wait {src} --fields exists,name --separator " & "'
        result = subprocess.run(shlex.split(cmd), capture_output=True, text=True)
        output = result.stdout.strip()
        
        if output:
            exists, filename = output.split(" & ")
            if exists == "True":
                # File created or modified
                src_file = os.path.join(src, filename)
                dest_file = os.path.join(dest, filename)
                print(f"Copying {src_file} to {dest_file}")
                shutil.copy(src_file, dest_file)
            elif exists == "False":
                # File deleted
                dest_file = os.path.join(dest, filename)
                if os.path.exists(dest_file):
                    print(f"Deleting {dest_file}")
                    os.remove(dest_file)

# Read the source-destination pairs from src_dest_list.txt
with open('src_dest_list.txt', 'r') as file:
    src_dest_pairs = [line.strip().split() for line in file]

# Create a pool of processes to monitor multiple source-destination pairs concurrently
with Pool(len(src_dest_pairs)) as pool:
    pool.starmap(monitor_and_copy, src_dest_pairs)

