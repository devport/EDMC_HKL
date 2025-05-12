#!/usr/bin/env python
# vim: textwidth=0 wrapmargin=0 tabstop=4 shiftwidth=4 softtabstop=4 smartindent smarttab

import logging

import tkinter as tk
from tkinter import ttk
import sys
#import datetime
#import shutil
import myNotebook as nb

from pathlib import Path
from tkinter import colorchooser
from app import MyApp


from config import config, appname, appversion

#globalne

plugin_name = Path(__file__).resolve().parent.name
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

this = sys.modules[__name__]
this.app = None

this.tag_fact_color = ''
this.tag_high_color = ''
this.tag_low_color = ''

#this.fact_high_level = 60
#this.fact_low_level = 40

#ladowanie kofiguracji
this.SquadronName = config.get_str("EDMC_HKL_SquadronName")
this.tag_fact_color = 'palegreen' if config.get_str("EDMC_HKL_tag_fact_color") == "" else config.get_str("EDMC_HKL_tag_fact_color")
this.tag_high_color = 'pink' if config.get_str("EDMC_HKL_tag_high_color") == "" else config.get_str("EDMC_HKL_tag_high_color")
this.tag_low_color = 'coral' if config.get_str("EDMC_HKL_tag_low_color") == "" else config.get_str("EDMC_HKL_tag_low_color")

this.fact_high_level = tk.IntVar(value=60 if config.get_int("EDMC_HKL_tag_high_level") == 0 else config.get_int("EDMC_HKL_tag_high_level")) 
this.fact_low_level = tk.IntVar(value=40 if config.get_int("EDMC_HKL_tag_low_level") == 0 else config.get_int("EDMC_HKL_tag_low_level"))

#ustawienia widgetow wtyczki (wygladu)
def plugin_app(parent):    
    return this.app.plugin_app(parent)

#start pluginu
def plugin_start3(plugin_dir):
    this.app = MyApp(plugin_dir)

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

    fact_high_tag_label1 = nb.Label(frame, text="Poziom frakcji wysoki:")
    fact_high_tag_label1.grid(column= 3,padx=10, row=6, sticky=tk.W)

    fact_high_tag_entry = tk.Spinbox(frame, from_= 0, to = 100, width=50, increment=1, textvariable=this.fact_high_level)
    fact_high_tag_entry.grid(column=4, padx=10, row=6, sticky=tk.EW)

    fact_low_tag_label = nb.Label(frame, text="Kolor frakcji niski:")
    if this.tag_low_color != 'None' : fact_low_tag_label.config(bg=this.tag_low_color)
    fact_low_tag_label.grid(column= 1,padx=10, row=7, sticky=tk.W)

    fact_low_tag_label1 = nb.Label(frame, text="Poziom frakcji niski:")
    fact_low_tag_label1.grid(column= 3,padx=10, row=7, sticky=tk.W)

    fact_low_tag_entry = tk.Spinbox(frame, from_= 0, to = 100, width=50, increment=1, textvariable=this.fact_low_level)
    fact_low_tag_entry.grid(column=4, padx=10, row=7, sticky=tk.EW)

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

# settings
def prefs_changed(cmdr, is_beta):
    config.set("EDMC_HKL_tag_fact_color", str(this.tag_fact_color))
    config.set("EDMC_HKL_tag_high_color", str(this.tag_high_color))
    config.set("EDMC_HKL_tag_low_color", str(this.tag_low_color))

    config.set("EDMC_HKL_tag_high_level", int(this.fact_high_level.get()))
    config.set("EDMC_HKL_tag_low_level", int(this.fact_low_level.get()))

    this.app.update_widgets()

#czytanie jurnala (zdarzen) i wyciagniecie danych
def journal_entry(cmdrname: str, is_beta: bool, system: str, station: str, entry: dict, state: dict) -> None:
    if entry['event'] == 'SquadronStartup':
            if entry['SquadronName'] != '':
                this.SquadronName = entry['SquadronName']
                config.set("EDMC_HKL_SquadronName", self.SquadronName)
    this.app.journal_entry(cmdrname, is_beta, system, station, entry, state)


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
