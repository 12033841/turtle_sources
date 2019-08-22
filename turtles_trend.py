import turtle
import random
import math


class HeatSource(turtle.Turtle):

    def __init__(self):
        turtle.Turtle.__init__(self, visible=False)
        self.shape('circle')
        self.penup()
        self.color(255, 190, 60)
        self.goto(random.randint(-200, 200), random.randint(-200, 200))
        self.showturtle()


class Vehicle(turtle.Turtle):

    def __init__(self, heat_list, vehicle_id, vehicle_type):
        turtle.Turtle.__init__(self, visible=False)
        self.vehicle_id = vehicle_id
        self.vehicle_type = vehicle_type
        self.heat_list = heat_list
        self.create_vehicle()
        self.speed_parameters = [20, 0.2, 6]
        self.turn_parameters = [20]


    def create_vehicle(self):
        self.shape('turtle')
        self.turtlesize(1)
        self.penup()
        if self.vehicle_type == 'crossed':
            self.color(random.randint(0, 150), random.randint(0, 150), 255)
        else:
            self.color(255, random.randint(0, 150), random.randint(0, 150))
        self.goto(random.randint(-290, 290), random.randint(-290, 290))
        self.right(random.randint(0, 360))
        self.pendown()
        self.showturtle()


    def get_input_information(self, position):
        input_distance = self.distance(position)
        input_angle = self.heading() - self.towards(position)
        return input_distance, input_angle


    def get_sensor_distances(self, distance, angle):
        sin_angle = math.sin(math.radians(angle))
        left_distance = distance - sin_angle
        right_distance = distance + sin_angle
        return left_distance, right_distance


    def compute_speed(self, left_distance, right_distance):
        if self.vehicle_type == 'crossed':
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

            for current_input in self.heat_list:
                input_distance, input_angle = self.get_input_information(current_input.position())
                left_distance, right_distance = self.get_sensor_distances(input_distance, input_angle)
                left_speed, right_speed, average_speed = self.compute_speed(left_distance, right_distance)
                turn_amount = self.compute_turn_amount(left_speed, right_speed)
                combined_turn_amount += turn_amount
                combined_speed += average_speed
            print(self.position())
            print(self.heading())

            if self.ycor() <= -370:
                if self.heading() >= 0 and self.heading() <= 180:
                    turn_angle = 180 - self.heading()
                    self.setheading(turn_angle)
                else:
                    turn_angle = abs(360 - self.heading())
                    self.setheading(turn_angle)
            if self.ycor() >= 380:
                if self.heading() >= 0 and self.heading() <= 180:
                    turn_angle = 360 - self.heading()
                    self.setheading(turn_angle)
                else:
                    turn_angle = 360 - (self.heading() - 180)
                    self.setheading(turn_angle)
            if self.xcor() <= -580:
                if self.heading() >= 0 and self.heading() <= 90:
                    turn_angle = 360 - self.heading()
                    self.setheading(turn_angle)
                if self.heading() >= 270 and self.heading() < 360:
                    turn_angle = 360 - self.heading()
                    self.setheading(turn_angle)
                if self.heading() > 90 and self.heading() < 180:
                    turn_angle = self.heading() - 90
                    self.setheading(turn_angle)
                if self.heading() >= 180 and self.heading() < 360:
                    turn_angle = self.heading() + 90
                    self.setheading(turn_angle)
            if self.xcor() >= 580:
                if self.heading() >= 0 and self.heading() <= 180:
                    turn_angle = self.heading() + 90
                    self.setheading(turn_angle)
                else:
                    turn_angle = self.heading() - 90
                    self.setheading(turn_angle)

            try:
                self.right(combined_turn_amount)
            except:
                print(combined_turn_amount)
            self.forward(combined_speed)


def create_screen():
    wn = turtle.Screen()
    wn.colormode(255)
    wn.setup(1200, 800)
    wn.title("Turtles")
    wn.tracer(0, 0)
    return wn


def main():
    wn = create_screen()
    num_vehicles = 5
    num_heat_sources = 5

    vehicle_list = []
    heat_list = []

    for i in range(num_heat_sources):
        heat_list.append(HeatSource())

    for i in range(num_vehicles):
        vehicle_list.append(Vehicle(heat_list, i, random.choice(["crossed", "direct"])))

    wn.update()
    # start == False
    # while start == True:
    while True:
        for j in range(num_vehicles):
            vehicle_list[j].move()
        wn.update()

main()