import inspect
import sys

def debug_function(func, *args, **kwargs):
    frame_container = {'frame': None}
    
    def tracer(frame, event, arg):
        if event == 'call':
            frame_container['frame'] = frame
        return tracer
    
    sys.settrace(tracer)
    try:
        result = func(*args, **kwargs)
    finally:
        sys.settrace(None)
    
    frame = frame_container['frame']
    if frame is not None:
        variables = frame.f_locals
        return variables, result
    else:
        return None, None

def sample_function(x, y):
    z = x + y
    return z

variables, result = debug_function(sample_function, 3, 4)
print("Internal Variables:", variables)
print("Function Result:", result)
