from GUI import PoseControlPanel, tk
from plot import Matplotlib3DView
from Math import Math


class PoseViewerApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Pose Viewer")
        self.geometry("1000x700")

        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        self.view = Matplotlib3DView(self)
        self.view.grid(row=0, column=1, sticky="nsew")

        self.controls = PoseControlPanel(self, self.view)
        self.controls.grid(row=0, column=0, sticky="ns", padx=10, pady=10)

if __name__ == "__main__":
    app = PoseViewerApp()
    app.mainloop()