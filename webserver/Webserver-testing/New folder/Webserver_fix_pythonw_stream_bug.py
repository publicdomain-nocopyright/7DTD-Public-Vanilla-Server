## Maybe redirecting to a log file would be a solution.
# This problem seems to be due to pythonw not having GUI to redirect error stream to. 
import sys
if sys.stderr is None:
    import io
    sys.stderr = io.StringIO()