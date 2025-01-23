from time import *
import board
import neopixel

NUM_PIXELS = 30
pixelsl = neopixel.NeoPixel(board.D18, NUM_PIXELS, brightness=0.05)
 
x = 0 
 
pixelsl.fill((255, 255,255))
while True:
	for i in range(NUM_PIXELS-1):
		pixelsl[i] = (255,255,255)
		sleep(0.05)
		pixelsl[i+1] = (255,255,255)

		pixelsl[i] = (0,0,0)
		pixelsl[i+1] = (0,0,0)

		sleep(0.05)
	
print("run!")
