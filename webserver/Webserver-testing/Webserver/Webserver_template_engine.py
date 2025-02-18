import re
import inspect

def render_template(template_file, **kwargs):
    # Read the template from file
    with open(template_file, 'r') as file:
        template_string = file.read()
    
    # Get the calling frame
    frame = inspect.currentframe().f_back
    
    # Combine local variables from the calling scope with passed kwargs
    variables = {**frame.f_locals, **kwargs}
    
    def replace_var(match):
        var_name = match.group(1)
        return str(variables.get(var_name, f'{{{{ {var_name} }}}}'))
    
    rendered_content = re.sub(r'\{\{ (\w+) \}\}', replace_var, template_string)
    return rendered_content


# Old example
            #import os
            #file_path = os.path.join(os.path.dirname(__file__), 'Page_component_simple-player-status.html')
            #with open(file_path, 'r') as file:
                #simple_player_status_component_loaded = file.read()