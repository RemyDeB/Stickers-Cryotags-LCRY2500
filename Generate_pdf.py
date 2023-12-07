# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 14:56:51 2023

@author: remy.de-boni
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from fpdf import FPDF
from datetime import datetime
import os
# Get the current date and time
current_date_time = datetime.now().strftime("%Y-%m-%d")



def load_CAS(file):
    
    with open(file, "r", encoding="unicode_escape") as file:
        names_list = list(filter(None, (line.rstrip() for line in file)))
    return(names_list)

def download_image(names_list):
    list_name = []

    for name in names_list:
        # Construct the URL for the chemical search
        search_url = 'https://www.chemspider.com/Search.aspx?q=' + str(name)
        print(f"Searching for: {name}")

        # Make a request to the search URL
        search_response = requests.get(search_url)

        if search_response.status_code == 200:
            # Parse the HTML content using BeautifulSoup
            try:
                soup = BeautifulSoup(search_response.text, 'html.parser')

                # Extract the name
                extracted_name = soup.find('span', {'id': 'ctl00_ctl00_ContentSection_ContentPlaceHolder1_RecordViewDetails_rptDetailsView_ctl00_WrapTitle'}).text.strip()
                list_name.append(extracted_name)

                # Find the img tag with the specified ID
                img_tag = soup.find('img', {'id': 'ctl00_ctl00_ContentSection_ContentPlaceHolder1_RecordViewDetails_rptDetailsView_ctl00_ThumbnailControl1_viewMolecule'})
                # Extract the source (src) attribute of the img tag
                relative_image_url = img_tag['src']

                # Create an absolute URL based on the base URL of the page
                absolute_image_url = urljoin("https://www.chemspider.com", relative_image_url)

                # Make a request to the absolute image URL
                image_response = requests.get(absolute_image_url)

                # Check if the image request was successful (status code 200)
                if image_response.status_code == 200:
                    # Save the image to a file
                    image_path = os.path.join("image", f"{name}.jpg")
                    with open(image_path, 'wb') as file:
                        file.write(image_response.content)
                        print('Image downloaded successfully.')
                else:
                    print(f'Failed to download image. Status code: {image_response.status_code}')

            except Exception as e:
                print(f'Error parsing search response: {e}')

                # If the initial search fails, try the multiple search
                print("Trying multiple search for this CAS")
                soup = BeautifulSoup(search_response.text, 'html.parser')

                first_link = soup.find('tbody').find('tr').find('td').find('a')

                if first_link:
                    url = first_link['href']

                    # Make a request to the selected URL
                    response = requests.get('https://www.chemspider.com' + url)

                    if response.status_code == 200:
                        # Parse the HTML content using BeautifulSoup
                        try:
                            soup = BeautifulSoup(response.text, 'html.parser')

                            # Extract the name
                            extracted_name = soup.find('span', {'id': 'ctl00_ctl00_ContentSection_ContentPlaceHolder1_RecordViewDetails_rptDetailsView_ctl00_WrapTitle'}).text.strip()
                            list_name.append(extracted_name)

                            # Find the img tag with the specified ID
                            img_tag = soup.find('img', {'id': 'ctl00_ctl00_ContentSection_ContentPlaceHolder1_RecordViewDetails_rptDetailsView_ctl00_ThumbnailControl1_viewMolecule'})
                            # Extract the source (src) attribute of the img tag
                            relative_image_url = img_tag['src']

                            # Create an absolute URL based on the base URL of the page
                            absolute_image_url = urljoin("https://www.chemspider.com", relative_image_url)

                            # Make a request to the absolute image URL
                            image_response = requests.get(absolute_image_url)

                            # Check if the image request was successful (status code 200)
                            if image_response.status_code == 200:
                                # Save the image to a file
                                image_path = os.path.join("image", f"{name}.jpg")
                                with open(image_path, 'wb') as file:
                                    file.write(image_response.content)
                                    print('Image downloaded successfully.')
                            else:
                                print(f'Failed to download image. Status code: {image_response.status_code}')

                        except Exception as e:
                            print(f'Error parsing response: {e}')
                    else:
                        print(f'Failed to make request to multiple search URL. Status code: {response.status_code}')

    return list_name

# Example usage

def Print_Cell(x,y):
    pdf.set_xy(x,y)
    pdf.cell(2.5,0.5,border=1)

def Create_sticker(x,y,n):
#Image
    pdf.set_xy(x,y)
    image_path = os.path.join("image", CAS_list[n] + ".jpg")
    pdf.image(image_path,w=0.5,h=0.5)
    
    
    pdf.set_xy(x+0.5,y)
    pdf.cell(2,0.5/4, text ="Solvant:")

    

    #CAS
    pdf.set_xy(x+0.5,y+0.5/4)
    pdf.cell(2,0.5/4, text ="CAS: "+CAS_list[n])

    #DATE
    pdf.set_xy(x+0.5,y+2*0.5/4)
    pdf.cell(2,0.5/4, text ="DATE: "+str(current_date_time))

    #ppm
    pdf.set_xy(x+0.5,y+3*0.5/4)
    pdf.cell(2,0.5/4, text ="ppm:")

x_pos = [0.47,2.97,5.47] #inch 
y_pos = [0.5,1,1.5,2,2.5,3,3.5,4,4.5,5,5.5,6,6.5,7,7.5,8,8.5,9,9.5,10] #inch
file ="CAS_list.txt"
CAS_list = load_CAS(file)
#name_molecule = download_image(CAS_list)



value = len(CAS_list)
if value > 60:
    value = 60
skip = 0
n=0
compteur =0
print(value)
#Creation PDF
pdf = FPDF(orientation="P",unit="in",format="letter")

pdf.set_font("Times", size=8)
pdf.set_auto_page_break(auto= False, margin = 0.0)
pdf.add_page()
pdf.set_margins(left = 0,top = 0 , right = 0)

while n < value: 
    for y in y_pos:
        for x in x_pos:
            compteur +=1
            print(compteur,n)
            if n == value:
                break
            if compteur>=skip:
                Create_sticker(x+0.3,y,n)
                n+=1
               

"""
for y in y_pos:
    for x in x_pos:
        Print_Cell(x,y)

"""

pdf.output("new1.pdf")

