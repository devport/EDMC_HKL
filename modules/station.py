import sys
import sqlite3
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont

from modules.db import BGSMini_DB

class Station_Page:
    def __init__(self, root):
        self.root = root
        self.db = BGSMini_DB(root.plugin_dir)

    #wyglad 
    def app(self, parent):
        global station_name_label, star_system_label, station_type_title, station_distance_label, landing_pads_title
        main_frame = tk.Frame(parent)
        main_frame.pack(fill="both", expand=True)

        select_frame = tk.LabelFrame(main_frame, text="Wybór")
        select_frame.pack(side="top", fill="x")
        select_group_frame = tk.Frame(select_frame)
        select_group_frame.pack(side="top", fill="x")
        select_system_frame = tk.Frame(select_frame)
        select_system_frame.pack(side="top", fill="x")
        select_station_frame = tk.Frame(select_frame)
        select_station_frame.pack(side="top", fill="x")

        group_title = tk.Label(select_group_frame, text="Grupa:")
        group_title.pack(side="left")
        group_combobox = ttk.Combobox(select_group_frame)
        group_combobox.pack(side="left", padx=10, fill="x", expand=True)

        system_title = tk.Label(select_system_frame, text="System:")
        system_title.pack(side="left")
        system_combobox = ttk.Combobox(select_system_frame)
        system_combobox.pack(side="left", padx=10, fill="x", expand=True)

        station_title = tk.Label(select_station_frame, text="Stacja:")
        station_title.pack(side="left")
        station_combobox = ttk.Combobox(select_station_frame)
        station_combobox.pack(side="left", padx=10, fill="x", expand=True)
        
        #Station
        station_frame = tk.LabelFrame(main_frame, text="Stacja/Obiekt")
        station_frame.pack(side="top", fill="x")

        left_frame = tk.Frame(station_frame, background="blue")
        left_frame.pack(side="left", fill="both", expand=True)

        right_frame = tk.Frame(station_frame, background="red")
        right_frame.pack(side="right", fill="both",  expand=True)

        eco_frame = tk.Frame(station_frame)
        eco_frame.pack(side="top", fill="x")


        station_name_label = tk.Label(left_frame, text="StationName", anchor='w', font=tkFont.Font(family="Arial", size=14))
        station_name_label.pack(side="top", fill="x", padx=15)
        star_system_label = tk.Label(right_frame, text="StarSystem", anchor='w', font=tkFont.Font(family="Arial", size=14))
        star_system_label.pack(side="top", fill="x", padx=15)


        station_type_title = tk.Label(left_frame, text="Typ : Corliolis", anchor='w')
        station_type_title.pack(side="top", fill="x")
        
        station_distance_label = tk.Label(right_frame, text="Disctance from Star : 3,405 LS", anchor='w')
        station_distance_label.pack(side="top", fill="x")

        landing_pads_title = tk.Label(left_frame, text="Landing Pads: ", anchor='w')
        landing_pads_title.pack(side="top", fill="x")

        landing_pads_label = tk.Label(left_frame, text="Large : 7 \nMedium: 14 \nSmall: 11", anchor='w')
        landing_pads_label.pack(side="top", fill="x")


    #odswiezanie danych wygladu
    def update_widgets(self):
        print("update")
        #station_name_label.config(text = self.StationName)
        #star_system_label.config(text = self.StarSystem)
        #station_type_title.config(text = "Typ : " + self.StationType)
        #station_distance_label.config(text="Disctance from Star : "+str(round(self.DistFromStarLS,2)) + " LS")
        #landing_pads_title.config(text="Large landing pads : "+ str(self.LandingPads["Large"]))

    def update(self, cmdrname: str, is_beta: bool, system: str, station: str, entry: dict, state: dict):
        if entry.get("event") == "Docked":
            self.StationName = entry.get("StationName")
            self.StationType = entry.get("StationType")
            self.Taxi = entry.get("Taxi")
            self.Multicrew = entry.get("Multicrew")
            self.StarSystem = entry.get("StarSystem")
            self.SystemAddress = entry.get("SystemAddress")
            
            self.MarketID = entry.get('MarketID')
            self.StationFaction = entry.get("StationFaction")
            self.StationGovernment = entry.get("StationGovernment")
            self.StationGovernment_Localised = entry.get("StationGovernment_Localised")
            self.StationServices = entry.get("StationServices")

            self.StationEconomy = entry.get("StationEconomy")
            self.StationEconomy_Localised = entry.get("StationEconomy_Localised")
            self.StationEconomies = entry.get("StationEconomies")


            self.DistFromStarLS = entry.get("DistFromStarLS")
            self.LandingPads = entry.get("LandingPads")
            self.update_widgets()