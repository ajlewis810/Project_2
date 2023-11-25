#This is the main page I am going to use for the Project 2 code

#import the necessary packages 
from astropy.io import fits 
from astropy.wcs import WCS 
import numpy as np 
import matplotlib.pyplot as plt
from astropy.visualization import make_lupton_rgb
from matplotlib.colors import LogNorm 
from astroquery.vizier import Vizier
import astropy.units as u
from astropy.coordinates import SkyCoord




#Call a function to scale the data, using the .5 and 99.5 as in DS9 so that the image is much bighter.  



def scale_data(data): 
	p_low, p_high = np.percentile(data, [.5, 99.5])
	data = np.clip(data, p_low, p_high)
	data = data - p_low  # Shift the scale to start from 0
	data = data / (p_high - p_low)  # Scale the data to run from 0 to 1
	return data


#Now open the fits files and extract the necessaryr data 

red = fits.open('h_udf_wfc_i_drz_img.fits') 
green = fits.open('h_udf_wfc_v_drz_img.fits')
blue =  fits.open('h_udf_wfc_b_drz_img.fits')



red_data = red[0].data
blue_data = blue[0].data
green_data = green[0].data


red_scaled = scale_data(red_data)
green_scaled = scale_data(green_data)
blue_scaled = scale_data(blue_data)



RGB = make_lupton_rgb(red_scaled, green_scaled, blue_scaled, stretch = 7, Q= 4.5)


wcs = WCS(red[0].header)

red.close()
blue.close()
green.close()



fig = plt.figure(figsize = (10,10))
ax = fig.add_subplot(1, 1, 1, projection = wcs)
ax.imshow(RGB, origin = 'lower')


ax.set_xlabel("RA")
ax.set_ylabel("DEC")

ax.grid(color = 'white', ls = 'dashed', lw = .1)
plt.show()

#Ok so now we have the color graph now we need to do the second part of the assignemnt. 


phot_table = fits.open('asu.fit')
phot_data = phot_table[1].data


phot_coords = SkyCoord(ra = phot_data['RAJ2000'], dec = phot_data['DEJ2000'], unit = (u.deg, u.deg))

x1,y1 = wcs.world_to_pixel(phot_coords)
ax.scatter(x1,y1,s=5,marker='x',color = 'red', alpha=0.1, label = "Photmetric RedShift")

spec_table = fits.open('asus.fit')
spec_data = spec_table[1].data
spec_coords = SkyCoord(ra = spec_data['RAJ2000'], dec = spec_data['DEJ2000'], unit = (u.deg, u.deg))


x2,y2 = wcs.world_to_pixel(spec_coords)

ax.scatter(x2, y2, s=5, marker = 'x', color = 'green', alpha = 1, label = "spectrooscopic redshif")

ax.legend()
plt.show()

#We now have the spec and phot redshifts represented in the HuDF images.














 




