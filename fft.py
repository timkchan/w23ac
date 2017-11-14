# fft.py
# Author: Tim K. Chan
# Email: me@timkchan.com
# Created: 16/10/2017

import scipy.fftpack as fp
import matplotlib.pyplot as plt
import skimage.io as skio
import numpy as np

## Functions to go from image to frequency-image and back
im2freq = lambda data: fp.rfft(fp.rfft(data, axis=0), axis=1)
freq2im = lambda f: fp.irfft(fp.irfft(f, axis=1), axis=0)

## Read in data file in grey scale
data = skio.imread('moon.jpg', as_grey=True)
temp = np.log(np.abs(np.fft.fftshift(np.fft.fft2(data))))
plt.imshow(temp)
plt.show()
#######################################################
#######################################################
# Encode

## Transform data to frequency domain
freq = im2freq(data)
print(freq)
## Salt secret
secret = '010101000110100101101101'
freq[0][0] = len(secret) # First index stores number of bites

# Salting: Put each bit in each subsequent 'pixel'
for i in range(len(secret)):
    freq[0][i + 1] = int(secret[i])

# Convert salted frequency domain data into grey scale image
back = freq2im(freq)
print()
# Show and save slated image
plt.imsave('moon_salted.jpg', back)
plt.imshow(back, cmap='gray')
plt.show()

#######################################################
#######################################################
# Decode

## Read in data file in grey scale
data_sated = skio.imread('moon_salted.jpg', as_grey=True)

# Decode image by going back to frequency domain
freq2 = im2freq(data_sated)

# Extract len of bit to be read
lenOfSecret = int(freq2[0][0])

# Extract salts
msg = freq[0][1:lenOfSecret]

# Format message
msg = ''.join([str(int(i)) for i in msg])
at = msg.index('-')
msg = msg[:at]
print(msg)

# Make sure the forward and backward transforms work!
# assert(np.allclose(data, back))

# Binary <=> ASCII
# http://www.rapidtables.com/convert/number/binary-to-ascii.htm
