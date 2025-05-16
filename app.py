import tkinter as tk
from tkinter import ttk
from modules.bgs import BGS_Page
from modules.construct import Construct_Page
from modules.system import System_Page
from modules.station import Station_Page
from modules.market import Market_Page
from modules.db import BGSMini_DB

from config import config, appname, appversion
from pathlib import Path

from tools import ptl

class MyApp:
    dbg_mode = False
    db = None
    market = None


    def __init__(self, plugin_dir):
        self.plugin_dir = plugin_dir
        self.db = BGSMini_DB(self.plugin_dir)
        self.market = Market_Page(self)
        self.bgs = BGS_Page(self)
        self.depot = Construct_Page(self)
        self.system = System_Page(self)
        self.station = Station_Page(self)

        #sprawdzam sobie sciezki 
        if self.dbg_mode:
            print('Directories:')
            print(config.plugin_dir_path)
            print(config.app_dir_path)
            print(config.internal_plugin_dir_path)
            print(config.default_plugin_dir_path)
            print(Path(__file__).resolve().parent)

    def plugin_app(self, parent):
        frame = tk.Frame(parent)
        self.notebook = ttk.Notebook(frame)

        self.notebook.config(width=600, height=550)
        self.notebook.pack(expand = True, fill ="both")

        #main_frame = tk.Frame(notebook, width= 250, height= 200)
        bgs_frame = tk.Frame(self.notebook)
        depot_frame = tk.Frame(self.notebook)
        system_frame = tk.Frame(self.notebook)
        station_frame = tk.Frame(self.notebook)
        market_frame = tk.Frame(self.notebook)

        #main_frame.pack(expand = True, fill ="both")
        bgs_frame.pack(expand = True, fill ="both")
        depot_frame.pack(expand = True, fill ="both")
        system_frame.pack(expand = True, fill = "both") 
        station_frame.pack(expand = True, fill = "both") 
        market_frame.pack(expand = True, fill = "both") 

        #notebook.add(main_frame, text ='Main') 
        self.notebook.add(bgs_frame, text = ptl('BGS')) 
        self.notebook.add(depot_frame, text = ptl('Constructions'))
        self.notebook.add(system_frame, text = ptl('Systems'))
        self.notebook.add(station_frame, text = ptl('Stations'))
        self.notebook.add(market_frame, text = ptl('Markets'))
    
        self.bgs.show(bgs_frame)
        self.depot.show(depot_frame)
        self.system.show(system_frame)
        self.station.show(station_frame)
        self.market.show(market_frame)
        return frame

    def update_widgets(self):
        self.notebook.tab(0, text=ptl('BGS'))
        self.notebook.tab(1, text=ptl('Constructions'))
        self.notebook.tab(2, text=ptl('Systems'))
        self.notebook.tab(3, text=ptl('Stations'))
        self.notebook.tab(4, text=ptl('Markets'))

        self.system.update_widgets()
        self.bgs.update_widgets()
        self.depot.update_widgets()
        self.market.update_widgets()
        self.station.update_widgets()



    #czytanie jurnala (zdarzen) i wyciagniecie danych
    def journal_entry(self, cmdrname: str, is_beta: bool, system: str, station: str, entry: dict, state: dict) -> None:
        '''logger.debug(
            f'cmdr = "{cmdrname}", is_beta = "{is_beta}"'
            f', system = "{system}", station = "{station}"'
            f', event = "{entry["event"]}"'
        )'''

        self.system.update(cmdrname, is_beta, system, station, entry, state)
        self.market.update(cmdrname, is_beta, system, station, entry, state)
        self.bgs.update(cmdrname, is_beta, system, station, entry, state)
        self.depot.update(cmdrname, is_beta, system, station, entry, state)
        self.station.update(cmdrname, is_beta, system, station, entry, state)

