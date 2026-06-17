import numpy as np
from numpy import sin, cos

class Math():
    def __init__(self) -> None:
        pass
        
    @staticmethod
    def transformation_matrix(x_trans, y_trans, z_trans, roll_deg, pitch_deg, yaw_deg) -> np.ndarray:
        """
        Roll  = X rotation
        Pitch = Y rotation
        Yaw   = Z rotation
        """
        roll = np.radians(roll_deg)
        pitch = np.radians(pitch_deg)
        yaw = np.radians(yaw_deg)
        
        K = np.array([
            [cos(pitch)*cos(yaw), -cos(pitch)*sin(yaw), sin(pitch), x_trans],
            [cos(roll)*sin(yaw)+sin(roll)*sin(pitch)*cos(yaw), cos(roll)*cos(yaw)-sin(roll)*sin(pitch)*sin(yaw), -sin(roll)*cos(pitch), y_trans],
            [sin(roll)*sin(yaw)-cos(roll)*sin(pitch)*cos(yaw), sin(roll)*cos(yaw)+cos(roll)*sin(pitch)*sin(yaw), cos(roll)*cos(pitch), z_trans],
            [0, 0, 0, 1]
        ])
        
        return K

    @staticmethod
    def arrangePoints(number, radius)-> np.ndarray[np.ndarray[np.float64]]:
        """Create an array of n points, arranged in a circle of set radius, around (0, 0, 0)."""
        
        stepSize = 2*np.pi/number
        points = np.empty((number, 3))

        for n in range(number):
            points[n] = np.array([radius*cos(n*stepSize), radius*sin(n*stepSize), 0])

        return points
    
    @classmethod
    def transformArray(cls, array: np.ndarray, x_trans, y_trans, z_trans, roll_deg, pitch_deg, yaw_deg) -> np.ndarray:
        """Transform an array of non homogenous vectors, that are stored as row vectors, using a transformation matrix K."""
        K = cls.transformation_matrix(x_trans, y_trans, z_trans, roll_deg, pitch_deg, yaw_deg)

        homogeneous = np.hstack((array, np.ones((array.shape[0], 1))))
        
        # Multiply with transposed transformation matrix, to account for the vectors being row vectors.
        transformedArray = homogeneous @ K.T

        # Return only x, y, z and drop w
        return transformedArray[:, :3]