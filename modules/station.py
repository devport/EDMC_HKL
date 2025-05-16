import sys
import sqlite3
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont

from tools import ptl

class Station_Page:
    select_group = None
    group_names = []
    select_system = None
    system_names = []
    select_station = None
    station_names = []

    def __init__(self, parent):
        self.app = parent
        self.db = self.app.db

    #wyglad 
    def show(self, parent):
        global station_name_label, star_system_label, station_type_title, station_distance_label, landing_pads_title
        main_frame = tk.Frame(parent)
        main_frame.pack(fill="both", expand=True)

        self.select_frame = tk.LabelFrame(main_frame)
        self.select_frame.pack(side="top", fill="x")
        select_group_frame = tk.Frame(self.select_frame)
        select_group_frame.pack(side="top", fill="x")
        select_system_frame = tk.Frame(self.select_frame)
        select_system_frame.pack(side="top", fill="x")
        select_station_frame = tk.Frame(self.select_frame)
        select_station_frame.pack(side="top", fill="x")

        self.group_title = tk.Label(select_group_frame)
        self.group_title.pack(side="left")
        self.combobox_groups = ttk.Combobox(select_group_frame)
        self.combobox_groups.pack(side="left", padx=10, fill="x", expand=True)
        self.combobox_groups.config(state='readonly')

        def Select_Group_Combo(event):
            group_row = self.db.Select('cmdr_groups', 'id, name', f"name = \"{self.combobox_groups.get()}\" ", True)
            if group_row:
                self.select_group = {"id" : group_row[0], "name" :group_row[1]}
                self.update_widgets()

        self.combobox_groups.bind('<<ComboboxSelected>>', Select_Group_Combo)

        self.system_title = tk.Label(select_system_frame)
        self.system_title.pack(side="left")
        self.combobox_systems = ttk.Combobox(select_system_frame)
        self.combobox_systems.pack(side="left", padx=10, fill="x", expand=True)
        self.combobox_systems.config(state='readonly')

        def Select_System_Combo(event):
            system_row = self.db.Select('cmdr_systems', 'star_system', f"star_system = \"{self.combobox_systems.get()}\" ", True)
            if system_row:
                self.select_system = {"star_system" :system_row[0]}
                self.update_widgets()

        self.combobox_systems.bind('<<ComboboxSelected>>', Select_System_Combo)

        self.station_title = tk.Label(select_station_frame)
        self.station_title.pack(side="left")
        self.combobox_stations = ttk.Combobox(select_station_frame)
        self.combobox_stations.pack(side="left", padx=10, fill="x", expand=True)
        self.combobox_stations.config(state='readonly')

        def Select_Station_Combo(event):
            station_row = self.db.Select('stations', '*', f"StationName = \"{self.combobox_stations.get()}\" ", True)
            if station_row:
                # StarSystem, SystemAddress, StationName, StationType, MarketID, DistFromStarLS, StationFaction, StationGovernment, 
                # StationGovernment_Localised, StationEconomy, StationEconomy_Localised, StationEconomies, LandingPads
                self.select_station = {
                    "StarSystem" : station_row[0],
                    "SystemAddress" : station_row[1],
                    "StationName" : station_row[2],
                    "StationType" : station_row[3],
                    "MarketID" :station_row[4],
                    "DistFromStarLS" :station_row[5],
                    "StationFaction" :station_row[6],
                    "StationGovernment" :station_row[7],
                    "StationGovernment_Localised" :station_row[8],
                    "StationEconomy" :station_row[9],
                    "StationEconomy_Localised" :station_row[10],
                    "StationEconomies" :station_row[11],
                    "LandingPads" :station_row[12]
                    }
                self.update_widgets()

        self.combobox_stations.bind('<<ComboboxSelected>>', Select_Station_Combo)

        #Station
        self.station_frame = tk.LabelFrame(main_frame, text="Stacja/Obiekt")
        self.station_frame.pack(side="top", fill="x")

        #left_frame = tk.Frame(station_frame)
        #left_frame.pack(side="left", fill="both", expand=True)

        #right_frame = tk.Frame(station_frame)
        #right_frame.pack(side="right", fill="both",  expand=True)

        eco_frame = tk.Frame(main_frame)
        eco_frame.pack(side="top", fill="x")


        self.station_name_label = tk.Label(self.station_frame, anchor='w', font=tkFont.Font(family="Arial", size=14))
        self.station_name_label.pack(side="top", fill="x", padx=15)
        self.star_system_label = tk.Label(self.station_frame, anchor='w', font=tkFont.Font(family="Arial", size=14))
        self.star_system_label.pack(side="top", fill="x", padx=15)

        #left
        self.station_type_title = tk.Label(self.station_frame, anchor='w')
        self.station_type_title.pack(side="top", fill="x", padx=15)

        self.landing_pads_title = tk.Label(self.station_frame, anchor='w')
        self.landing_pads_title.pack(side="top", fill="x", padx=15)

        self.station_faction_label = tk.Label(self.station_frame, anchor='w')
        self.station_faction_label.pack(side="top", fill="x", padx=15)
                
        self.station_faction_list = tk.Label(self.station_frame, anchor='w')
        self.station_faction_list.pack(side="top", fill="x", padx=15)
        #right
        self.station_distance_label = tk.Label(self.station_frame, anchor='w')
        self.station_distance_label.pack(side="top", fill="x", padx=15)

        self.station_government_label = tk.Label(self.station_frame, anchor='w')
        self.station_government_label.pack(side="top", fill="x", padx=15)

        self.station_economy_title = tk.Label(self.station_frame, anchor='w')
        self.station_economy_title.pack(side="top", fill="x", padx=15)

        self.station_economies_label = tk.Label(self.station_frame, anchor='w')
        self.station_economies_label.pack(side="top", fill="x", padx=15)

        self.station_economies_list = tk.Label(self.station_frame, anchor='w')
        self.station_economies_list.pack(side="top", fill="x", padx=15)

        self.update_widgets()
        
    #odswiezanie danych wygladu
    def update_widgets(self):

        print("select_group: ", self.select_group)
        print("select_system: ", self.select_system)
        print("select_station: ", self.select_station)

        self.select_frame.config(text= ptl("Choise"))
        self.group_title.config(text= ptl("Group"))
        self.system_title.config(text = ptl("System") + ":")
        self.station_title.config(text = ptl("Station") + ":")

        self.station_name_label.config(text = ptl("Station name"))
        self.star_system_label.config(text = ptl("System name"))
        self.station_type_title.config(text = ptl("Station type : "))
        self.landing_pads_title.config(text = ptl("Landing pads : "))
        self.station_faction_label.config(text = ptl("Station faction : "))
        self.station_faction_list.config(text = ptl("no data"))
        self.station_distance_label.config(text = ptl("Disctance from star : "))
        self.station_government_label.config(text = ptl("Government : "))
        self.station_economy_title.config(text = ptl("Station economy : "))
        self.station_economies_label.config(text = ptl("Others economies : "))
        self.station_economies_list.config(text = ptl("no data"))

        # groups
        group_rows = self.db.Select('cmdr_groups', 'id, name', '')
        self.group_names.clear()
        if group_rows :
            self.group_names.append(ptl("All"))
            for group_item in group_rows:
                self.group_names.append(group_item[1])
        else:
            self.group_names.append(ptl("None"))

        self.combobox_groups.config(values=self.group_names)
        self.combobox_groups.current(0)   
        if self.select_group != None:
            self.combobox_groups.set(self.select_group['name'])      

        # systems
        if self.select_group != None:
            system_rows = self.db.Select('cmdr_systems', 'star_system, faction_name', f"group_id = {self.select_group['id']}")
        else:
            system_rows = self.db.Select('cmdr_systems', 'star_system', '')

        self.system_names.clear()
        if system_rows :
            self.system_names.append(ptl("All"))
            for system_item in system_rows:
                self.system_names.append(system_item[0])
        else:
            self.system_names.append(ptl("None"))

        self.combobox_systems.config(values=self.system_names)
        self.combobox_systems.current(0)   
        if self.select_system != None:
            self.combobox_systems.set(self.select_system['star_system'])      

        # stations
        # StarSystem, SystemAddress, StationName, StationType, MarketID, DistFromStarLS, StationFaction, StationGovernment, 
        # StationGovernment_Localised, StationEconomy, StationEconomy_Localised, StationEconomies, LandingPads
        if self.select_system != None:
            station_rows = self.db.Select('stations', 'StationName', f"StarSystem = \"{self.select_system['star_system']}\"")
        else:
            station_rows = self.db.Select('stations', 'StationName', '')

        self.station_names.clear()
        if station_rows :
            self.station_names.append(ptl("All"))
            for station_item in station_rows:
                self.station_names.append(station_item[0])
        else:
            self.station_names.append(ptl("None"))

        self.combobox_stations.config(values=self.station_names)
        self.combobox_stations.current(0)   
        if self.select_station != None:
            self.combobox_stations.set(self.select_station['StationName']) 

        # Station Info
            self.station_name_label.config(text=self.select_station['StationName'])
            self.star_system_label.config(text=self.select_station['StarSystem'])
            self.station_type_title.config(text=ptl("Station type : ") + self.select_station['StationType'])
            landingPads = eval(self.select_station['LandingPads'])
            self.landing_pads_title.config(text=ptl("Landing pads : ")+f" L({landingPads['Large']}) M({landingPads['Medium']}) S({landingPads['Small']})")

            stationFaction = eval(self.select_station["StationFaction"])
            self.station_faction_list.config(text=f"{stationFaction['Name']}")

            self.station_distance_label.config(text=ptl("Disctance from star : ") + f"{round(self.select_station['DistFromStarLS'],2)} Ls")
            self.station_government_label.config(text=ptl("Government : ") + f"{self.select_station['StationGovernment_Localised']}")
            stationEconomies = eval(self.select_station["StationEconomies"])
            st_text = ""
            for st in stationEconomies:
                if self.select_station['StationEconomy'] == st['Name'] :
                    self.station_economy_title.config(text=ptl("Station economy : ")+f"{self.select_station['StationEconomy_Localised']}  ({round(st['Proportion'],1)})")
                else:
                    st_text += f"{st['Name_Localised']} : {round(st['Proportion'],1)}\n"
            self.station_economies_list.config(text=st_text)




    def update(self, cmdrname: str, is_beta: bool, system: str, station: str, entry: dict, state: dict):
        system_row = self.db.Select('cmdr_systems', 'star_system', f"star_system = '{system}' ", True)
        if system_row:
            if entry.get("event") == "Docked":
                station_object = self.db.Select('stations', '*', f"UPPER(StarSystem) = \"{entry.get("StarSystem").upper()}\" AND UPPER(StationName) = \"{entry.get("StationName").upper()}\"", True)
                if station_object : 
                    self.db.Delete('stations', f"UPPER(StarSystem) = \"{entry.get("StarSystem").upper()}\" AND UPPER(StationName) = \"{entry.get("StationName").upper()}\"")
                
                self.db.Insert('stations', 'StarSystem, SystemAddress, StationName, StationType, MarketID, DistFromStarLS, StationFaction, StationGovernment, StationGovernment_Localised, StationEconomy, StationEconomy_Localised, StationEconomies, LandingPads', 
                        f"\"{entry.get("StarSystem")}\", {entry.get("SystemAddress")}, \"{entry.get("StationName")}\", \"{entry.get("StationType")}\", {entry.get('MarketID')}, {entry.get("DistFromStarLS")}, \"{entry.get("StationFaction")}\", \"{entry.get("StationGovernment")}\", \"{entry.get("StationGovernment_Localised")}\", \"{entry.get("StationEconomy")}\", \"{entry.get("StationEconomy_Localised")}\", \"{entry.get("StationEconomies")}\", \"{entry.get("LandingPads")}\" ")
                self.update_widgets()

            '''self.StationName = entry.get("StationName")
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
            self.update_widgets()'''