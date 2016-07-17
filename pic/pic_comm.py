from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import render
from PIL import Image
import pdb


class Common():
    def resize_img(self,imgfile, percent_x=240, percent_y=240,q=100): 
        try:
            imgfile = '40.png'
            image = Image.open(imgfile)
            image.thumbnail((percent_x, percent_y), Image.ANTIALIAS)
            image.save('sml_'+imgfile,  quality=q)
            return True
        except IOError:
            return False

    
   
