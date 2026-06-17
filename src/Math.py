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
        
        H = np.array([
            [cos(pitch)*cos(yaw), -cos(pitch)*sin(yaw), sin(pitch), x_trans],
            [cos(roll)*sin(yaw)+sin(roll)*sin(pitch)*cos(yaw), cos(roll)*cos(yaw)-sin(roll)*sin(pitch)*sin(yaw), -sin(roll)*cos(pitch), y_trans],
            [sin(roll)*sin(yaw)-cos(roll)*sin(pitch)*cos(yaw), sin(roll)*cos(yaw)+cos(roll)*sin(pitch)*sin(yaw), cos(roll)*cos(pitch), z_trans],
            [0, 0, 0, 1]
        ])
        
        return H

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
        H = cls.transformation_matrix(x_trans, y_trans, z_trans, roll_deg, pitch_deg, yaw_deg)

        homogeneous = np.hstack((array, np.ones((array.shape[0], 1))))
        
        # Multiply with transposed transformation matrix, to account for the vectors being row vectors.
        transformedArray = homogeneous @ H.T

        # Return only x, y, z and drop w
        return transformedArray[:, :3]
    
    @classmethod
    def projectionMatrix(cls, focalLength, x, y, z, roll_deg, pitch_deg, yaw_deg) -> np.ndarray:
        # Intrisic matrix
        K = np.array([
            [focalLength, 0, 0, 0],
            [0, focalLength, 0, 0],
            [0, 0, 1, 0]
        ])

        # Extrinsic matrix
        H = cls.transformation_matrix(x, y, z, roll_deg, pitch_deg, yaw_deg)
        
        C = K @ H
        
        return C
    
    @classmethod
    def projectPoints(cls, points: np.ndarray, focalLength, x, y, z, roll_deg, pitch_deg, yaw_deg) -> np.ndarray:
        """Project an array of row vectors into the camera viewfield.

        Args:
            points (np.ndarray): Array of row vectors

        Returns:
            np.ndarray: Processed vectors.
        """
        
        C = cls.projectionMatrix(focalLength, x, y, z, roll_deg, pitch_deg, yaw_deg)
        
        homogeneous = np.hstack((points, np.ones((points.shape[0], 1))))
        
        
        # Multiply with transposed transformation matrix, to account for the vectors being row vectors.
        projectedPoints = homogeneous @ C.T

        # Drop the homogenous coordinate
        projectedPoints = projectedPoints[:, :3]

        # Remove the Z factor and move to the correct heigth
        correctedPoints = projectedPoints/(-projectedPoints[:, 2]) - np.array([0, 0, focalLength-1])
        
        return correctedPoints