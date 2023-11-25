#This is the main page I am going to use for the Project 2 code

#import the necessary packages 
from astropy.io import fits 
from astropy.wcs import WCS 
import numpy as np 
import matplotlib.pyplot as plt
from astropy.visualization import make_lupton_rgb
from matplotlib.colors import LogNorm 


#Call a function to scale the data 

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





