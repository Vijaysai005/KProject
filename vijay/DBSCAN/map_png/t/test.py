import matplotlib.pyplot as plt
im = plt.imread('test.png')
implot = plt.imshow(im)
plt.plot([100,200,300],[200,150,200],'o')
plt.show()