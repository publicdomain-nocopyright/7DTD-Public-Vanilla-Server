def produce_renamed_python_executable(new_executable_path: str):
    import os, shutil, pathlib, sys
    python_executable_installed = pathlib.Path(sys.exec_prefix, 'python.exe')  # change to pythonw to create a pythonw executable.
    python_executable_new = pathlib.Path(new_executable_path)
    os.makedirs(os.path.dirname(new_executable_path), exist_ok=True)
    return str(shutil.copy2(python_executable_installed, python_executable_new))

if __name__=="__main__": 
    import argparse
    parser = argparse.ArgumentParser(description='Produce renamed Python Executable.')
    parser.add_argument('file_path', type=str, help='Path to the file to be processed. Example usage: python %(prog)s .\\test.exe')
    produce_renamed_python_executable(parser.parse_args().file_path)
    # python library-simplified.py ".\test.exe"