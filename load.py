#!/usr/bin/env python
# vim: textwidth=0 wrapmargin=0 tabstop=4 shiftwidth=4 softtabstop=4 smartindent smarttab

import logging
import tkinter as tk
from tkinter import ttk
import sys
import datetime
import shutil
import myNotebook as nb
from pathlib import Path
from module_bgs import BGS_Page
from module_depot import Depot_Page
from tkinter import colorchooser

import semantic_version

from config import config, appname, appversion

from market import Market

#globalne
this = sys.modules[__name__]
this.pluginname = 'BGSmini by devport'
this.version = 0.1
this.label_sys_info = tk.Label
this.label_station_info = tk.Label
this.economy_table = ttk.Treeview
this.table_frac = ttk.Treeview
this.label_frac = tk.Label
this.bgs = BGS_Page
this.username = ''
this.userApikey = ''
this.SquadronName = ''
this.plugin_dir = ''
this.config = config
this.market = type(Market)

this.tag_fact_color = ''
this.tag_high_color = ''
this.tag_low_color = ''

# This could also be returned from plugin_start3()
plugin_name = Path(__file__).resolve().parent.name

# Logger per found plugin, so the folder name is included in
# the logging format.
logger = logging.getLogger(f'{appname}.{plugin_name}')
if not logger.hasHandlers():
    level = logging.INFO  # So logger.info(...) is equivalent to print()

    logger.setLevel(level)
    logger_channel = logging.StreamHandler()
    logger_channel.setLevel(level)
    logger_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(module)s:%(lineno)d:%(funcName)s: %(message)s')  # noqa: E501
    logger_formatter.default_time_format = '%Y-%m-%d %H:%M:%S'
    logger_formatter.default_msec_format = '%s.%03d'
    logger_channel.setFormatter(logger_formatter)
    logger.addHandler(logger_channel)

#ladowanie kofiguracji
this.SquadronName = config.get_str("BGSMini_SquadronName")
this.tag_fact_color = 'palegreen' if config.get_str("BGSMini_tag_fact_color") == "" else config.get_str("BGSMini_tag_fact_color")
this.tag_high_color = 'pink' if config.get_str("BGSMini_tag_high_color") == "" else config.get_str("BGSMini_tag_high_color")
this.tag_low_color = 'coral' if config.get_str("BGSMini_tag_low_color") == "" else config.get_str("BGSMini_tag_low_color")

#ustawienia widgetow wtyczki (wygladu)
def plugin_app(parent):
    this.parent = parent
    
    frame = tk.Frame(parent)
    notebook = ttk.Notebook(frame)
    notebook.config(width=500, height=350)
    notebook.pack(expand = True, fill ="both")
    #main_frame = tk.Frame(notebook, width= 250, height= 200)
    bgs_frame = tk.Frame(notebook, width=300)
    depot_frame = tk.Frame(notebook, width=300)

    #main_frame.pack(expand = True, fill ="both")
    bgs_frame.pack(expand = True, fill ="both")
    depot_frame.pack(expand = True, fill ="both")
     
    #notebook.add(main_frame, text ='Main') 
    notebook.add(bgs_frame, text ='BGS') 
    notebook.add(depot_frame, text ='CS')

    this.bgs.show(bgs_frame)
    this.depot.show(depot_frame)
    return (frame)
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
def plugin_start3(plugin_dir: str) -> str:
    """
    Plugin startup method.

    :param plugin_dir:
    :return: 'Pretty' name of this plugin.
    """
    # Up until 5.0.0-beta1 config.appversion is a string
    if isinstance(appversion, str):
        core_version = semantic_version.Version(appversion)

    elif callable(appversion):
        # From 5.0.0-beta1 it's a function, returning semantic_version.Version
        core_version = appversion()

    logger.info(f'Core EDMC version: {core_version}')
    # And then compare like this
    if core_version < semantic_version.Version('5.0.0-beta1'):
        logger.info('EDMC core version is before 5.0.0-beta1')
    else:
        logger.info('EDMC core version is at least 5.0.0-beta1')

    # Yes, just blow up if config.appverison is neither str or callable

    logger.info(f'Folder is {plugin_dir}')

    this.plugin_dir = plugin_dir
    this.market = Market(this)
    this.bgs = BGS_Page(logger, this)
    this.depot = Depot_Page(logger, this)

    # test Marketu
    #this.market.load_journal()
    #this.market.load(3710784768)
    #this.market.save()
    #print(this.market.commodity_names)


    #sprawdzam sobie sciezki 
    print(config.plugin_dir_path)
    print(config.app_dir_path)
    print(config.internal_plugin_dir_path)
    print(config.default_plugin_dir_path)
    print(Path(__file__).resolve().parent)

    return plugin_name


def plugin_stop() -> None:
    logger.info('Stopping')


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
                this.tag_fact_color.color = colorchooser.askcolor(title ="Wybierz kolor")[1]
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

# settings
def prefs_changed(cmdr, is_beta):
    print('preffs functiion entry')
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

    this.market.update(cmdrname, is_beta, system, station, entry, state)
    this.bgs.update(cmdrname, is_beta, system, station, entry, state)
    this.depot.update(cmdrname, is_beta, system, station, entry, state)

    #this.market.load()
    #print(this.market.get_comm())



    '''
    if entry['event'] == 'FSDJump':
        this.label_sys_info['text'] = entry['SystemEconomy_Localised']
        clear_economy_info()
        enum = 0
        for i in  this.table_frac.get_children():
             this.table_frac.delete(i)
        for i in entry['Factions']:
            enum += 1
            data = (i['Name'], i['FactionState'], str(int(i['Influence'] * 100)) +'%')
            this.table_frac.insert(parent = '', index = 0, values = data)
        this.label_frac['text'] = "Frakcje w systemie ( " + str(enum) + ' )'


    if entry['event'] == 'Docked':
        for i in this.economy_table.get_children():
            this.economy_table.delete(i)
        this.label_station_info['text'] = entry['StationEconomy_Localised']
        for j in entry['StationEconomies']:
            data = (j['Name_Localised'], str(int(j['Proportion'] * 100)) +'%')
            this.economy_table.insert(parent = '', index = 0, values = data)
    
def clear_economy_info():
    this.label_station_info['text'] = ''
    for i in this.economy_table.get_children():
        this.economy_table.delete(i)
'''
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
