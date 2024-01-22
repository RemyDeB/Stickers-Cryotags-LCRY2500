# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 14:56:51 2023

@author: remy.de-boni
"""

import requests
from bs4 import BeautifulSoup
from fpdf import FPDF
from datetime import datetime
import os
# Get the current date and time
current_date_time = datetime.now().strftime("%Y-%m")



def load_CID(file):
    
    with open(file, "r", encoding="unicode_escape") as file:
        CID_list = list(filter(None, (line.rstrip() for line in file)))
    return(CID_list)

def download_image(CID_list):

    for CID in CID_list:
        # Construct the URL for the chemical search
        search_url = 'https://pubchem.ncbi.nlm.nih.gov/image/imgsrv.fcgi?cid=' + str(CID)+"&t=l"
        print(f"Searching for: {CID}")

        # Make a request to the search URL
        search_response = requests.get(search_url)

        if search_response.status_code == 200:
            # Parse the HTML content using BeautifulSoup
                    image_path = os.path.join("image", f"{CID}.png")
                    with open(image_path, 'wb') as file:
                        file.write(search_response.content)
                        print('Image downloaded successfully.')
        else:
             print(f'Failed to download image. Status code: {search_response.status_code} \n Verify CID: {CID}')


# Example usage

def Print_Cell(x,y):
    pdf.set_xy(x,y)
    pdf.cell(2.5,0.5,border=1)

def Create_sticker(x,y,n):
#Image
    pdf.set_xy(x,y)
    image_path = os.path.join("image", CID_list[n] + ".png")
    pdf.image(image_path,w=0.5,h=0.5)
    
    
    pdf.set_xy(x+0.5,y)
    pdf.cell(2,0.5/4, text ="Solvant:")

    

    #CID
    pdf.set_xy(x+0.5,y+0.5/4)
    pdf.cell(2,0.5/4, text ="CID: "+CID_list[n])

    #DATE
    pdf.set_xy(x+0.5,y+2*0.5/4)
    pdf.cell(2,0.5/4, text ="DATE: "+str(current_date_time))
    
    #position 
    #rangement 
    pdf.set_xy(x+1.25,y+2*0.5/4)
    pdf.cell(2,0.5/4, text ="position ID:")
   

    #ppm
    pdf.set_xy(x+0.5,y+3*0.5/4-0.025)
    pdf.cell(2,0.5/4, text ="ppm:")
    
    


x_pos = [0.47,2.97,5.47] #inch 
y_pos = [0.5,1,1.5,2,2.5,3,3.5,4,4.5,5,5.5,6,6.5,7,7.5,8,8.5,9,9.5,10] #inch
file ="CIDlist.txt"
CID_list = load_CID(file)
download_image(CID_list)



value = len(CID_list)
if value > 60:
    value = 60
    print("print only first 60 compounds")
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
                Create_sticker(x+0.1,y,n)
                n+=1
               

"""
for y in y_pos:
    for x in x_pos:
        Print_Cell(x,y)
"""


pdf.output("new1.pdf")

