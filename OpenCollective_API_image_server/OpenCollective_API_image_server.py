# http://localhost:8001/image.png

from http.server import HTTPServer, BaseHTTPRequestHandler
from PIL import Image
from io import BytesIO

# Importing the PIL library
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
 

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
            I1 = ImageDraw.Draw(img)
             
            # Add Text to an image 
            I1.text((28, 36),  "Received donations total overall: ", fill=(255, 0, 0), font=ImageFont.truetype("Roboto-Medium.ttf", 18))
            I1.text((300, 36),  str(project_info['total_amount_received']) + " Eur", fill=(200, 0, 0), font=ImageFont.truetype("Roboto-Medium.ttf", 18))
            I1.text((28, 56),  "Required to exist for a year: " + str(project_info['goal_amount']) + " Eur", fill=(255, 0, 0), font=ImageFont.truetype("Roboto-Medium.ttf", 18))
            I1.text((28, 76),  "Required overall for Upgrade: " + "200" + " Eur", fill=(255, 0, 0), font=ImageFont.truetype("Roboto-Medium.ttf", 18))
             
            # Display edited image
            #img.show()
             
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
