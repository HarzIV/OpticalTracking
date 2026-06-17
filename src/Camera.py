class Camera():
    """
    Class to store all the camera stecific data.
    
    Everything is in mm units.
    
    Args:
        name (str): Name of the camera/sensor.
        sensorSize (tuple): (width, heigth) of the camera sensor.
        focalDistance (float): Distance of the focus point to the camera sensor.
    
    The position defines the position of the focal point.
    The Orientation defines the orientation of the vector normal to the camera sensor,
    which uses the focal point as its base and has the length of the focal distance.
    """
    
    def __init__(self, name: str, sensorSize: tuple, focalDistance: float) -> None:
        self.name = name
        self.sensorSize = sensorSize
        self.focalDistance = focalDistance
        # Set all DOF to 0 for now, because a veriable camera position isn't needed right now.
        self.position = (0, 0, 0)
        self.orientation = (0, 0, 0)
    
    def saveData(self):
        # TODO: Save all camera specific data to json file.
        pass
    
    def findLensDistortion(self):
        # TODO: Implement an algorithm to take in an image and information about the distances of the features in that image and return a lens distortion.
        pass