import sympy
from currenteqs import current

# Add the name of the circuit being simulated here
cirname = 'NAND implementation of XOR gate '

# The functions in this library change with the circuit being used. 
# All the state space equations go into the get_nonlinear_matrix() function
# The state space ordering is done by the get_stateorder() function
print "Working on",cirname

# The following parameters are to be customized for the circuit being simulated
# These parameters are the bridge between the project and SPICE.
#-------------------------------------------------------------------------------------------- 
order = 8
sim_begin = 0.0
sim_end = 2.00000000000000e-006
file_voltage = './Data/XOR_voltage.txt'
file_current = './Data/XOR_current.txt'
file_netlist = './Data/XOR.net'
input_list = ['ainp']
output_list = ['xorout']
denominator = 40
constant_dict = {'vdd':5 , '0' :0}
intg_end = 2e-6

#--------------------------------------------------------------------------------------------
# Check-list before running the program : 
#	1. All the details pertaining to the SPICE file
#	2. All the constant voltages in the SPICE simulation
#	3. State equations for the current circuit
#	4. State order for the current state space
#	5. Inputs specific to the current scenario ( in sync with the input list mentioned above )	


def get_nonlinear_matrix(state,regions,Vth):
	''' 
	1.This function is instance specific. 
	2.All the state equations are defined in here
	Input:
		
	state = symbolic vector with states defined it
	regions = contains information regarding each transistor with the region of operation specified
	Vth = dictionary with threshold voltages of each transistor
	
	Returns :
	The symbolic expression with non-linear state space equations in it.'''
	
	# Define all the parasitic capacitors in here. Generally we assume that they are constant. 
	# Name the parasitics accordingly
	#-----------------------------------------------------------------------------------------------------
	Cpara_out = 1e-15
	Cpara_M1 = 1e-15
	Cpara_M2 = 1e-15
	Cpara_M3 = 1e-15

	#-----------------------------------------------------------------------------------------------------	
	# This provides a dictionary with
	# KEY	:	Name of the transistor
	# VALUE	:	Polynomial expansion of current equation at a particular linearization point 
	# To access any current equation use I[ 'name of the transistor' ] 
	
	I={i: current(regions[i],state,Vth[i]) for i in regions.keys()}

	
	# The equations from here are all circuit dependant. Add your equations from here
	# NOTE:
	
	# To access any current through a transistor use I[ 'name of transistor' ], we assume this current is the DRAIN current
	#-----------------------------------------------------------------------------------------------------
	   
	v1dot = (I[ 'm3' ] + I[ 'm4' ] - I[ 'm1' ] )/ Cpara_out
	v2dot = ( I[ 'm1' ] - I[ 'm2' ] ) / Cpara_M1

	v3dot = (I[ 'm7' ] + I[ 'm8' ] - I[ 'm5' ] )/ Cpara_out
	v4dot = ( I[ 'm5' ] - I[ 'm6' ] ) / Cpara_M1

	v5dot = (I[ 'm11' ] + I[ 'm12' ] - I[ 'm9' ] )/ Cpara_out
	v6dot = ( I[ 'm9' ] - I[ 'm10' ] ) / Cpara_M1

	v7dot = (I[ 'm15' ] + I[ 'm16' ] - I[ 'm13' ] )/ Cpara_out
	v8dot = ( I[ 'm13' ] - I[ 'm14' ] ) / Cpara_M1
	#-----------------------------------------------------------------------------------------------------
	
	# The next line packs all the equations in a certain order which is binding. This order decides the state space co-ordinates
	# Ensure that the same ordering is maintained with the stateorder function.
	
#	eqs=sympy.Matrix( [(vd0dot),(vd12dot),(vd11dot),(vcmfb2dot),(vomdot),(vopdot),(vdc3dot),(vdc5dot),(vcmfb1dot),(vd1dot),(vd2dot),(ig9dot),(ig7dot)] )
	eqs = sympy.Matrix( [(v1dot),(v2dot),(v3dot),(v4dot),(v5dot),(v6dot),(v7dot),(v8dot)] )	    
	return eqs


# Define the time dependant input signal. 
def get_input_signals( t ):
	''' Returns:
	The values of all the inputs at any given time instant'''
	if t <= 1e-6:
		return [  5e6*t ]
	if t > 1e-6:
		return [ 5 ]

		

def get_stateorder(state):
	''' Returns stateorder, which is necessary for the construction of the state 
	Check with the state space equations and ensure that the same ordering is being followed'''

	stateorder=sympy.Matrix([(state['inter1']),(state['n001']),(state['ainter1']),(state['n002']),(state['binter1']),(state['n003']),(state['xorout']),(state['n004'])])
	
	return stateorder

