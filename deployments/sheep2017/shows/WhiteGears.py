#
# WhiteGears
#
# 2 pinwheel gears plus a drive chain
# 
# Touch OSC controls speed and direction of gears
# 

import sheep
import time
from math import sin, pi
from random import randint, choice
from color import RGB, HSV            

# Darkens a color by a 0.0 - 1.0 gradient
def gradient_color(color, fade_value):
	# Check limits
	if fade_value < 0: fade_value = 0
	if fade_value > 1: fade_value = 1
			   
	return RGB(color.r * fade_value,
				color.g * fade_value,
				color.b * fade_value)

class Gear(object):
	def __init__(self, sheep, trajectory):
		self.sheep = sheep
		self.trajectory = trajectory
		self.pos = 0
		self.max = len(self.trajectory)
	
	def draw_gear(self, color):
		for c in range(self.max):
			intensity = (sin (((c + self.pos) % self.max) * 2 * pi / (self.max - 1)) + 1) / 2.0
			intensity = intensity * intensity	# squaring magnifies differences
			self.sheep.set_cell(self.trajectory[c], gradient_color(color, intensity))

	def move_gear(self, dir):
		self.pos += dir
		if self.pos < 0:
			self.pos = self.max - 1
		if self.pos >= self.max:
			self.pos = 0
			
class WhiteGears(object):
	def __init__(self, sheep_sides):
		self.name = "WhiteGears"
		self.sheep = sheep_sides.both		
		self.rate_min = 1
		self.rate_max = 10
		self.rate = randint(self.rate_min, self.rate_max)
		self.eqlizer = [0,0,0]	# Random initial values
	
		self.speed = 0.02
		
		self.gear_color = RGB(255,255,255)
		self.chain_color = RGB(255,255,255)
		
		self.last_osc = time.time()
		self.OSC = False	# Is Touch OSC working?
		
		self.REAR_SPIRAL = [24,32,35,36,33,26,25]
		self.CHAIN = [39,40,41,42,43,37,34,30,31,22,23,3,2,1,5,6,12,11,15,19]
		
		self.gears = {}
		
		new_gear = Gear(self.sheep, sheep.FRONT_SPIRAL)
		self.gears['FRONT'] = new_gear

		new_gear = Gear(self.sheep, self.REAR_SPIRAL)
		self.gears['REAR'] = new_gear
		
		new_gear = Gear(self.sheep, self.CHAIN)
		self.gears['CHAIN'] = new_gear

	def set_param(self, name, val):
		# name will be 'colorR', 'colorG', 'colorB'
		rgb255 = int(val * 0xff)
		if name == 'colorR':
			self.rate = (rgb255 * self.rate_max * 2 / 255) - (self.rate_max)
			self.last_osc = time.time()
			self.OSC = True
					
	def next_frame(self):	
		while (True):
			
			# Fill in the background with black
			# Some times, flash white
			
			if randint(0,20) == 1:
				background = RGB(255,255,255)
			else:
				background = RGB(0,0,0)
			
			self.sheep.set_all_cells(background)
			
			# Draw the gears
			self.gears['FRONT'].draw_gear(self.gear_color)
			self.gears['REAR'].draw_gear(self.gear_color)
			self.gears['CHAIN'].draw_gear(self.chain_color)
			
			# Move the gears
			
			if self.rate > 0:
				dir = 1	# Forward
			else:
				dir = -1	# Backwards
			
			self.gears['FRONT'].move_gear(dir)
			self.gears['REAR'].move_gear(dir)
			self.gears['CHAIN'].move_gear(dir)
			
			# Randomly change speeds
			
			if time.time() - self.last_osc > 120:	# 2 minutes
				self.OSC == False
				
			if self.OSC == False:
				if randint(0,10) == 1:
					self.rate += randint(-1,1)
					if self.rate > self.rate_max:
						self.rate = self.rate_max
					if self.rate < -1 * self.rate_max:
						self.rate = -1 * self.rate_max
			yield (self.speed * (self.rate_max + 1 - abs(self.rate)))