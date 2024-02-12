# Anle of Attack sensor.


"""
angle of attack class will provide the following. It will select different anlge of attacks. These angle of attacks are 
then used to get the CL

the angle of attack is adjusted to adjust the lift . This is done inside the altitude hold mode.

Considering thrust is set... 


"""

class AngleOfAttackSensor(Sensor):
    """
    This class will contain and "measure" the angle of attack. The angle of attack will not be visible in the simulation
    rendering, but will be used to control the airplane as well as the forces acting on it like Lift and Drag.
    """
    
    def __init__(self, config={}):
        """
        Initialize the AngleOfAttack Class.

        Args:
        """

        super().__init__(sensor_type="Heading Indicator", update_rate=config.get("update_rate", 250.0))

        # state of the sensor
        self._state = {"angle_of_attack:": 0.0}

    def update(self, aoa):

        self._state["angle_of_attack:"] = aoa
        
        