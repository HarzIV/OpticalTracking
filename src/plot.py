from tkinter import ttk

import numpy as np

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from Math import Math

class Matplotlib3DView(ttk.Frame):
    """Embedded matplotlib 3D viewport."""

    def __init__(self, parent):
        super().__init__(parent)

        self.figure = Figure(figsize=(6, 5), dpi=100)
        self.ax = self.figure.add_subplot(111, projection="3d")

        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        self._setup_axes()
        
        self.points = Math.arrangePoints(3, 1)
        
        self.update(0, 0, 0, 0, 0, 0)

    def _setup_axes(self):
        self.ax.set_xlabel("X")
        self.ax.set_ylabel("Y")
        self.ax.set_zlabel("Z")

        self.ax.set_xlim(-5, 5)
        self.ax.set_ylim(-5, 5)
        self.ax.set_zlim(-5, 5)

    def update(self, x, y, z, roll_deg, pitch_deg, yaw_deg):
        """Updates the plot, by rerunning all calculations."""
        # self.drawLocalCoordinateSystem(x, y, z, roll_deg, pitch_deg, yaw_deg)
        self.drawPoints(self.points, x, y, z, roll_deg, pitch_deg, yaw_deg)

    def drawLocalCoordinateSystem(self, x_origin, y_origin, z_origin, roll_deg, pitch_deg, yaw_deg):
        self.ax.clear()
        self._setup_axes()

        K = Math.transformation_matrix(x_origin, y_origin, z_origin, roll_deg, pitch_deg, yaw_deg)

        origin = np.array([x_origin, y_origin, z_origin])

        axis_len = 1.5
        
        # Using homogenous vectors.
        x_axis = K @ np.array([[axis_len], [0], [0], [1]])
        y_axis = K @ np.array([[0], [axis_len], [0], [1]])
        z_axis = K @ np.array([[0], [0], [axis_len], [1]])
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

    def drawPoints(self, points, x, y, z, roll_deg, pitch_deg, yaw_deg):
        self.ax.clear()
        self._setup_axes()
        
        transformedPoints = Math.transformArray(points, x, y, z, roll_deg, pitch_deg, yaw_deg)

        self.ax.scatter(*transformedPoints[0], s=20, color='r')
        self.ax.scatter(*transformedPoints[1], s=20, color='g')
        self.ax.scatter(*transformedPoints[2], s=20, color='b')

        self.canvas.draw_idle()