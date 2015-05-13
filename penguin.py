import numpy as np
import scipy as sp
import random
from operator import itemgetter

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

	def __str__(self):

		return "Penguin located at ({}, {}, {})".format(self.position[0], self.position[1], self.position[2])

	def __repr__(self):

		return self.__str__()

	def get_distance(self, penguin2):

		return self.position - penguin2.position

	def determine_boundary_condition(self, penguin_list, a):

		critical_radius = 1.3 * a

		theta_list = []

		for i in range(len(penguin_list)):

			if (penguin_list[i] != self):

				r = self.get_distance(penguin_list[i])
				r_mag = np.linalg.norm(r)

				if (r_mag < critical_radius):

					theta = np.arctan2(r[1],r[0])
					theta_list.append(theta)

		theta_list.sort()

		for j in range(len(theta_list)):

			try:

				difference = theta_list[j+1] - theta_list[j]

			except IndexError:

				difference =  (np.pi - theta_list[j]) + (theta_list[0] + np.pi)

			if (difference > np.pi):

				self.boundary = True

			else:

				self.boundary = False

	def find_exterior_bisector(self, penguin_list, a):

		critical_radius = 1.3 * a

		r_theta_list = []

		for i in range(len(penguin_list)):

			if (penguin_list[i] != self):

				r = self.get_distance(penguin_list[i])
				r_mag = np.linalg.norm(r)

				if (r_mag < critical_radius):

					theta = np.arctan2(r[1],r[0])
					r_theta_list.append([r,theta])

		theta_list = sorted(theta_list, key=itemgetter(1))

		for j in range(len(theta_list)):

			try:

				a = j
				b = j+1
				difference = r_theta_list[b][1] - r_theta_list[a][1]

			except IndexError:

				a = 0
				b = j
				difference =  (np.pi - r_theta_list[b][1]) + (r_theta_list[a][1] + np.pi)

			if (difference > np.pi):

				self.boundary = True

				exterior_bisector = r_theta_list[a][0] + r_theta_list[b][0]

				return exterior_bisector

			else:

				self.boundary = False

				return 0


	# def find_net_force(self, F_self, F_in, k, penguin_list, a):

	# 	critical_radius = 1.3 * a

	# 	F_self_propulsion = F_self * self.alignment

	# 	F_repulsion = np.zeros(3) 

	# 	for i in range(len(penguin_list)):















