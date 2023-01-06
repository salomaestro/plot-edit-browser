import os
import pickle
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import PySimpleGUI as sg
from eventhandler import EventHandler
from gui import Gui
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


APPFONT = 'Any 16'

ACCEPTED_PICKLE_FORMATS = ["pkl", "pickle"]

class plotEditor(Gui):
    def __init__(self, debug):

        sg.theme("Topanga")

        self.workdir = Path(os.path.dirname(__file__)).resolve()
        self.recent_dir = self.workdir / "recent"
        self.recent_plots = self.get_recent_plots()

        # Layout for plot tab
        plotlayout = [
            [sg.Canvas(key="-figCanvas-", size=(400*2, 400))],
            [sg.Canvas(key="-ctrlCanvas-")],
            [sg.B("Edit", key="-editPlot"), sg.B("Clear", key="-clearPlot-")]
        ]

        browse_table = sg.Table(
            values=self.display_fmt_recent(self.recent_plots), 
            headings=["Name", "suffix"], 
            expand_x=True, 
            font=APPFONT, 
            justification="left",
            key="-browseTable-",
            tooltip="Double Click To Select",
            alternating_row_color="grey"
        )

        # Layout for browse tab
        browselayout = [
            [browse_table]
        ]

        # Put them together into a tabgroup 
        tabs = sg.TabGroup([
            [sg.Tab("Plot", plotlayout, key="-plotTab-"), sg.Tab("Browse", browselayout, key="-browseTab-")]
        ], tab_location="topleft", key="-mainTabGroup-")

        # Construct layout
        self.layout = [
            [tabs],
            [sg.Push(), sg.B("Exit", key="-EXIT-")]
        ]

        # Call init of Gui
        super().__init__(
            "Plot Editor",
            self.layout,
            event_handler=EventHandler(),
            debug=debug
        )

        self.window["-browseTable-"].bind("<Double-Button-1>", "+-double click-")

        # register handlers
        self.new_handler(self.select_from_table, "-browseTable-+-double click-")
        self.new_handler(self.updatePlot, "-clearPlot-")

        self.figCanvas = self.window["-figCanvas-"]
        self.ctrlCanvas = self.window["-ctrlCanvas-"]

        # Initial figure 
        self.curr_fig = self.empty_fig()
        self.fig_agg = self.draw_figure(self.curr_fig)

    def empty_fig(self):
        return plt.figure()

    def draw_figure(self, figure):
        if self.ctrlCanvas.TKCanvas.children:
            for child in self.ctrlCanvas.TKCanvas.winfo_children():
                child.destroy()
        figure_canvas_agg = FigureCanvasTkAgg(figure, self.figCanvas.TKCanvas)
        figure_canvas_agg.draw()
        toolbar = NavigationToolbar2Tk(figure_canvas_agg, self.ctrlCanvas.TKCanvas)
        toolbar.update()
        figure_canvas_agg.get_tk_widget().pack(side="top", fill="both", expand=1)
        return figure_canvas_agg

    def updatePlot(self, values, **kwargs):
        self.fig_agg.get_tk_widget().forget()
        fig = self.empty_fig()
        
        repl_fig, repl_ax = kwargs.get("browsed", (False, False))

        if repl_fig and repl_ax:

            # Remember to close previous figure
            plt.close()

            # Assign figure as the imported one
            fig, ax = repl_fig, repl_ax
            for line in ax.lines:
                ax.plot(*line.get_data())

        self.fig_agg = self.draw_figure(fig)
        self.curr_fig = fig

    def get_recent_plots(self):
        res = []
        for fname in self.recent_dir.iterdir():
            res.append(fname)
        return res

    def display_fmt_recent(self, recent):
        return list(map(lambda x: (x.stem, x.suffix), recent))

    def select_from_table(self, values):
        selected = values["-browseTable-"]

        fig, ax =  self.load_pickled_plot(self.recent_plots[selected[0]])        
        self.updatePlot(
            values,
            **{"browsed": (fig, ax)}
        )
        self.window["-plotTab-"].select()

    def load_pickled_plot(self, path):
        fig, ax = pickle.load(open(path, "rb"))
        return fig, ax


gui = plotEditor(debug=False)
while True:
    gui.run()