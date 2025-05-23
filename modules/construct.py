
from config import config
import tkinter as tk
import sys
from tkinter import ttk
from pathlib import Path
from modules.db import BGSMini_DB

from tools import ptl

dbg_mode = False

class Construct_Page:
  def __init__(self, parent):
    #podstawa kazdej klasy
    self.app = parent
    self.db = self.app.db

    self.check_completed = tk.IntVar()
    #nowe
    self.select_system = None
    self.systems = []     #nazwy systemow dla combobox
    self.current_object = None
    self.current_object_materials = None
    self.select_object = None
    self.select_object_materials = None
    self.objects = []     #nazwy obiektow dla combobox
    self.select_market = None
    self.select_market_materials = None
    self.markets = []     #nazwy rynkow dla combobox
    self.current_market = None
    self.current_market_materials = None
    #stare
    self.current_system = None
    

  def load_object_materials(self, marketid, starsystem):
    meterial_rows = self.db.Select('object_materials', "name, name_localised, RequiredAmount, ProvidedAmount, Payment", f"market_id = {marketid} ")
    if meterial_rows:
      materials = []
      for material_row in meterial_rows:
        material = {
            "StarSystem"      : starsystem,
            "Name"            : material_row[0],
            "NameLocalised"   : material_row[1],
            "MarketID"        : marketid,
            "RequiredAmount"  : material_row[2], 
            "ProvidedAmount"  : material_row[3], 
            "Payment"         : material_row[4]
        }
        materials.append(material)
      self.select_object_materials = materials
      print("Pobrano materiały dla System ID: "+ str(starsystem) +" i Market ID: "+str(marketid))
    else:
      self.select_object_materials = None
      print("Brak materiałów dla System ID: "+ str(starsystem) +" i Market ID: "+str(marketid))


#aktualizacja zawartosci widgetow
  def update_widgets(self):
    print('Depot Page : begin update_widgets')

    self.frame_system.config(text= ptl("System"))
    self.frame_object.config(text= ptl("Object"))
    self.frame_market.config(text= ptl("Market"))

    self.label_object.config(text= ptl("Object : "))
    self.label_current_object.config(text= ptl("Current : "))
    self.button_current_object_add.config(text= ptl("Add"))
    self.button_current_object_show.config(text= ptl("Show"))
    self.button_object_del.config(text= ptl("Delete"))

    self.label_current_market.config(text= ptl("Current : "))
    self.label_market.config(text= ptl("Market : "))
    self.button_current_market_add.config(text= ptl("Add"))
    self.button_current_market_show.config(text= ptl("Show"))
    self.button_market_del.config(text= ptl("Delete"))

    self.treeview_material_list.heading('#0', text= ptl("Material name"))
    self.treeview_material_list.heading('CS_RequiredAmount', text= ptl("Demand"))
    self.treeview_material_list.heading('CS_ProvidedAmount', text= ptl("Left"))
    self.treeview_material_list.heading('FC_State', text= ptl("Market"))

    self.checkbutton_completed.config(text= ptl("Hide completed content"))


    #frame system
    system_rows = self.db.Select('cmdr_systems', 'star_system', '')
    self.systems = []
    if system_rows :
      self.systems.append(ptl("All"))
      for system_item in system_rows:
        self.systems.append(system_item[0])
    else:
      self.systems.append(ptl("None"))

    self.combobox_systems.config(values=self.systems)
    self.combobox_systems.current(0)
    if self.select_system != None :
      self.combobox_systems.set(self.select_system)

    if dbg_mode :
      print("-> select system : " + str(self.select_system))
      print("-> current object : " + str(self.current_object))
      print("-> select object : " + str(self.select_object))
      print("-> current market : " + str(self.current_market))
      print("-> select market : " + str(self.select_market))
    #---wczytanie listy obiektow -----------------------------------------------------------------------------
       
    self.objects = []
    if self.select_system != None:
      object_rows = self.db.Select('system_objects', 'star_system, stationname, market_id, progress', f"UPPER(star_system) = \"{self.select_system.upper()}\"")
    else:
      object_rows = self.db.Select('system_objects', 'star_system, stationname, market_id, progress', '')
    if object_rows:
      for object_row in object_rows:
        self.objects.append(object_row[1])
        if self.select_object != None:
          if self.select_object['StationName'] == object_row[1]:
            self.select_object = {'StarSystem' : object_row[0],
            'StationName': object_row[1],
            'MarketID' : object_row[2],
            'ConstructionProgress' :  object_row[3] }

      self.combobox_objects.config(state='readonly')
    else:
      self.objects.append(ptl("None"))
      self.combobox_objects.config(state='disabled')

    self.combobox_objects.config(values=self.objects)
    self.combobox_objects.current(0)
    ConstructionProgress = 0
    if self.select_object != None:
      self.combobox_objects.set(self.select_object['StationName'])
      ConstructionProgress = round(self.select_object['ConstructionProgress']*100,2)
      self.label_progress.config(text= ptl("Completed : ") + str(ConstructionProgress) + " %")

    if self.current_object != None:
      self.label_current_object.config(text= ptl("Current object : ") + str(self.current_object['StationName']))
    
    #aktualny rynek
    if self.current_market != None:
      self.label_current_market.config(text=ptl("Current market : ")+str(self.current_market['StationName']))

    #---wczytanie listy rynkow -----------------------------------------------------------------------------
    self.markets = []
    market_rows = self.db.Select('markets', 'market_id, name, station_type', '')
    if market_rows:
      self.markets.append(ptl("None"))
      for market_row in market_rows:
        self.markets.append(market_row[1])
      self.combobox_markets.config(state='readonly')
    else:
      self.markets.append(ptl("None"))
      self.combobox_markets.config(state='disabled')

    self.combobox_markets.config(values=self.markets)
    self.combobox_markets.current(0)
    if self.select_market != None :
      self.combobox_markets.set(self.select_market["StationName"])
    
    #kasowanie listy materialow
    for i in self.treeview_material_list.get_children():
      self.treeview_material_list.delete(i)

    # wczytanie materialow 

   
    #self.select_market_materials = None
    if self.select_market != None: 
      self.select_market_materials = self.db.Select('market_materials', 'name, name_localised, stock', f"market_id = {self.select_market['MarketID']}")
    
    # jezeli jest aktualny obiekt to wlacz przyciski
    if self.current_market == None:
      self.button_current_market_add.config(state='disabled')
      self.button_current_market_show.config(state='disabled')
    else:
      self.button_current_market_add.config(state='normal')
      self.button_current_market_show.config(state='normal')

    #---koniec informacji o obiektach -----------------------------------------------------------------------------
    # jezeli jest aktualny obiekt to wlacz przyciski
    if self.current_object == None:
      self.button_current_object_add.config(state='disabled')
      self.button_current_object_show.config(state='disabled')
    else:
      self.button_current_object_add.config(state='normal')
      self.button_current_object_show.config(state='normal')

    if self.select_object == None:
      return

# jezeli obecny system istnieje 

    self.load_object_materials(self.select_object['MarketID'] , self.select_object['StarSystem'] )
    if self.select_object_materials == None:
      return

    #wyswietlanie listy z object_info
    for material_row in self.select_object_materials:
      m_stock = 0
      if self.select_market_materials != None:
        for market_material in self.select_market_materials:
          if material_row['Name'] == market_material[0] :
            m_stock = market_material[2]
      
      if material_row['RequiredAmount']-material_row['ProvidedAmount'] == 0 :
        if not self.check_completed.get():
          self.treeview_material_list.insert('', 'end', text=material_row['NameLocalised'], values=(format(int(material_row['RequiredAmount']), ',d')+" t", format(int(material_row['RequiredAmount']-material_row['ProvidedAmount']), ',d')+" t", format(int(m_stock), ',d')+" t"))
      else:
        self.treeview_material_list.insert('', 'end', text=material_row['NameLocalised'], values=(format(int(material_row['RequiredAmount']), ',d')+" t", format(int(material_row['RequiredAmount']-material_row['ProvidedAmount']), ',d')+" t", format(int(m_stock), ',d')+" t"))

  #glowna ramka modulu (glowna zakladka)
  def show(self, parent):
    self.parent = parent
    #frames
    self.frame_system = tk.LabelFrame(self.parent, text= ptl("System"))
    self.frame_system.pack(side="top", fill='x')
    self.frame_object = tk.LabelFrame(self.parent, text= ptl("Object"))
    self.frame_object.pack(side="top", fill='x')
    self.frame_market = tk.LabelFrame(self.parent, text= ptl("Market"))
    self.frame_market.pack(side="top", fill='x')
    frame_object_frame1 = tk.Frame(self.frame_object, height=50)
    frame_object_frame1.pack(side='top', fill='x', expand=True)
    frame_object_frame2 = tk.Frame(self.frame_object, height=50)
    frame_object_frame2.pack(side='top', fill='x', expand=True)
    frame_object_frame3 = tk.Frame(self.frame_object, height=50)
    frame_object_frame3.pack(side='top', fill='x', expand=True)
    frame_market_frame1 = tk.Frame(self.frame_market, height=50)
    frame_market_frame1.pack(side='top', fill='x')
    frame_market_frame2 = tk.Frame(self.frame_market, height=50)
    frame_market_frame2.pack(side='top', fill='x')
    frame_show_option = tk.Frame(self.parent, height=50)
    frame_show_option.pack(side='top', fill='x')
  
    #frame_system
    self.combobox_systems = ttk.Combobox(self.frame_system, values = [])
    self.combobox_systems.pack(side='left', fill='x', expand=True)
    self.combobox_systems.config(state='readonly')

    def Select_System_Combo(event):
      system_row = self.db.Select('cmdr_systems', 'star_system', f"UPPER(star_system) = \"{self.combobox_systems.get().upper()}\"", True)
      if system_row:
        self.select_system = self.combobox_systems.get()
      else:
        self.select_system = None
      self.update_widgets()
        

    self.combobox_systems.bind('<<ComboboxSelected>>', Select_System_Combo)

    #frame_object
    self.label_current_object  = tk.Label(frame_object_frame1, text= ptl("Current : "), anchor='w')
    self.label_current_object.pack(side='left', fill='x', expand=True)

    def current_object_add():
      if self.current_object != None:
        self.select_object = self.current_object
        row = self.db.Select('system_objects', 'star_system, market_id', f"market_id = {self.current_object['MarketID']}", True)
        if not row:
          self.db.Insert('system_objects', 'star_system, stationname, market_id, progress', f"\"{self.current_object['StarSystem']}\", \"{self.current_object['StationName']}\", {self.current_object['MarketID']}, {self.current_object['ConstructionProgress']}")
        self.update_widgets()

    self.button_current_object_add = tk.Button(frame_object_frame1, text= ptl("Add"), command=current_object_add)
    self.button_current_object_add.pack(side='left', expand=False)

    def current_object_show():
      if self.current_object != None:
        self.select_object = self.current_object
        self.select_object_materials = self.current_object_materials
        self.update_widgets()

    self.button_current_object_show = tk.Button(frame_object_frame1, text= ptl("Show"), command=current_object_show)
    self.button_current_object_show.pack(side='left', expand=False)

    self.label_object = tk.Label(frame_object_frame2, text= ptl("Object : "), anchor='w')
    self.label_object.pack(side='left', expand=False)

    self.combobox_objects = ttk.Combobox(frame_object_frame2, values = [])
    #self.combobox_objects.config(state='disabled')
    self.combobox_objects.config(state='readonly')
    self.combobox_objects.pack(side='left', fill='x', expand=True)
    
    def Select_Obj_Combo(event):
      if self.select_system != None:
        object_row = self.db.Select('system_objects', 'star_system, stationname, market_id, progress', f"stationname = '{self.combobox_objects.get()}' AND UPPER(star_system) = '{self.select_system.upper()}'", True)
      else:
        object_row = self.db.Select('system_objects', 'star_system, stationname, market_id, progress', f"stationname = '{self.combobox_objects.get()}' ", True)

      if object_row:
        self.select_object = {'StarSystem' : object_row[0],
        'StationName': object_row[1],
        'MarketID' : object_row[2],
        'ConstructionProgress' :  object_row[3] }
      
        self.load_object_materials(self.select_object['MarketID'] , self.select_object['StarSystem'] )
        self.update_widgets()

    self.combobox_objects.bind('<<ComboboxSelected>>', Select_Obj_Combo)

    def select_object_remove():
      if self.select_object != None :
        self.db.Delete('system_objects', f"stationname = \"{self.select_object['StationName']}\" AND market_id = {self.select_object['MarketID']}")
        self.db.Delete('object_materials', f"market_id = {self.select_object['MarketID']}")
        self.select_object = None
        self.select_object_materials = None
        self.update_widgets()

    self.button_object_del = tk.Button(frame_object_frame2, text= ptl("Delete"), command=select_object_remove)
    self.button_object_del.pack(side='left', expand=False)
    
    self.label_progress = tk.Label(frame_object_frame3, text= ptl("Completed : "), anchor='w')
    self.label_progress.pack(side='left', anchor='w')


    #----------------
    self.label_current_market  = tk.Label(frame_market_frame1, text= ptl("Current : "), anchor='w')
    self.label_current_market.pack(side='left', fill='x', expand=True)

    def current_market_add():
      if self.current_market != None :
        self.app.market.load_journal()
        self.select_market = self.current_market
        self.app.market.save()
        self.update_widgets()

    self.button_current_market_add = tk.Button(frame_market_frame1, text= ptl("Add"), command=current_market_add)
    self.button_current_market_add.pack(side='left', expand=False)

    def current_market_show():
      if self.current_market != None:
        self.app.market.load_journal()
        self.current_market_materials = self.app.market.get_commodity_names() 
        self.select_market = self.current_market
        self.select_market_materials = self.current_market_materials 
        self.update_widgets()

    self.button_current_market_show = tk.Button(frame_market_frame1, text= ptl("Show"), command=current_market_show)
    self.button_current_market_show.pack(side='left', expand=False)

    self.label_market = tk.Label(frame_market_frame2, text= ptl("Market : "), anchor='w')
    self.label_market.pack(side='left', expand=False)

    self.combobox_markets = ttk.Combobox(frame_market_frame2, values = [])
    self.combobox_markets.config(state='readonly')
    self.combobox_markets.pack(side='left', fill='x', expand=True)
    
    def Select_Market_Combo(event):
      market_row = self.db.Select('markets', 'name, market_id, station_type', f"name = \"{self.combobox_markets.get()}\"", True)
      self.select_market = None
      if market_row : 
        self.select_market = {'StationName' : market_row[0], 'MarketID' : market_row[1], 'StationType' :  market_row[2]} 
      self.update_widgets()
    
    self.combobox_markets.bind('<<ComboboxSelected>>', Select_Market_Combo)

    def market_delete():
      if self.select_market != None:
        self.root.market.delete(self.select_market['MarketID'])
        self.select_market = None
        self.select_market_materials = None
        self.update_widgets()

    self.button_market_del = tk.Button(frame_market_frame2, text= ptl("Delete"), command=market_delete)
    self.button_market_del.pack(side='left', expand=False)

    def update_check_completed():
      self.update_widgets()
    self.checkbutton_completed = tk.Checkbutton(frame_show_option, text= ptl("Hide completed content"), variable=self.check_completed, onvalue=1, offvalue=0, command=update_check_completed)
    self.checkbutton_completed.pack(side='top', anchor='w')
    
    #---------------------------------------------------------------------


    #current markets

    

    #main
    self.mainframe = tk.Frame(self.parent)
    self.mainframe.pack(expand = True, fill ="both")


    self.treeview_material_list = ttk.Treeview(self.mainframe,columns=('CS_RequiredAmount', 'CS_ProvidedAmount', 'FC_State'), selectmode="browse")
    self.treeview_material_list.pack(side="bottom", expand = True, fill ="both")

    self.treeview_material_list.column('#0', minwidth=50, width=120)
    self.treeview_material_list.column('CS_RequiredAmount', minwidth=20, width=50)
    self.treeview_material_list.column('CS_ProvidedAmount', minwidth=20, width=50)
    self.treeview_material_list.column('FC_State', minwidth=20, width=50)

    self.update_widgets()

  #aktualizacja ze zdarzenia dziennika gry
  def update(self, cmdrname: str, is_beta: bool, system: str, station: str, entry: dict, state: dict):
    
    self.current_system = system
    #sprawdzam aktualny rynek
     #"event":"Market", "MarketID":3710784768, "StationName":"TNB-46F", "StationType":"FleetCarrier"
    if entry['event'] == 'Market':
      self.current_market = {'StationName' : entry['StationName'], 'MarketID' : entry['MarketID'], 'StationType' : entry['StationType']}

    # sprawdzam czy zadokowano
    #if entry['event'] == "Docked":
  

    if entry['event'] == 'Undocked':
      self.current_object = None
      self.current_object_materials = None

    # sprawdzam czy jestem na obiekcie kolonizacyjnym
    if entry['event'] == 'ColonisationConstructionDepot' :

      self.current_object = {
        'StarSystem' : system, 
        'StationName' : station, 
        'MarketID' : entry['MarketID'], 
        'ConstructionProgress' : entry['ConstructionProgress']}
      
      check_object = self.db.Select('system_objects', '*', f"market_id = {self.current_object['MarketID']}", True)
      if check_object : 
        self.db.Delete('object_materials', f"market_id = {self.current_object['MarketID']}")
        self.db.Update('system_objects', f"progress = {self.current_object['ConstructionProgress']}", f"market_id ={self.current_object['MarketID']}")

      materials = []
      for material_row in entry['ResourcesRequired'] :
        material = {
            "StarSystem"      : self.current_object['StarSystem'],
            "Name"            : material_row['Name'][1:-6],
            "NameLocalised"   : material_row['Name_Localised'],
            "MarketId"        : self.current_object['MarketID'],
            "RequiredAmount"  : material_row['RequiredAmount'], 
            "ProvidedAmount"  : material_row['ProvidedAmount'], 
            "Payment"         : material_row['Payment']
        }
        materials.append(material)

        if check_object:
            self.db.Insert('object_materials', 'star_system, name, name_localised, market_id, RequiredAmount, ProvidedAmount, Payment', f"\"{self.current_object['StarSystem']}\", \"{material['Name']}\", \"{material_row['Name_Localised']}\", {self.current_object['MarketID']}, {material_row['RequiredAmount']}, {material_row['ProvidedAmount']}, {material_row['Payment']}")
      self.current_object_materials = materials    
    self.update_widgets()

