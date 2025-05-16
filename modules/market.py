import json
from os.path import join
from typing import Dict, List

import tkinter as tk
from tkinter import Tk
from tkinter import ttk

from config import config
from tools import ptl

FILENAME_MARKET = "Market.json"
FILENAME_CARGO = "Cargo.json"

dbg_mode = False

class Market_Page:
    label_current_market = None
    button_current_market_add = None
    button_current_market_show = None
    button_select_market_delete = None
    combobox_markets = None
    treeview_commodities = None

    select_market = None
    select_market_materials = None
    markets = []     #nazwy rynkow dla combobox
    current_market = None
    current_market_materials = None

    check_demand = tk.IntVar()
    check_stock = tk.IntVar()

    def __init__(self, parent):
        #podstawa kazdej klasy
        self.app = parent
        self.db = self.app.db

        self.name:str = None
        self.id:int = None
        self.new_market = True
        self.station_type:str = None
        self.star_system:str = None
        self.commodities:Dict = {}
        self.commodity_names = [] 

        self.vessel :str = None
        self.count = None
        self.cargo_commodity_names = []

        self.check_demand.set(1)
        self.check_stock.set(1)


    #glowna ramka modulu (glowna zakladka)
    def show(self, parent):
        self.parent = parent
    
        #Commodities
        self.frame_markets = tk.LabelFrame(self.parent)
        self.frame_markets.pack(fill="both", expand=True)

        child_frame1 = tk.Frame(self.frame_markets)
        child_frame1.pack(side='top', fill='x')
        child_frame2 = tk.Frame(self.frame_markets)
        child_frame2.pack(side='top', fill='x')
        self.child_frame3 = tk.LabelFrame(self.frame_markets)
        self.child_frame3.pack(side='top', fill='x')        
        child_frame31 = tk.Frame(self.frame_markets)
        child_frame31.pack(side='top', fill='both', expand=True)
         
        self.label_current_market = tk.Label(child_frame1, anchor='w')
        self.label_current_market.pack(padx=5, side='left', fill='x', expand=True)

        def current_market_add():
            if self.current_market != None :
                self.app.market.load_journal()
                self.select_market = self.current_market
                self.app.market.save()
                self.update_widgets()
        
        def current_market_show():
            if self.current_market != None:
                self.app.market.load_journal()
                self.current_market_materials = self.app.market.get_commodity_names() 
                self.select_market = self.current_market
                self.select_market_materials = self.current_market_materials 
                self.update_widgets()

        self.button_current_market_add = tk.Button(child_frame1, command=current_market_add)
        self.button_current_market_add.pack(side='left', expand=False)
        self.button_current_market_show = tk.Button(child_frame1, command=current_market_show)
        self.button_current_market_show.pack(side='left', expand=False)


        self.combobox_markets = ttk.Combobox(child_frame2)
        self.combobox_markets.config(state='readonly')
        self.combobox_markets.pack(side='left', fill='x', expand=True)

        def select_market_combo(event):
            market_row = self.db.Select('markets', 'name, market_id, station_type', f"name = \"{self.combobox_markets.get()}\"", True)
            self.select_market = None
            if market_row : 
                self.select_market = {'StationName' : market_row[0], 'MarketID' : market_row[1], 'StationType' :  market_row[2]} 
            self.update_widgets()
            
        self.combobox_markets.bind('<<ComboboxSelected>>', select_market_combo)

        def market_delete():
            if self.select_market != None:
                self.delete(self.select_market['MarketID'])
                self.select_market = None
                self.select_market_materials = None
                self.update_widgets()

        self.button_select_market_delete = tk.Button(child_frame2, command=market_delete)
        self.button_select_market_delete.pack(side='left', expand=False)

        #----------------------------------------------------------------------------------------------------------------------------------------------------
        def update_check():
            self.update_widgets()

        def treeview_OnDoubleClick(event):
            selected = self.treeview_commodities.focus() 
            copiedText = self.treeview_commodities.item(selected)['text']
            print(copiedText)
            r = Tk()
            r.withdraw()
            r.clipboard_clear()
            r.clipboard_append(copiedText)
            r.destroy()

        self.checkbutton_demand = tk.Checkbutton(self.child_frame3, text='Pokaż skup', variable=self.check_demand, onvalue=1, offvalue=0, command=update_check)
        self.checkbutton_demand.pack(side='left', anchor='w')
        self.checkbutton_demand.flash()
        self.checkbutton_stock = tk.Checkbutton(self.child_frame3, text='Pokaż sprzedaż', variable=self.check_stock, onvalue=1, offvalue=0, command=update_check)
        self.checkbutton_stock.pack(side='left', anchor='w')
        self.checkbutton_stock.flash()
        self.button_commodities_search = tk.Button(self.child_frame3, text="Szukaj", command=self.commodities_search)
        self.button_commodities_search.pack(side='right', expand=False)

        self.treeview_commodities = ttk.Treeview(child_frame31, columns=('Stock', 'Demand', 'Cargo'))
        self.treeview_commodities.heading('#0', text= 'Nazwa')
        self.treeview_commodities.column('#0', minwidth=120)
        self.treeview_commodities.column('Demand', minwidth=70, width=70)
        self.treeview_commodities.column('Stock', minwidth=30, width=30)
        self.treeview_commodities.column('Cargo', minwidth=30, width=30)
        self.treeview_commodities.tag_configure('cargo', background='palegreen1')
        self.treeview_commodities.pack(fill ="both", expand = True)
        self.treeview_commodities.bind("<Double-1>", treeview_OnDoubleClick)

        self.update_widgets()

    def update_widgets(self):
        #aktualny rynek

        self.frame_markets.config(text= ptl("Markets"))

        self.child_frame3.config(text= ptl("Commodities"))
        self.label_current_market.config(text= ptl("Current : "))
        self.button_current_market_add.config(text= ptl("Add"))
        self.button_current_market_show.config(text= ptl("Show"))
        self.button_select_market_delete.config(text= ptl("Delete"))

        self.checkbutton_demand.config(text = ptl("Show demand"))
        self.checkbutton_stock.config(text = ptl("Show stock"))
        self.button_commodities_search.config(text= ptl("Search"))

        self.treeview_commodities.heading('Demand', text= ptl("Demand"))
        self.treeview_commodities.heading('Stock', text= ptl("Stock"))
        self.treeview_commodities.heading('Cargo', text= ptl("On cargo"))

        self.load_journal()
        if self.current_market != None:
            self.label_current_market.config(text="Aktualny :"+str(self.current_market['StationName']))
        
        #---wczytanie listy rynkow -----------------------------------------------------------------------------
        self.markets = []
        market_rows = self.db.Select('markets', 'market_id, name, station_type', '')
        if market_rows:
            self.markets.append(ptl("None"))
            self.combobox_markets.config(state='readonly')
            for market_row in market_rows:
                self.markets.append(market_row[1])
        else:
            self.markets.append(ptl("None"))
            self.combobox_markets.config(state='disabled')

        self.combobox_markets.config(values=self.markets)
        self.combobox_markets.current(0)
        if self.select_market != None :
            self.combobox_markets.set(self.select_market["StationName"])

        #kasowanie listy materialow
        for i in self.treeview_commodities.get_children():
            self.treeview_commodities.delete(i)

        if self.select_market != None: 
            self.select_market_materials = self.db.Select('market_materials', 'name, name_localised, stock, Demand', f"market_id = {self.select_market['MarketID']}")
    
        # jezeli jest aktualny obiekt to wlacz przyciski
        if self.current_market == None:
            self.button_current_market_add.config(state='disabled')
            self.button_current_market_show.config(state='disabled')
        else:
            self.button_current_market_add.config(state='normal')
            self.button_current_market_show.config(state='normal')

        if dbg_mode :     
            print("Market module:")
            print("-> current market : " + str(self.current_market))
            print("-> select market : " + str(self.select_market))

        #wyswietlanie listy materialow
        if self.select_market_materials != None:
            for material_row in self.select_market_materials:
                cargo = 0
                if self.cargo_commodity_names != None:
                    for cargo_material in self.cargo_commodity_names:
                        if material_row[0] == cargo_material['Name'] :
                            cargo = cargo_material['Count']
                if (self.check_demand.get() == 1 and material_row[3] != 0) or (self.check_stock.get() == 1 and material_row[2] != 0):
                    if cargo > 0: 
                        self.treeview_commodities.insert('', 'end', text=material_row[1], values=(material_row[2], material_row[3], cargo), tag="cargo")
                    else:
                        self.treeview_commodities.insert('', 'end', text=material_row[1], values=(material_row[2], material_row[3], cargo))

               
    def commodities_search(self):
        material_name = tk.StringVar()
        search_wnd = tk.Toplevel(self.parent)
        commodities_frame = tk.Frame(search_wnd)
        treeview_commodities = ttk.Treeview(commodities_frame, columns=('Star_System','Station_Type', 'Stock','BuyPrice', 'SellPrice'))

        def close():
            search_wnd.destroy()
            search_wnd.update()
        
        def search(event):
            commodities_rows = self.db.Select('market_materials mm JOIN markets m ON mm.market_id = m.market_id','m.name AS market_name, m.star_system, m.station_type, mm.stock, mm.BuyPrice, mm.SellPrice', f"UPPER(mm.name) LIKE '%{commoditie_name_entry.get().upper()}%'")
            if commodities_rows:
                for i in treeview_commodities.get_children():
                    treeview_commodities.delete(i)
                #('Wagner Station', 'Thrite', 'Coriolis', 0, 0, 857)
                for commodities_row in commodities_rows:
                    treeview_commodities.insert('', 'end', text=commodities_row[0], values=(commodities_row[1], commodities_row[2], commodities_row[3], commodities_row[4], commodities_row[5]))

        def treeview_OnDoubleClick(event):
            selected = treeview_commodities.focus() 
            copiedText = treeview_commodities.item(selected)['text']
            print(copiedText)
            r = Tk()
            r.withdraw()
            r.clipboard_clear()
            r.clipboard_append(copiedText)
            r.destroy()

        search_wnd.minsize(400,500)
        search_wnd.title(ptl("Search commoditie"))
        search_wnd.resizable(width=False, height=False)
        label_commoditie_title = tk.Label(search_wnd, text= ptl("Commoditie name :"), anchor='w')
        label_commoditie_title.pack(padx=5, side='top', fill='x')
        frame = tk.Frame(search_wnd)
        frame.pack(padx=5, side='top', fill='x')
        commoditie_name_entry = tk.Entry(frame, textvariable=material_name)
        commoditie_name_entry.pack(side='left', fill='x', expand=True)
        commoditie_name_entry.focus()
        self.button_select_market_delete = tk.Button(frame, text= ptl("Close"), command=close)
        self.button_select_market_delete.pack(side='right')
        commodities_frame.pack(padx=5, fill='both', expand = True)
        
        treeview_commodities.heading('#0', text= ptl("Station name"))
        treeview_commodities.heading('Star_System', text= ptl("System name"))
        treeview_commodities.heading('Station_Type', text= ptl("Station type"))
        treeview_commodities.heading('Stock', text= ptl("Stock"))
        treeview_commodities.heading('BuyPrice', text= ptl("Buy price"))
        treeview_commodities.heading('SellPrice', text= ptl("Sell price"))
        treeview_commodities.pack(fill ="both", expand = True)
        treeview_commodities.bind("<Double-1>", treeview_OnDoubleClick)
        search_wnd.bind("<Key>", search)


    def create_table(self):
        self.db.CreateTables()

    def _clear_data(self):
        self.name = None
        self.id = None
        self.station_type:str = None
        self.star_system:str = None
        self.commodities = {}
        self.commodity_names.clear()
        #cargo
        self.vessel :str = None
        self.count = None
        self.cargo_commodity_names.clear()
        
    # pobieranie z pliku Market.json
    def load_journal(self):
        self._clear_data()
        self._parse()
        self._parse_cargo()

    def delete(self, marketid):
        self._clear_data()
        self.db.Delete('markets', f"market_id = {marketid} ")
        self.db.Delete('market_materials', f"market_id = {marketid} ")

    # Wczytanie z bazy danych
    def load(self, marketid):
        self._clear_data()
        market_row = self.db.Select('markets', 'name, star_system, station_type', f"market_id = {marketid} ", True)
        
        self.id = marketid
        self.name = market_row[0][0]
        self.star_system = market_row[0][1]
        self.station_type = market_row[0][2]
        
        material_rows = self.db.Select('market_materials', 'name, name_localised, category, stock, Demand, BuyPrice, SellPrice', f"market_id = {marketid}")
        for material_row in material_rows:
            material  = {
                        'Id'                : int,
                        'Station_Name'      : str,
                        'Station_Type'      : str,
                        'Star_System'       : str,
                        'Name'              : str, 
                        'Name_Localised'    : str,
                        'Category'          : str,
                        'Stock'             : int,
                        'Demand'            : int, 
                        'BuyPrice'          : int,
                        'SellPrice'         : int
                    }
            material['Name'] = material_row[0]
            material['Name_Localised'] = material_row[1]
            material['Category'] = material_row[2]
            material['Stock'] = material_row[3]
            material['Demand'] = material_row[4]
            material['BuyPrice'] = material_row[5]
            material['SellPrice'] = material_row[6]
            self.commodity_names.append(material)

    # Zapisanie do bazy danych
    def save(self):
        if self.name and self.id and self.star_system and self.station_type:
            self.db.Delete('markets', f"market_id = {self.id}")
            self.db.Insert('markets', 'market_id, name, star_system, station_type', f"{self.id}, \"{self.name}\", \"{self.star_system}\", \"{self.station_type}\"  ")
            self.db.Delete('market_materials', f"market_id = {self.id}")
            for material_item in self.commodity_names:
                self.db.Insert('market_materials', 'market_id, name, name_localised, category, stock, Demand, BuyPrice, SellPrice', f"{self.id}, \"{material_item['Name']}\", \"{material_item['Name_Localised']}\", \"{material_item['Category']}\", {material_item['Stock']}, {material_item['Demand']}, {material_item['BuyPrice']}, {material_item['SellPrice']} ")
        
    # parsowanie pliku
    def _parse(self):
        journal_dir:str = config.get_str('journaldir') or config.default_journal_dir
        if not journal_dir: return

        try:
            with open(join(journal_dir, FILENAME_MARKET), 'rb') as file:
                data:bytes = file.read().strip()
                if not data: return

                json_data = json.loads(data)
                items:List = json_data['Items']

                self.name = json_data['StationName']
                self.id = json_data['MarketID']
                self.station_type = json_data['StationType']
                self.star_system = json_data['StarSystem']
        
                for item in items:
                    material  = {
                        'Id'                : int,
                        'Station_Name'      : str,
                        'Station_Type'      : str,
                        'Star_System'       : str,
                        'Name'              : str, 
                        'Name_Localised'    : str,
                        'Category'          : str,
                        'Stock'             : int, 
                        'Demand'            : int, 
                        'BuyPrice'          : int,
                        'SellPrice'         : int
                    }
                    material['Name'] = item.get('Name', "")[1:-6] # Remove leading "$" and trailing "_name;"
                    material['Name_Localised'] =  item.get('Name_Localised', "")
                    material['Category'] = item.get('Category', "")[17:-1] 
                    material['Stock'] = item.get('Stock', 0)
                    material['Demand'] = item.get('Demand', 0)
                    material['BuyPrice'] = item.get('BuyPrice', 0)
                    material['SellPrice'] = item.get('SellPrice', 0)
                    if material['Name'] == "": continue
                    self.commodity_names.append(material)

        except Exception as e:
            print(f"Unable to load {FILENAME_MARKET} from the player journal folder")


    def get_market_id(self) -> int:
        return self.id
    
    def get_market_name(self) -> str:
        return self.name
    
    def get_market_starsystem(self) -> str:
        return self.star_system
    
    def get_market_stationtype(self) -> str:
        return self.station_type

    def get_commodity_names(self) -> []:
        return self.commodity_names
    
    def market_is_new(self):
        return self.new_market

    def _parse_cargo(self):
        journal_dir:str = config.get_str('journaldir') or config.default_journal_dir
        if not journal_dir: return

        try:
            with open(join(journal_dir, FILENAME_CARGO), 'rb') as file:
                data:bytes = file.read().strip()
                if not data: return

                json_data = json.loads(data)
                items:List = json_data['Inventory']

                self.vessel = json_data['Vessel']
                self.count = json_data['Count']
        
                for item in items:
                    material  = {
                        'Name'          : str,
                        'Count'         : int,
                        'Stolen'        : int,
                    }
                    material['Name'] = item.get('Name',"") 
                    material['Count'] = item.get('Count', 0)
                    material['Stolen'] = item.get('Stolen', 0)
                    if material['Name'] == "": continue
                    self.cargo_commodity_names.append(material)

        except Exception as e:
            print(f"Unable to load {FILENAME_CARGO} from the player journal folder")

    def get_cargo_commodity_names(self) -> []:
        return self.cargo_commodity_names

    def update(self, cmdrname: str, is_beta: bool, system: str, station: str, entry: dict, state: dict):
        #"event":"Market", "MarketID":3710784768, "StationName":"TNB-46F", "StationType":"FleetCarrier"
        if entry['event'] == 'Market':      
            self.current_market = {'StationName' : entry['StationName'], 'MarketID' : entry['MarketID'], 'StationType' : entry['StationType']}
            market_row = self.db.Select('markets', 'name, star_system, station_type', f"market_id = {entry['MarketID']} ", True)    
            if market_row:
                self.load_journal()
                self.save()
        return