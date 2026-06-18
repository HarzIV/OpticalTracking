from GUI import PoseControlPanel, tk
from plot import Matplotlib3DView, MatplotlibCameraView
from Math import Math
from Camera import Camera


class PoseViewerApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Pose Viewer")
        self.geometry("1000x700")

        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        
        self.Camera = Camera("OV2640", (3.59, 2.684), 3.6)

        self.View3D = Matplotlib3DView(self, self.Camera)
        self.View3D.grid(row=0, column=1, sticky="nsew")

        self.controls = PoseControlPanel(self, self.View3D, self.Camera)
        self.controls.grid(row=0, column=0, sticky="ns", padx=10, pady=10)

if __name__ == "__main__":
    app = PoseViewerApp()
    app.mainloop()