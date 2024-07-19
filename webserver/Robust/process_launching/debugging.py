import inspect

def debug_function(func):
    def wrapper(*args, **kwargs):
        frame = inspect.currentframe()
        try:
            # Get local variables of the called function
            local_vars = inspect.getargvalues(frame).locals
            print(f"Function: {func.__name__}")
            print("Arguments:")
            for name, value in local_vars.items():
                if name != 'frame':
                    print(f"  {name} = {value}")
            
            # Call the original function
            result = func(*args, **kwargs)
            
            print(f"Return value: {result}")
            return result
        finally:
            del frame  # Avoid reference cycles

    return wrapper

@debug_function
def example_function(a, b, c=3):
    return a + b + c

# Test the decorated function
example_function(1, 2, c=4)