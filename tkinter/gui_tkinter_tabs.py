import os
import time
from tkinter import Tk, Label, Button, Text, ttk, filedialog, messagebox, OptionMenu, StringVar, IntVar, Scale
from pandas import read_csv
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


class OpenVA:
    def __init__(self, master):
        self.master = master
        master.title("openVA App")

        self.xva_title = Label(self.master, text="Load and Prepare Data")
        self.xva_title.grid(row=0, column=0,
                            ipadx=2, ipady=2,
                            padx=2, pady=2, sticky="nw")
        self.load_data = Button(self.master, text='Choose data file...', command=self.upload_action)
        self.load_data.grid(row=1, column=0)
        self.load_data_label = Label(self.master, text="(no data loaded)", justify="left")
        self.load_data_label.grid(row=2, column=0)
        self.data_loaded = False
        self.xva_btn_label = Label(self.master, text="Run pyCrossVA")
        self.xva_btn_label.grid(row=4, column=0)

        self.algorithm_label = Label(self.master, text="Algorithm")
        self.algorithm_label.grid(row=0, column=1, columnspan=2,
                                  ipadx=2, ipady=2,
                                  padx=2, pady=2, sticky="n")
        self.tab_control = ttk.Notebook(self.master)
        self.tab_control.grid(row=1, column=1, columnspan=5, rowspan=8)
        self.tab_interva = ttk.Frame(self.tab_control)
        self.tab_insilico = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_interva, text="InterVA")
        self.tab_control.add(self.tab_insilico, text="InSilicoVA")

        self.interva_label_hiv = Label(self.tab_interva, text="Level of HIV prevalence")
        self.interva_label_hiv.grid(row=0, column=0)
        self.interva_hiv = StringVar(self.master)
        hiv_options = ("very low (v)", "low (l)", "high (h)")
        self.interva_hiv_menu = OptionMenu(self.tab_interva,
                                           self.interva_hiv,
                                           #hiv_options[0],
                                           *hiv_options)
        self.interva_hiv_menu.grid(row=0, column=1)
        self.interva_label_malaria = Label(self.tab_interva, text="Level of malaria prevalence")
        self.interva_label_malaria.grid(row=1, column=0)
        self.interva_malaria = StringVar(self.master)
        malaria_options = ("very low (v)", "low (l)", "high (h)")
        self.interva_malaria_menu = OptionMenu(self.tab_interva,
                                           self.interva_malaria,
                                           *malaria_options)
        self.interva_malaria_menu.grid(row=1, column=1)
        self.interva_run = Button(self.tab_interva, text='Run Algorithm', command=self.interva_run)
        self.interva_run.grid(row=2, column=0)
        self.interva_progress = ttk.Progressbar(self.tab_interva,
                                                orient="horizontal",
                                                length=100,
                                                mode="determinate")
        self.interva_progress.grid(row=2, column=1, sticky="nw", padx=10, pady=10)

        self.insilico_label_nsim = Label(self.tab_insilico, text="Choose number of simulations")
        self.insilico_label_nsim.grid(row=0, column=0)
        self.insilico_slider = Scale(self.tab_insilico, from_=1000, to=5000, orient="horizontal")
        self.insilico_slider.grid(row=1, column=0, columnspan=2, rowspan=2)
        self.insilico_run = Button(self.tab_insilico, text='Run Algorithm', command=self.insilico_run)
        self.insilico_run.grid(row=3, column=1)
        self.insilico_plot = Button(self.tab_insilico, text='Show plot', command=self.insilico_csmf_plot)
        self.insilico_plot.grid(row=4, column=0)

        self.close_button = Button(master, text="Close", command=master.quit)
        self.close_button.grid(row=10, column=10, sticky="nw", padx=20, pady=20)

    def upload_action(self, event=None):
        file_path = filedialog.askopenfilename()
        if not file_path == ():
            file_name = os.path.basename(file_path)
            self.load_data_label.config(text="loaded file: " + file_name)
            self.data = read_csv(file_path)
            data_msg = f"Data file ({file_name}) loaded with {self.data.shape[0]} deaths."
            messagebox.showinfo(title="Data loaded",
                                message=data_msg)
            self.data_loaded = True

    def interva_run(self, event=None):
        if not self.data_loaded:
            messagebox.showinfo(title="InterVA5",
                                message="Data must be loaded to run InterVA5")
        else:
            for a in range(0, 100):
                self.interva_progress["value"] = a
                self.tab_interva.update_idletasks()
                time.sleep(0.01)
            messagebox.showinfo(title="InterVA5",
                                message="InterVA results are ready!")

    def insilico_run(self, event=None):
        if not self.data_loaded:
            messagebox.showinfo(title="InSilicoVA",
                                message="Data must be loaded to run InSilicoVA")
        else:
            for a in range(0, 100):
                self.insilicova_progress["value"] = a
                self.tab_insilico.update_idletasks()
                time.sleep(0.01)
            messagebox.showinfo(title="InSilicoVA",
                                message="InSilicoVA results are ready!")

    def insilico_csmf_plot(self, event=None):
        fig = Figure(figsize=(2, 2), tight_layout=True)
        plot1 = fig.add_subplot(111)
        plot1.plot([1, 2, 3, 4])
        plot1.set_title("Example Plot")
        plot1.set_xlabel("X axis")
        plot1.set_ylabel("Y axis")
        canvas = FigureCanvasTkAgg(fig, master=self.tab_insilico)
        canvas.get_tk_widget().grid(row=5, column=0, columnspan=4, rowspan=4,
                                    padx=2, pady=2, ipadx=2, ipady=2,)
        canvas.draw()




root = Tk()
root.geometry("800x600")
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)
openva = OpenVA(root)
root.mainloop()
