# Changes made:
# 1. Removed the line containing "timeout 15".
# 2. Removed the line containing "pause" at the end of the file.
# 3. Modified the start command to use the new format for configfile and UserDataFolder.

import os

def modify_bat_file(source_path, target_path):
    with open(source_path, 'r') as file:
        lines = file.readlines()
    
    # Remove lines containing "timeout 15" and "pause" at the end of the file
    lines = [line for line in lines if not line.strip().startswith("timeout 15")]
    if lines[-1].strip() == "pause":
        lines.pop()
    
    # Modify the start command line
    for i, line in enumerate(lines):
        if line.strip().startswith("start "):
            lines[i] = 'start %GAMENAME% -logfile "%LOGFILE%" -quit -batchmode -nographics "-configfile=%~DP0serverconfig.xml" -dedicated -UserDataFolder="%~dp0UserDataFolder"\n'
            break
    
    # Write the modified lines to the new file
    with open(target_path, 'w') as file:
        file.writelines(lines)

# Define paths
source_file = r"C:\Program Files (x86)\Steam\steamapps\common\7 Days To Die\startdedicated.bat"
current_folder = os.path.dirname(os.path.abspath(__file__))
target_file = os.path.join(current_folder, "startdedicated_modified.bat")

# Modify the bat file
modify_bat_file(source_file, target_file)

print("Modification complete. The new file is saved as 'startdedicated_modified.bat' in the current script folder.")
