import tkinter as tk
from tkinter import ttk
from Math import Math

class PoseControlPanel(ttk.Frame):
    """Slider controls for translation and orientation."""

    def __init__(self, parent, view):
        super().__init__(parent)

        self.view = view
        self.vars = {}

        controls = [
            ("X", -5, 5),
            ("Y", -5, 5),
            ("Z", -5, 5),
            ("Roll",  -180, 180),
            ("Pitch", -180, 180),
            ("Yaw",   -180, 180),
        ]
        
        self.defaultValues = {
            "X": 0.0,
            "Y": 0.0,
            "Z": 0.0,
            "Roll":  0.0,
            "Pitch": 0.0,
            "Yaw":   0.0,
        }

        for row, (name, mn, mx) in enumerate(controls):
            ttk.Label(self, text=name).grid(
                row=row,
                column=0,
                sticky="w",
                padx=5,
                pady=3
            )

            # Listener variable
            var = tk.DoubleVar(value=self.defaultValues[name])
            
            self.vars[name] = var

            scale = ttk.Scale(
                self,
                from_=mn,
                to=mx,
                variable=var,
                command=self._on_change
            )

            scale.grid(
                row=row,
                column=1,
                sticky="ew",
                padx=5
            )

            value_label = ttk.Label(self, width=8)
            value_label.grid(row=row, column=2)

            def update_label(*_, v=var, lbl=value_label):
                lbl.config(text=f"{v.get():.1f}")
                

            var.trace_add("write", update_label)
            update_label()

        self.columnconfigure(1, weight=1)
        
        self.resetButton = ttk.Button(
            self,
            text="RESET",
            command=self.resetPlot
            )
        
        self.resetButton.grid(
            row=len(controls),
            column=0,
            columnspan=3,
            sticky="ew",
            padx=5,
            pady=(15, 5)
        )

    def _on_change(self, _=None):
        """Update the plot, when one of the slider values changes."""

        self.view.update(
            self.vars["X"].get(),
            self.vars["Y"].get(),
            self.vars["Z"].get(),
            self.vars["Roll"].get(),
            self.vars["Pitch"].get(),
            self.vars["Yaw"].get(),
        )
    
    def resetPlot(self):
        print(self.vars)
        for name in self.vars:
            self.vars[name].set(value=self.defaultValues[name])
        
        self._on_change()
