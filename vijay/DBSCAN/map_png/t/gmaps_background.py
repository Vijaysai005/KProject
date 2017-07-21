from PIL import Image
import matplotlib.pyplot as plt

import urllib


url = "http://maps.googleapis.com/maps/api/staticmap?center=18.027489,74.229248&size=800x800&zoom=10&sensor=true"

gmap_static_file = urllib.request.urlopen(url)

with open('./gmap_static.png','wb') as output:
  output.write(gmap_static_file.read())

plt.figure(1)     
ax = plt.subplot(111)

im = plt.imread('./gmap_static.png')
plt.plot(74.229,18.027,"r.", MarkerSize=15)

# ax.set_xticks([i for i in range(0,800,2)]) #python3 code to create 90 tick marks
# ax.set_xticklabels([-i for i in range(-400,400,2)]) #python3 code to create 90 labels

plt.imshow(im, extent=[18.027489-10**-6,18.027489+10**-6,74.229248-10**-6,74.229248+10**-6], aspect='auto')

plt.show()
