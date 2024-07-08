import sys
import inspect

def get_importing_script_name():
    # Using sys.argv[0] to get the script name of the initial executing program
    script_name = sys.argv[0]
    
    # Alternatively, using inspect.stack() to get the calling script's filename
    caller_frame = inspect.stack()[-1]
    calling_script = caller_frame.filename
    
    return script_name, calling_script

# Example usage
if __name__ != "__main__":
    script_name, calling_script = get_importing_script_name()
    print(f"Script name of the importing program: {script_name}")
    print(f"Calling script's filename: {calling_script}")