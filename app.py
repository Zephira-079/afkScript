from pynput.mouse import Controller as MouseController
from pynput.keyboard import Controller as KeyboardController
import time
import subprocess
import os
import psutil

countdown = int(input("Seconds before considering AFK: ")) or 120
t_countdown = 0

mouse = MouseController()
keyboard = KeyboardController()
is_task = False
afk_file = "./afk.txt"

x, y = mouse.position

def is_notepad_running():
    try:
        for proc in psutil.process_iter(['pid', 'name']):
            if 'notepad.exe' in proc.info['name'].lower():
                return True
        return False
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        return False

while True:
    c_x, c_y = mouse.position

    if c_x != x or c_y != y:
        # Mouse is moving
        if os.path.exists(afk_file):
            is_task = False
            
            # Kill any running instances of Notepad
            try:
                subprocess.call("TASKKILL /F /IM notepad.exe", shell=True)
                is_task = True
            except Exception as e:
                print(f"Error killing Notepad process: {e}")
            
            # Wait for Notepad to terminate
            if is_task:
                while is_notepad_running():
                    time.sleep(1)
            
            # Remove afk.txt if it exists and Notepad was terminated
            if os.path.exists(afk_file):
                try:
                    os.remove(afk_file)
                    print("afk.txt removed successfully.")
                except Exception as e:
                    print(f"Error removing afk.txt: {e}")
            else:
                print("afk.txt does not exist.")
        else:
            print("afk.txt does not exist.")

        print("Mouse is moving")
        x = c_x
        y = c_y
        t_countdown = 0  # Reset countdown
        
    else:
        # Mouse is not moving
        if t_countdown == countdown:
            with open(afk_file, "w") as f:
                f.write(f"AFK for {t_countdown - countdown} seconds\n")  # Write to afk.txt
            subprocess.Popen(["notepad", afk_file])

            t_countdown += 1
        elif t_countdown >= countdown:
            if os.path.exists(afk_file):
                with open(afk_file, "a") as f:
                    f.write(f"AFK for {t_countdown - countdown} seconds\n")  # Append to afk.txt
            else:
                with open(afk_file, "w") as f:
                    f.write(f"AFK for {t_countdown - countdown} seconds\n")  # Write to afk.txt
            subprocess.Popen(["notepad", afk_file])

            t_countdown += 1
        else:
            t_countdown += 1
        
        print(f"Countdown: {t_countdown}/{countdown} seconds")

    time.sleep(1)
