import tkinter as tk
from tkinter import ttk
from modules.bgs import BGS_Page
from modules.construct import Construct_Page
from modules.system import System_Page
from modules.market import Market_Page
from modules.db import BGSMini_DB

from config import config, appname, appversion
from pathlib import Path

class MyApp:
    dbg_mode = True
    db = None
    market = None


    def __init__(self, plugin_dir):
        self.plugin_dir = plugin_dir
        self.db = BGSMini_DB(self.plugin_dir)
        self.market = Market_Page(self)
        self.bgs = BGS_Page(self)
        self.depot = Construct_Page(self)
        self.system = System_Page(self)

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
        notebook = ttk.Notebook(frame)

        notebook.config(width=600, height=550)
        notebook.pack(expand = True, fill ="both")

        #main_frame = tk.Frame(notebook, width= 250, height= 200)
        bgs_frame = tk.Frame(notebook)
        depot_frame = tk.Frame(notebook)
        system_frame = tk.Frame(notebook)
        market_frame = tk.Frame(notebook)

        #main_frame.pack(expand = True, fill ="both")
        bgs_frame.pack(expand = True, fill ="both")
        depot_frame.pack(expand = True, fill ="both")
        system_frame.pack(expand = True, fill = "both") 
        market_frame.pack(expand = True, fill = "both") 

        #notebook.add(main_frame, text ='Main') 
        notebook.add(bgs_frame, text ='BGS') 
        notebook.add(depot_frame, text ='Konstrukcje')
        notebook.add(system_frame, text ='Systemy')
        notebook.add(market_frame, text ='Rynki')

        self.bgs.show(bgs_frame)
        self.depot.show(depot_frame)
        self.system.show(system_frame)
        self.market.show(market_frame)
        return frame

    def update_widgets(self):
        self.system.update_widgets()
        self.bgs.update_widgets()
        self.depot.update_widgets()
        self.market.update_widgets()

    #czytanie jurnala (zdarzen) i wyciagniecie danych
    def journal_entry(self, cmdrname: str, is_beta: bool, system: str, station: str, entry: dict, state: dict) -> None:
        '''logger.debug(
            f'cmdr = "{cmdrname}", is_beta = "{is_beta}"'
            f', system = "{system}", station = "{station}"'
            f', event = "{entry["event"]}"'
        )'''
    
        if entry['event'] == 'SquadronStartup':
            if entry['SquadronName'] != '':
                self.SquadronName = entry['SquadronName']
                config.set("BGSMini_SquadronName", self.SquadronName)

        self.system.update(cmdrname, is_beta, system, station, entry, state)
        self.market.update(cmdrname, is_beta, system, station, entry, state)
        self.bgs.update(cmdrname, is_beta, system, station, entry, state)
        self.depot.update(cmdrname, is_beta, system, station, entry, state)

