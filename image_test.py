from PIL import Image

try:
    filename = '4.png'
    image = Image.open(filename)
    image.thumbnail((240, 240), Image.ANTIALIAS)
    image.save('small_'+filename,  quality=100)
except IOError:
    print "cannot create thumbnail for "
