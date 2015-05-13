import numpy as np
import scipy as sp
import random
from operator import itemgetter
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class Penguin(object):

	def __init__(self, radius, position, alignment):
		"""
		Arguments:
			radius		:=	float representing penguin radius
			position	:=	numpy array representing penguin position (x, y, z)
			alignment	:=	numpy array representing alignment unit vector
			boundary	:=	boolean value, True if boundary penguin, False if bulk penguin
		"""

		self.radius = radius
		self.position = position
		self.alignment = alignment
		self.boundary = False
		self.bisection_angle = 0
		self.bisector = np.zeros(3)

	def __str__(self):

		return "Penguin located at ({}, {})".format(self.position[0], self.position[1])

	def __repr__(self):

		return self.__str__()

	def get_distance(self, penguin2):

		return self.position - penguin2.position

	def update_position(self, position):

		self.position = position

	def update_alignment(self, alignment):

		self.alignment = alignment


	# def determine_boundary_condition(self, penguin_list, a):

	# 	critical_radius = 2.0 * a

	# 	theta_list = []

	# 	for i in range(len(penguin_list)):

	# 		if (penguin_list[i] != self):

	# 			r = self.get_distance(penguin_list[i])
	# 			r_mag = np.linalg.norm(r)

	# 			if (r_mag < critical_radius):

	# 				theta = np.arctan2(r[1],r[0])
	# 				theta_list.append(theta)

	# 	theta_list.sort()

	# 	for j in range(len(theta_list)):

	# 		try:

	# 			difference = theta_list[j+1] - theta_list[j]

	# 		except IndexError:

	# 			difference =  (np.pi - theta_list[j]) + (theta_list[0] + np.pi)

	# 		# print(difference * 180 / np.pi)

	# 		if (difference >= np.pi):

	# 			self.boundary = True

	# 			return True

	# 		else:

	# 			self.boundary = False

	def find_exterior_bisector(self, penguin_list, a):

		critical_radius = 1.5 * a

		r_theta_list = []

		for i in range(len(penguin_list)):

			if (penguin_list[i] != self):

				r = self.get_distance(penguin_list[i])
				r_mag = np.linalg.norm(r)

				if (r_mag < critical_radius):

					theta = np.arctan2(r[1],r[0])
					r_theta_list.append([r,theta])

		r_theta_list = sorted(r_theta_list, key=itemgetter(1))

		for j in range(len(r_theta_list)):

			try:

				a = j
				b = j+1
				difference = r_theta_list[b][1] - r_theta_list[a][1]

			except IndexError:

				a = 0
				b = j
				difference =  (np.pi - r_theta_list[b][1]) + (r_theta_list[a][1] + np.pi)

			if (difference >= np.pi):

				self.boundary = True
				self.bisection_angle = difference

				exterior_bisector = -1.0 * (r_theta_list[a][0] + r_theta_list[b][0])

				angle1 = np.arctan2(r_theta_list[a][0][1], r_theta_list[a][0][0]) * 180 / np.pi
				angle2 = np.arctan2(r_theta_list[b][0][1], r_theta_list[b][0][0]) * 180 / np.pi

				# bisector_angle = (angle1 + angle2) / 2.0

				# exterior_bisector = np.array([np.cos(bisector_angle), np.sin(bisector_angle)])

				if (exterior_bisector[0] == 0) and (exterior_bisector[1] == 0):

					if (angle1 == 0) and (angle2 == 180):

						exterior_bisector = np.array([0.0,-1.0])

					if (angle1 == 180) and (angle2 == 0):

						exterior_bisector = np.array([0.0,1.0])

					if (angle1 == 90) and (angle2 == -90):

						exterior_bisector = np.array([-1.0,0.0])

					if (angle1 == -90) and (angle2 == 90):

						exterior_bisector = np.array([1.0,0.0])

				self.bisector = exterior_bisector					

				# return exterior_bisector

				break

			else:

				self.boundary = False


	def find_net_force(self, F_self, F_in, k, penguin_list, a):

		critical_radius = 1.3 * a

		F_self_propulsion = F_self * self.alignment

		F_repulsion = np.zeros(2) 

		for i in range(len(penguin_list)):

			if (penguin_list[i] != self):

				if (self.boundary == True):

					F_boundary = F_in * self.alignment * (self.bisection_angle - np.pi)

				else:

					F_boundary = 0

				r = self.get_distance(penguin_list[i])
				r_mag = np.linalg.norm(r)

				# print i 
				# print r_mag
				# print critical_radius
				if (r_mag < critical_radius):

					# print r
					F_repulsion += -k * r

		return F_self_propulsion + F_boundary  + F_repulsion

	def find_net_torque(self, T_in, T_noise, T_align, penguin_list, a):

		critical_radius = 1.3 * a

		if (self.boundary == True):

			T_boundary = T_in * (self.alignment - self.bisector)

		else:

			T_boundary = 0

		eta = random.uniform(-1.0,1.0)

		T_random = T_noise * eta

		T_alignment = np.zeros(2)

		for i in range(len(penguin_list)):

			if (penguin_list[i] != self):

				r = self.get_distance(penguin_list[i])
				r_mag = np.linalg.norm(r)

				if (r_mag < critical_radius):

					T_alignment += T_align * (self.alignment - penguin_list[i].alignment)

		return T_boundary + T_random + T_alignment


def move_penguins(penguin_list, a):

	F_self = 1.0
	F_in = 1.0
	k = 1.0
	T_in = 1.0
	T_noise = 1.0
	T_align = 1.0

	t_start = 0.01
	t_end = 1.0
	t_iter = 0.01

	mass = 1.0

	while t_start < t_end:

		for i in range(len(penguin_list)):

			penguin = penguin_list[i]
			force = penguin.find_net_force(F_self, F_in, k, penguin_list, a)
			torque = penguin.find_net_torque(T_in, T_noise, T_align, penguin_list, a)

			I = (2.0 / 5.0) * mass * penguin.radius ** 2.0
			alpha = torque / I

			acceleration = force / mass

			new_position = penguin.position + acceleration * t_iter
			new_alignment = penguin.alignment + alpha * t_iter

			penguin.update_position(new_position)
			penguin.update_alignment(new_alignment)

			penguin.find_exterior_bisector(penguin_list, a)


		print t_start
		t_start += t_iter



a = 1.0
penguin_list = []

for i in range(5):
	for j in range(5):

			x = i + random.uniform(-0.2,0.2)
			y = j + random.uniform(-0.2,0.2)

			radius = a

			position = np.array([x,y])

			alignment = np.array([1,1])

			penguin = Penguin(a, position, alignment)
			penguin_list.append(penguin)

# penguin1 = Penguin(a, np.array([-0.5,0]), np.array([1,1]))
# penguin2 = Penguin(a, np.array([0.5,0]), np.array([1,1]))
# penguin3 = Penguin(a, np.array([0,-0.5]), np.array([1,1]))
# penguin4 = Penguin(a, np.array([0,0.5]), np.array([1,1]))
# penguin5 = Penguin(a, np.array([0,0]), np.array([1,1]))

# penguin_list.append(penguin1)
# penguin_list.append(penguin2)
# penguin_list.append(penguin3)
# penguin_list.append(penguin4)
# penguin_list.append(penguin5)

# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')

for penguin in penguin_list:

	# print penguin

	penguin.find_exterior_bisector(penguin_list, a)

	# print exterior_bisector

	# print penguin.boundary

	# print penguin.find_net_force(1.0,1.0,1,penguin_list,1.0)
	# print penguin.find_net_torque(1.0,1.0,1.0,penguin_list,1.0)

	if penguin.boundary == True:

		plt.plot(penguin.position[0], penguin.position[1], "ro")

	else:

		plt.plot(penguin.position[0], penguin.position[1], "bo")



# plt.xlim([-1,5])
# plt.ylim([-1,5])
plt.show()

plt.clf()

move_penguins(penguin_list, a)

for penguin in penguin_list:

	# print penguin

	penguin.find_exterior_bisector(penguin_list, a)

	# print exterior_bisector

	# print penguin.boundary

	# print penguin.find_net_force(1.0,1.0,1,penguin_list,1.0)
	# print penguin.find_net_torque(1.0,1.0,1.0,penguin_list,1.0)

	if penguin.boundary == True:

		plt.plot(penguin.position[0], penguin.position[1], "ro")

	else:

		plt.plot(penguin.position[0], penguin.position[1], "bo")

plt.show()















