def produce_renamed_python_executable(new_executable_path: str):
    import os, shutil, pathlib, sys
    python_executable_installed = pathlib.Path(sys.exec_prefix, 'python.exe')  # change to pythonw to create a pythonw executable.
    python_executable_new = pathlib.Path(new_executable_path)
    os.makedirs(os.path.dirname(new_executable_path), exist_ok=True)
    return str(os.path.abspath(shutil.copy2(python_executable_installed, python_executable_new)))

def main():
    import argparse
    parser = argparse.ArgumentParser(
        description='Produce renamed Python Executable on Windows Operating System.', 
        epilog='Example usage: python %(prog)s ".\\test.exe"')
    parser.add_argument('file_path', type=str, help='Path to the new executable file')
    try:
        new_executable_path = produce_renamed_python_executable(parser.parse_args().file_path)
        print(f"Successfully created new executable at: {new_executable_path}")
        return 0
    except FileNotFoundError:
        print("Error: Source Python executable not found.", file=sys.stderr)
        return 1
    except PermissionError:
        print("Error: Permission denied. Make sure you have the necessary rights.", file=sys.stderr)
        return 2
    except Exception as e:
        print(f"Error: An unexpected error occurred: {str(e)}", file=sys.stderr)
        return 3

if __name__=="__main__": 
    import sys
    sys.exit(main())