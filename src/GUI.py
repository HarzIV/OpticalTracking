import tkinter as tk
from tkinter import ttk
from Math import Math

class PoseControlPanel(ttk.Frame):
    """Slider controls for translation and orientation."""

    def __init__(self, parent, view):
        super().__init__(parent)

        self.view = view
        self.entryVars = {}
        self.scaleVars = {}

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
            varScale = tk.DoubleVar(value=self.defaultValues[name])
            self.scaleVars[name] = varScale

            scale = ttk.Scale(
                self,
                from_=mn,
                to=mx,
                variable=varScale,
                command=self.syncEntryScale
            )
            scale.grid(
                row=row,
                column=1,
                sticky="ew",
                padx=5
            )

            entryVar = tk.DoubleVar(value=self.defaultValues[name])
            self.entryVars[name] = entryVar

            entry = ttk.Entry(self, textvariable=entryVar, width=5, justify="center")
            entry.grid(
                row=row,
                column=2,
                sticky="w",
                padx=5,
                pady=3,
                columnspan=1
            )
            entry.bind("<Return>", self.syncScaleEntry)
            entry.bind("<FocusOut>", self.syncScaleEntry)
            self.entryVars[name] = entryVar


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
        
    def syncScaleEntry(self, event) -> None:
        """Make sure that when the entry changes the sclae updates."""
        for varName in self.scaleVars:
            self.scaleVars[varName].set(self.entryVars[varName].get())
        
        self.updatePlot()

    def syncEntryScale(self, _=None) -> None:
        """Make sure that when the scle changes the entry updates."""
        for varName in self.entryVars:
            self.entryVars[varName].set(self.scaleVars[varName].get())
            
        self.updatePlot()

    def updatePlot(self):
        """Update the plot, when one of the sclae values changes."""

        self.view.update(
            self.scaleVars["X"].get(),
            self.scaleVars["Y"].get(),
            self.scaleVars["Z"].get(),
            self.scaleVars["Roll"].get(),
            self.scaleVars["Pitch"].get(),
            self.scaleVars["Yaw"].get(),
        )
    
    def resetPlot(self):
        print(self.scaleVars)
        for name in self.scaleVars:
            self.scaleVars[name].set(value=self.defaultValues[name])
            self.entryVars[name].set(value=self.defaultValues[name])
        
        self.updatePlot()
