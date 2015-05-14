#Initalizes the animation plot
def init():
	path = ax.scatter3D([],[],[])
	return path


#Updates the position of the particles for the animation
def update_position(i):
	if i%10 == 0:
		print i
	ax.clear()

	ax.set_xlim3d([-L, L])
	ax.set_xlabel('X')

	ax.set_ylim3d([-L, L])
	ax.set_ylabel('Y')

	ax.set_zlim3d([-L, L])
	ax.set_zlabel('Z')

	x = data[0][i*skip_factor]
	y = data[1][i*skip_factor]
	z = data[2][i*skip_factor]
	path = ax.scatter3D(x,y,z)

	return path


#Runs the animation of particle positions
	fig = plt.figure()
	ax = p3.Axes3D(fig)	

	ax.set_axis_off()
	ax.axis('off') 

	numframes = int(max_frames/skip_factor)
	anim = animation.FuncAnimation(fig, update_position, numframes, blit=False, init_func=init)

	plt.show()