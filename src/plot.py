from tkinter import ttk

import numpy as np

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

from Math import Math
from Camera import Camera

class Matplotlib3DView(ttk.Frame):
    """Embedded matplotlib 3D viewport."""

    def __init__(self, parent, Camera: Camera):
        super().__init__(parent)

        self.figure = Figure(figsize=(6, 5), dpi=100)
        self.ax = self.figure.add_subplot(111, projection="3d")

        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        self._setup_axes()

        # Set up the tracking points        
        self.trackingPoints = Math.arrangePoints(3, 1)
        self.trackingPointsCurrently = Math.arrangePoints(3, 1) # Current position of points, after aplying all transformations.

        # Set up the camera
        self.Camera = Camera
        
        self.update(0, 0, 0, 0, 0, 0)

    def _setup_axes(self) -> None:
        self.ax.set_xlabel("X(mm)")
        self.ax.set_ylabel("Y(mm)")
        self.ax.set_zlabel("Z(mm)")

        self.ax.set_xlim(-5, 5)
        self.ax.set_ylim(-5, 5)
        self.ax.set_zlim(-5, 5)

    def update(self, x, y, z, roll_deg, pitch_deg, yaw_deg) -> np.ndarray:
        """Updates the plot, by rerunning all calculations."""
        
        self.ax.clear()
        self._setup_axes()
        self.placeCamera()
        # self.drawLocalCoordinateSystem(x, y, z, roll_deg, pitch_deg, yaw_deg)
        self.drawTrackingPoints(self.trackingPoints, x, y, z, roll_deg, pitch_deg, yaw_deg)
        
        projectedPoints = self.projectPoints()
        
        self.canvas.draw_idle()
        
        return projectedPoints

    def drawLocalCoordinateSystem(self, x_origin, y_origin, z_origin, roll_deg, pitch_deg, yaw_deg) -> None:
        self.ax.clear()
        self._setup_axes()

        H = Math.transformation_matrix(x_origin, y_origin, z_origin, roll_deg, pitch_deg, yaw_deg)

        origin = np.array([x_origin, y_origin, z_origin])

        axis_len = 1.5
        
        # Using homogenous vectors.
        x_axis = H @ np.array([[axis_len], [0], [0], [1]])
        y_axis = H @ np.array([[0], [axis_len], [0], [1]])
        z_axis = H @ np.array([[0], [0], [axis_len], [1]])
        self.ax.quiver(
            origin[0], origin[1], origin[2],
            x_axis[0], x_axis[1], x_axis[2],
            color='r'
        )

        self.ax.quiver(
            origin[0], origin[1], origin[2],
            y_axis[0], y_axis[1], y_axis[2],
            color='g'
        )

        self.ax.quiver(
            origin[0], origin[1], origin[2],
            z_axis[0], z_axis[1], z_axis[2],
            color='b'
        )

        self.ax.scatter(*origin, s=50, color='y')

        self.canvas.draw_idle()

    def placeCamera(self) -> None:
        # Seprate subplot for the camera, since this one doesn't change when the points move.
        # cameraPlot = self.figure.add_subplot(111, projection="3d")
        
        x, y, z = self.Camera.position
        width, height = self.Camera.sensorSize

        verticies = [[
            (x+width/2, y+height/2, z-self.Camera.focalLength),
            (x+width/2, y-height/2, z-self.Camera.focalLength),
            (x-width/2, y-height/2, z-self.Camera.focalLength),
            (x-width/2, y+height/2, z-self.Camera.focalLength)
        ]]
        
        # Rectangle that show the sensor
        sensorRect = Poly3DCollection(
            verts=verticies,
            facecolors="orange",
            edgecolor="black",
            alpha=0.7
        )
        
        self.ax.add_collection3d(sensorRect)
        
        self.ax.scatter(x, y, z, color="lightblue", alpha=0.9)

    def drawTrackingPoints(self, points, x, y, z, roll_deg, pitch_deg, yaw_deg) -> None:
        self.trackingPointsCurrently = Math.transformArray(points, x, y, z, roll_deg, pitch_deg, yaw_deg)

        self.ax.scatter(*self.trackingPointsCurrently[0], s=20, color='r')
        self.ax.scatter(*self.trackingPointsCurrently[1], s=20, color='g')
        self.ax.scatter(*self.trackingPointsCurrently[2], s=20, color='b')
    
    def projectPoints(self) -> np.ndarray:
        """
        Project the tracking points, onto the camera sensor.
        """
        projectedPoints = Math.projectPoints(self.trackingPointsCurrently, self.Camera.focalLength, *self.Camera.position, *self.Camera.orientation)

        self.ax.scatter(*projectedPoints[0], s=20, color='r')
        self.ax.scatter(*projectedPoints[1], s=20, color='g')
        self.ax.scatter(*projectedPoints[2], s=20, color='b')

        return projectedPoints

class MatplotlibCameraView(ttk.Frame):
    """Embedded matplotlib 2D viewport."""

    def __init__(self, parent, Camera: Camera) -> None:
        super().__init__(parent)

        self.Camera = Camera

        self.figure = Figure(dpi=80)
        self.cameraViewPlot = self.figure.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def setupAxes(self) -> None:
        sensorWidth = self.Camera.sensorSize[0]
        sensorHeight = self.Camera.sensorSize[1]
        
        self.cameraViewPlot.set_xlabel(f"{sensorWidth}mm")
        self.cameraViewPlot.set_ylabel(f"{sensorHeight}mm")

        self.cameraViewPlot.set_xlim(0, sensorWidth)
        self.cameraViewPlot.set_ylim(0, sensorHeight)

        self.cameraViewPlot.grid(visible=True, axis="both")
    
    def drawView(self, points: np.ndarray) -> None:
        self.cameraViewPlot.clear()
        self.setupAxes()

        fittedPoints = Math.fitPointsToRect(points[:, :2], *self.Camera.sensorSize)

        try:
            self.cameraViewPlot.scatter(*fittedPoints[0], s=20, color='r')
            self.cameraViewPlot.scatter(*fittedPoints[1], s=20, color='g')
            self.cameraViewPlot.scatter(*fittedPoints[2], s=20, color='b')
        except Exception as Error:
            # Incase the points are invalid.
            print(Error)
            print(fittedPoints)

        self.canvas.draw_idle()