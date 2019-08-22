import turtle
import tkinter as tk
from turtle import RawTurtle, TurtleScreen
import numpy as np
import random
import math
import time


class TurtleTrend:
	def __init__(self, wn, startFrame, stopFrame, resetFrame):
		self.wn = wn
		self.running = False

		self.num_turtles = 1
		self.num_heat_sources = 5
		self.turtle_list = []
		self.heat_list = []
		self.create_heatsource()

		self.speed_parameters = [20, 0.2, 6]
		self.turn_parameters = [20]
		self.create_turtles()

		self.start = tk.Button(startFrame, text = "start", fg = "black", command = self.start).pack()
		self.stop = tk.Button(stopFrame, text = "stop", fg = "black", command = self.stop).pack()
		self.reset = tk.Button(resetFrame, text = "reset", fg = "black", command = self.reset).pack()


	def reset(self):
		self.turtle_list.pop(0)
		self.wn.clear()
		# self.turtle_list[0].hideturtle()
		# self.turtle_list.pop(0)
		self.create_heatsource()
		self.create_turtles()


	def onclick_event(self, source):
		def onclick_hit(x, y):
			source.penup()
			source.goto(x, y)
			return

		self.wn.onclick(onclick_hit)
		return


	def create_heatsource(self):
		for i in range(self.num_heat_sources):
			heatsource = RawTurtle(self.wn)
			heatsource.shape('circle')
			heatsource.penup()
			heatsource.color("orange")
			heatsource.showturtle()
			heatsource.goto(random.randint(-290, 290), random.randint(-290, 290))
			time.sleep(2)
			self.onclick_event(heatsource)
			self.heat_list.append(heatsource)


	def create_turtles(self):
		for i in range(self.num_turtles):
			turtle = RawTurtle(self.wn)
			turtle.vehicle_id = i
			turtle.type = random.choice(["crossed", "direct"])
			turtle.shape('turtle')
			turtle.turtlesize(1)
			turtle.penup()
			if turtle.type == 'crossed':
				turtle.color("red", (1, 0.85, 0.85))
			else:
				turtle.color("blue", (0.85, 0.85, 1))
			turtle.goto(random.randint(-290, 290), random.randint(-290, 290))
			turtle.right(random.randint(0, 360))
			turtle.showturtle()
			time.sleep(2)
			self.onclick_event(turtle)
			self.turtle_list.append(turtle)


	def get_input_information(self, position, turtle):
		input_distance = turtle.distance(position)
		input_angle = turtle.heading() - turtle.towards(position)
		return input_distance, input_angle


	def get_sensor_distances(self, distance, angle):
		sin_angle = math.sin(math.radians(angle))
		left_distance = distance - sin_angle
		right_distance = distance + sin_angle
		return left_distance, right_distance


	def compute_speed(self, left_distance, right_distance, turtle):
		if turtle.type == 'crossed':
			left_speed = (self.speed_parameters[0] / (right_distance ** self.speed_parameters[1])) - self.speed_parameters[2]
			right_speed = (self.speed_parameters[0] / (left_distance ** self.speed_parameters[1])) - self.speed_parameters[2]
		else:
			left_speed = (self.speed_parameters[0] / (left_distance ** self.speed_parameters[1])) - self.speed_parameters[2]
			right_speed = (self.speed_parameters[0] / (right_distance ** self.speed_parameters[1])) - self.speed_parameters[2]

		combined_speed = (left_speed + right_speed) / 2

		return left_speed, right_speed, combined_speed


	def compute_turn_amount(self, left_speed, right_speed):
		turn_amount = self.turn_parameters[0] * (right_speed - left_speed)
		return turn_amount


	def move(self):
		combined_speed = 0
		combined_turn_amount = 0

		while self.running == True:
			for j in range(self.num_turtles):
				for current_input in self.heat_list:
					input_distance, input_angle = self.get_input_information(current_input.position(), self.turtle_list[j])
					left_distance, right_distance = self.get_sensor_distances(input_distance, input_angle)
					left_speed, right_speed, average_speed = self.compute_speed(left_distance, right_distance, self.turtle_list[j])
					turn_amount = self.compute_turn_amount(left_speed, right_speed)
					combined_turn_amount += turn_amount
					combined_speed += average_speed
					print(self.turtle_list[j].position())
					print(self.turtle_list[j].heading())

					if self.turtle_list[j].ycor() <= -330:
						if self.turtle_list[j].heading() >= 0 and self.turtle_list[j].heading() <= 180:
							turn_angle = 180 - self.turtle_list[j].heading()
							self.turtle_list[j].setheading(turn_angle)
						else:
							turn_angle = abs(360 - self.turtle_list[j].heading())
							self.turtle_list[j].setheading(turn_angle)
					if self.turtle_list[j].ycor() >= 330:
						if self.turtle_list[j].heading() >= 0 and self.turtle_list[j].heading() <= 180:
							turn_angle = 360 - self.turtle_list[j].heading()
							self.turtle_list[j].setheading(turn_angle)
						else:
							turn_angle = 360 - (self.turtle_list[j].heading() - 180)
							self.turtle_list[j].setheading(turn_angle)
					if self.turtle_list[j].xcor() <= -330:
						if self.turtle_list[j].heading() >= 0 and self.turtle_list[j].heading() <= 90:
							turn_angle = 360 - self.turtle_list[j].heading()
							self.turtle_list[j].setheading(turn_angle)
						if self.turtle_list[j].heading() >= 270 and self.turtle_list[j].heading() < 360:
							turn_angle = 360 - self.turtle_list[j].heading()
							self.turtle_list[j].setheading(turn_angle)
						if self.turtle_list[j].heading() > 90 and self.turtle_list[j].heading() < 180:
							turn_angle = self.turtle_list[j].heading() - 90
							self.turtle_list[j].setheading(turn_angle)
						if self.turtle_list[j].heading() >= 180 and self.turtle_list[j].heading() < 360:
							turn_angle = self.turtle_list[j].heading() + 90
							self.turtle_list[j].setheading(turn_angle)
					if self.turtle_list[j].xcor() >= 330:
						if self.turtle_list[j].heading() >= 0 and self.turtle_list[j].heading() <= 180:
							turn_angle = self.turtle_list[j].heading() + 90
							self.turtle_list[j].setheading(turn_angle)
						else:
							turn_angle = self.turtle_list[j].heading() - 90
							self.turtle_list[j].setheading(turn_angle)

					try:
						self.turtle_list[j].right(combined_turn_amount)
					except:
						print(combined_turn_amount)
					self.turtle_list[j].forward(combined_speed)


	def start(self):
		self.running = True
		self.move()


	def stop(self):
		self.running = False


def create_screen():
	root = tk.Tk()
	canvas = tk.Canvas(root, width = 700, height = 700)
	canvas.pack()
	wn = TurtleScreen(canvas)
	return wn, root


def create_buttons(root):
	startFrame = tk.Frame(root)
	startFrame.pack()

	stopFrame = tk.Frame(root)
	stopFrame.pack()

	resetFrame = tk.Frame(root)
	resetFrame.pack()

	return startFrame, stopFrame, resetFrame


def main():
	wn, root = create_screen()
	startFrame, stopFrame, resetFrame = create_buttons(root)
	TurtleTrend(wn, startFrame, stopFrame, resetFrame)
	wn.mainloop()


main()