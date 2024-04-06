# http://localhost:8001/image.png

from http.server import HTTPServer, BaseHTTPRequestHandler
from PIL import Image
from io import BytesIO

# Importing the PIL library
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
 
 
from PIL import ImageFont, ImageDraw, ImageFilter, Image
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler

 

import requests

def get_project_info():
    # Define the GraphQL query
    query = '''
    {
      project(slug: "7-days-to-die-public-dedicated") {
        settings
        name
        slug
        currency
        tiers { nodes { stats { totalAmountReceived { value currency } } contributors { totalCount nodes { totalAmountDonated } } currency orders { totalCount } contributors { nodes { id } } goal { value currency } id name amount { value } } }
      }
    }
    '''

    # Define the API endpoint
    url = 'https://api.opencollective.com/graphql/v2'

    # Send the GraphQL request
    response = requests.post(url, json={'query': query})

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        # Access the relevant data
        project_data = data['data']['project']

        # Return project data
        return {
            "name": project_data['name'],
            "slug": project_data['slug'],
            "currency": project_data['currency'],
            "goal_amount": project_data['tiers']['nodes'][0]['goal']['value'],
            "total_amount_received": project_data['tiers']['nodes'][0]['stats']['totalAmountReceived']['value']
            # Access more fields as needed
        }
    else:
        print("Error:", response.status_code)
        return None


def draw_text_with_shadow(draw, text, position, font, text_color, shadow_color, shadow_offset):
    # Draw shadow text
    shadow_position = (position[0] + shadow_offset[0], position[1] + shadow_offset[1])
    draw.text(shadow_position, text, fill=shadow_color, font=font)

    # Apply blur filter to the shadow
    shadow_img = Image.new('RGBA', draw.im.size, (255, 255, 255, 0))
    shadow_draw = ImageDraw.Draw(shadow_img)
    shadow_draw.text(shadow_position, text, fill=shadow_color, font=font)
    shadow_img_blur = shadow_img.filter(ImageFilter.GaussianBlur(5))

    # Paste the blurred shadow onto the original image
    draw.bitmap((0, 0), shadow_img_blur, fill=shadow_color)

    # Draw actual text on top of the shadow
    draw.text(position, text, fill=text_color, font=font)

def draw_project_info(draw, project_info, font):
    text_color = (218, 198, 184)  # Default text color
    shadow_color = (0, 0, 0)  # Shadow color
    shadow_offset = (2, 2)  # Offset for the shadow
    red_color = (232,220,212)  # Red color for specific parts

    # Draw total amount received
    total_amount_text = f"Received donations: "
    draw_text_with_shadow(draw, total_amount_text, (28, 36), font, text_color, shadow_color, shadow_offset)

    # Draw total amount received value in red
    total_amount_received = f"{project_info['total_amount_received']} Eur"
    draw_text_with_shadow(draw, total_amount_received, (28 + draw.textsize(total_amount_text, font=font)[0], 36), font, red_color, shadow_color, shadow_offset)

    # Draw goal amount
    goal_amount_text = f"To keep for next year: "
    draw_text_with_shadow(draw, goal_amount_text, (28, 56), font, text_color, shadow_color, shadow_offset)

    # Draw goal amount value in red
    goal_amount_value = f"{project_info['goal_amount']} Eur"
    draw_text_with_shadow(draw, goal_amount_value, (28 + draw.textsize(goal_amount_text, font=font)[0], 56), font, red_color, shadow_color, shadow_offset)

    # Draw project name
    # project_name_text = f"Project Name: "
    # draw_text_with_shadow(draw, project_name_text, (28, 76), font, text_color, shadow_color, shadow_offset)

    # Draw project name value in red
    # project_name_value = f"{project_info['name']}"
    # draw_text_with_shadow(draw, project_name_value, (28 + draw.textsize(project_name_text, font=font)[0], 76), font, red_color, shadow_color, shadow_offset)

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"Hello, world!")
        elif self.path == '/image.png':
            project_info = get_project_info()
            if project_info:
                print("Project Name:", project_info['name'])
                print("Project Slug:", project_info['slug'])
                print("Currency:", project_info['currency'])
                print("Goal Amount:", project_info['goal_amount'])
                print("Total Amount Received:", project_info['total_amount_received'])

            # Open an Image
            img = Image.open('image.png')

            # Call draw Method to add 2D graphics in an image
            draw = ImageDraw.Draw(img)
            font = ImageFont.truetype("Roboto-Medium.ttf", 18)

            # Draw project information
            draw_project_info(draw, project_info, font)

            # Save the edited image
            img.save("image2.png")

            self.send_response(200)
            self.send_header('Content-type', 'image/png')
            self.end_headers()
            # Open the image file
            with open('image2.png', 'rb') as f:
                img_data = f.read()
            self.wfile.write(img_data)
        else:
            self.send_error(404, 'File Not Found: %s' % self.path)

def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8001):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Server running on port {port}")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
