import tkinter as tk
from stonks import *
import yfinance as yf
from tkcalendar import DateEntry, Calendar
from pandas import DataFrame
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from random import randint

#hello2
resolution = (700, 400)
res_str = str(resolution[0]) + "x" + str(resolution[1])


class SaveButton(tk.Button):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)


class TickerEntry(tk.Entry):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.ticker = None

    def validate(self):
        text = self.get()
        if not text:
            return True

        try:
            yf.Ticker(text)
            self.ticker = text
            return True
        except ValueError:
            return False


class PlusButton(tk.Button):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)


class OverviewListbox(tk.Listbox):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.tickers = []

    def add_item(self, item): #TODO: colors
        self.tickers.append(item)
        self.tickers.sort()
        index = self.tickers.index(item)
        self.insert(index, item)

    def delete_selection(self):
        index = self.curselection()
        self.delete(index)
        del self.tickers[index[0]]

    def delete_all(self):
        self.delete(0, tk.END)
        self.tickers.clear()

    def get_all_items(self):
        return self.tickers

    def get_item(self, index):
        return self.tickers[index]


class DeleteButton(tk.Button):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)


class MenuBar(tk.Menu):
    def __init__(self, parent, *args, **kwargs):
        self.parent = parent
        super().__init__(parent, *args, **kwargs)
        menu_bar = tk.Menu(self.parent)
        self.parent.config(menu=menu_bar)

        self.file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(menu=self.file_menu, label="File")

        self.help_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(menu=self.help_menu, label="Help")
        self.help_menu.add_command(label='About', command=lambda: print('About'))


class ChartFrame(tk.LabelFrame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.config(width=600, height=400)
        self.text = "Chart"
        self.figure_canvas = plt.Figure()
        self.default = self.figure_canvas.add_subplot(111)
        self.figure_canvas.suptitle("Stonks")

        self.a = FigureCanvasTkAgg(self.figure_canvas, self)


class Dates(DateEntry):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.config(date_pattern="dd/mm/yyyy")
        self.from_date = None
        self.to_date = None


class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        self.parent = parent
        super().__init__(self.parent, *args, **kwargs)
        self.parent.title('Stock info')
        #---Frames---
        self.chart_frame = ChartFrame(self.parent)
        self.settings_frame = tk.LabelFrame(self.parent, text="Settings")
        #---Menu Bar---
        self.menu_bar = MenuBar(self.parent)
        self.menu_bar.file_menu.add_command(label='Clear', command=lambda: self.overview_listbox.delete_all())
        self.menu_bar.file_menu.add_separator()
        self.menu_bar.file_menu.add_command(label='Save', command=lambda: print('Save'))
        self.menu_bar.file_menu.add_command(label='Save as', command=lambda: print('Save as'))
        #---Setting's widgets---
        self.ticker_entry = TickerEntry(self.settings_frame)
        self.plus_button = PlusButton(self.settings_frame, text="add", command=lambda: self.plus_button_callback())
        self.delete_button = DeleteButton(self.settings_frame, text=" Delete ", command=lambda: self.overview_listbox.delete_selection())
        self.overview_listbox = OverviewListbox(self.settings_frame)
        self.from_label = tk.Label(self.settings_frame, text="From:")
        self.to_label = tk.Label(self.settings_frame, text='To:')
        self.from_date_entry = Dates(self.settings_frame)
        self.to_date_entry = Dates(self.settings_frame)
        self.click_to_plot = tk.Button(self.settings_frame, text='Click for plot', command= lambda: self.click_for_plot_callback())

        # ---grid master---
        self.settings_frame.grid(column=0, row=0)
        self.chart_frame.grid(column=1, row=0)
        self.ticker_entry.grid(column=0, row=0)
        self.plus_button.grid(column=0, row=1, sticky=tk.E)
        self.from_label.grid(column=0, row=2, sticky=tk.W)
        self.from_date_entry.grid(column=0, row=3, sticky=tk.W+tk.E)

        self.to_label.grid(column=0, row=4, sticky=tk.W)
        self.to_date_entry.grid(column=0, row=5, sticky=tk.W+tk.E)

        self.overview_listbox.grid(column=0, row=6)
        self.delete_button.grid(column=0, row=7)
        self.click_to_plot.grid(column=0, row=8)

    def plus_button_callback(self):
        input = self.ticker_entry.get()
        if not input:
            print('invalid ticker')
            return
        try:
            self.ticker_entry.validate()
            item = Stonk(ticker=input, from_date=self.from_date_entry.get_date(), to_date=self.to_date_entry.get_date())

        except:
            print("Error invalid ticker")
            return
        self.overview_listbox.add_item(item)

    def click_for_plot_callback(self):
        if len(self.overview_listbox.tickers) == 0:
            pass

        self.chart_frame.figure_canvas.clf()
        self.chart_frame.default = self.chart_frame.figure_canvas.add_subplot(1, 1, 1)
        self.chart_frame.figure_canvas.suptitle("Show Stonks")
        self.chart_frame.figure_canvas.autofmt_xdate(rotation=45)

        for tick in self.overview_listbox.tickers:
            self.chart_frame.default.plot(tick.date_series[0], tick.close_series[0], label=tick.ticker)

        self.chart_frame.default.legend()
        self.chart_frame.a.draw()
        self.chart_frame.a.get_tk_widget().grid(column=0, sticky=tk.W + tk.E)


if __name__ == '__main__':
    root = tk.Tk()
    app = MainApplication(root)
    root.mainloop()








