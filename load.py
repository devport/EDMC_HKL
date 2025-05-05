import logging

from theme import theme
import tkinter as tk
from tkinter import ttk
import sys
#import datetime
#import shutil
#import myNotebook as nb

from pathlib import Path
from modules.module_bgs import BGS_Page
from modules.module_depot import Depot_Page
from modules.module_system import System_Page
from modules.module_market import Market
from tkinter import colorchooser

import semantic_version

from config import config, appname, appversion

#globalne

this = sys.modules[__name__]
this.dbg_mode = False
'''this.pluginname = 'BGSmini by devport'
this.version = 0.1
this.dbg_mode = False
this.label_sys_info = tk.Label
this.label_station_info = tk.Label
this.economy_table = ttk.Treeview
this.table_frac = ttk.Treeview
this.label_frac = tk.Label
this.username = ''
this.userApikey = ''
this.SquadronName = ''
this.plugin_dir = ''
this.config = config
'''

this.tag_fact_color = ''
this.tag_high_color = ''
this.tag_low_color = ''

#ladowanie kofiguracji
this.SquadronName = config.get_str("BGSMini_SquadronName")
this.tag_fact_color = 'palegreen' if config.get_str("BGSMini_tag_fact_color") == "" else config.get_str("BGSMini_tag_fact_color")
this.tag_high_color = 'pink' if config.get_str("BGSMini_tag_high_color") == "" else config.get_str("BGSMini_tag_high_color")
this.tag_low_color = 'coral' if config.get_str("BGSMini_tag_low_color") == "" else config.get_str("BGSMini_tag_low_color")

#ustawienia widgetow wtyczki (wygladu)
def plugin_app(parent):    
    frame = tk.Frame(parent)
    notebook = ttk.Notebook(frame)

    notebook.config(width=600, height=550)
    notebook.pack(expand = True, fill ="both")

    #main_frame = tk.Frame(notebook, width= 250, height= 200)
    bgs_frame = tk.Frame(notebook)
    depot_frame = tk.Frame(notebook)
    system_frame = tk.Frame(notebook)

    #main_frame.pack(expand = True, fill ="both")
    bgs_frame.pack(expand = True, fill ="both")
    depot_frame.pack(expand = True, fill ="both")
    system_frame.pack(expand = True, fill = "both") 

    #notebook.add(main_frame, text ='Main') 
    notebook.add(bgs_frame, text ='BGS') 
    notebook.add(depot_frame, text ='Magazyn')
    notebook.add(system_frame, text ='Systemy')

    this.bgs.show(bgs_frame)
    this.depot.show(depot_frame)
    this.system.app(system_frame)

    theme.update(frame)
    print(theme.current)

    return frame
'''

    #dane o ekonomii
    label_sys = tk.Label(frame, text="Ekonomia systemu :", anchor='w')
    label_sys.grid(row=3, column=0)
    this.label_sys_info = tk.Label(frame, text="")
    this.label_sys_info.grid(row=3, column=1)
    
    label_station = tk.Label(frame, text="Ekonomia wiodąca obiektu :", anchor='w')
    label_station.grid(row=4, column=0)
    this.label_station_info = tk.Label(frame, text="")
    this.label_station_info.grid(row=4, column=1)
    
    this.economy_table = ttk.Treeview(frame, height= 5,columns=('Name_Localised', 'Proportion'), show = 'headings')
    this.economy_table.grid(row=5, column=0, columnspan=3)
    this.economy_table.heading('Name_Localised', text= 'Nazwa ekonomii')
    this.economy_table.heading('Proportion', text= 'Proporcje')
   
    return (frame)

'''

#start pluginu
def plugin_start3(plugin_dir):
    """
    Plugin startup method.

    :param plugin_dir:
    :return: 'Pretty' name of this plugin.
    """

    this.plugin_dir = plugin_dir
    this.market = Market(this)
    this.bgs = BGS_Page(this)
    this.depot = Depot_Page(this)
    this.system = System_Page(this)

    #sprawdzam sobie sciezki 
    if this.dbg_mode:
        print(config.plugin_dir_path)
        print(config.app_dir_path)
        print(config.internal_plugin_dir_path)
        print(config.default_plugin_dir_path)
        print(Path(__file__).resolve().parent)

    return "EDMC_HKL"


def plugin_stop() -> None:
    print('Stopping')


def plugin_prefs(parent, cmdr, is_beta):
    frame = nb.Frame(parent)
    frame.columnconfigure(2, weight=1)

    squadron_name_label = nb.Label(frame, text="Nazwa Squadronu:")
    squadron_name_label.grid(column= 1, padx=10, row=1, sticky=tk.W)

    squadron_name = nb.Label(frame, text=this.SquadronName)
    squadron_name.grid(column= 2, padx=10, row=1, sticky=tk.W)

    #kolory frakcji
    fact_faction_tag_label = nb.Label(frame, text="Kolor frakcji standardowy:")
    if this.tag_fact_color != 'None' : fact_faction_tag_label.config(bg=this.tag_fact_color)
    fact_faction_tag_label.grid(column= 1, padx=10, row=5, sticky=tk.W)

    fact_high_tag_label = nb.Label(frame, text="Kolor frakcji wysoki:")
    if this.tag_high_color != 'None' : fact_high_tag_label.config(bg=this.tag_high_color)
    fact_high_tag_label.grid(column= 1,padx=10, row=6, sticky=tk.W)

    fact_low_tag_label = nb.Label(frame, text="Kolor frakcji niski:")
    if this.tag_low_color != 'None' : fact_low_tag_label.config(bg=this.tag_low_color)
    fact_low_tag_label.grid(column= 1,padx=10, row=7, sticky=tk.W)

    def choose_color(tag_name):
        match tag_name:
            case 'faction':
                this.tag_fact_color = colorchooser.askcolor(title ="Wybierz kolor")[1]
                fact_faction_tag_label.config(bg=this.tag_fact_color)
            case 'high':
                this.tag_high_color = colorchooser.askcolor(title ="Wybierz kolor")[1]
                fact_high_tag_label.config(bg=this.tag_high_color)
            case 'low':
                this.tag_low_color = colorchooser.askcolor(title ="Wybierz kolor")[1]
                fact_low_tag_label.config(bg=this.tag_low_color)


    fact_faction_tag_button = nb.Button(frame, text="Wybierz Kolor", command=lambda: choose_color('faction'))
    fact_faction_tag_button.grid(column= 2, padx=10, row=5, sticky=tk.W)

    fact_high_tag_button = nb.Button(frame, text="Wybierz Kolor", command=lambda: choose_color('high'))
    fact_high_tag_button.grid(column= 2, padx=10, row=6, sticky=tk.W)

    fact_low_tag_button = nb.Button(frame, text="Wybierz Kolor", command=lambda: choose_color('low'))
    fact_low_tag_button.grid(column= 2, padx=10, row=7, sticky=tk.W)
    return frame    

def update_widgets():
    this.system.update_widgets()
    this.bgs.update_widgets()
    this.depot.update_widgets()

# settings
def prefs_changed(cmdr, is_beta):
    config.set("BGSMini_tag_fact_color", str(this.tag_fact_color))
    config.set("BGSMini_tag_high_color", str(this.tag_high_color))
    config.set("BGSMini_tag_low_color", str(this.tag_low_color))
    this.bgs.update_widgets()

#czytanie jurnala (zdarzen) i wyciagniecie danych
def journal_entry(cmdrname: str, is_beta: bool, system: str, station: str, entry: dict, state: dict) -> None:
    logger.debug(
            f'cmdr = "{cmdrname}", is_beta = "{is_beta}"'
            f', system = "{system}", station = "{station}"'
            f', event = "{entry["event"]}"'
    )
    
    if entry['event'] == 'SquadronStartup':
        if entry['SquadronName'] != '':
            this.SquadronName = entry['SquadronName']
            config.set("BGSMini_SquadronName", this.SquadronName)

    this.system.update(cmdrname, is_beta, system, station, entry, state)
    this.market.update(cmdrname, is_beta, system, station, entry, state)
    this.bgs.update(cmdrname, is_beta, system, station, entry, state)
    this.depot.update(cmdrname, is_beta, system, station, entry, state)


#{ "timestamp":"2025-04-11T14:44:21Z", "event":"Location", 
# "DistFromStarLS":17098.307003, 
# "Docked":false, 
# "Taxi":false, 
# "Multicrew":false, 
# "StarSystem":"HR 8222", 
# "SystemAddress":112975660228, 
# "StarPos":[-147.90625,-266.81250,235.00000], 
# "SystemAllegiance":"", 
# "SystemEconomy":"$economy_None;", 
# "SystemEconomy_Localised":"None", 
# "SystemSecondEconomy":"$economy_None;", 
# "SystemSecondEconomy_Localised":"None", 
# "SystemGovernment":"$government_None;", 
# "SystemGovernment_Localised":"None", 
# "SystemSecurity":"$GAlAXY_MAP_INFO_state_anarchy;", 
# "SystemSecurity_Localised":"Anarchy", 
# "Population":0, 
# "Body":"HR 8222 AB 1", 
# "BodyID":56, 
# "BodyType":"Planet", 
# "Factions":[ { 
#   "Name":"The Winged Hussars", 
#   "FactionState":"Expansion", "Government":"Cooperative", 
#   "Influence":1.000000, 
#   "Allegiance":"Independent", 
#   "Happiness":"$Faction_HappinessBand2;", 
#   "Happiness_Localised":"Happy", 
#   "SquadronFaction":true, 
#   "MyReputation":100.000000, 
#   "ActiveStates":[ { "State":"Expansion" } ] } ], "SystemFaction":{ "Name":"The Winged Hussars", "FactionState":"Expansion" } }
