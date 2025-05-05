
from config import config
import tkinter as tk
import sys
from tkinter import ttk
from pathlib import Path
from module_db import BGSMini_DB


this = sys.modules[__name__]
class Depot_Page:
  def __init__(self, logger, root):
    self.plugin_dir = root.plugin_dir
    self.logger = logger
    self.root = root
    self.config = root.config
    self.check_completed = tk.IntVar()
    self.db = BGSMini_DB(root.plugin_dir)
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
    #frame system
    system_rows = self.db.Select('cmdr_systems', 'star_system', '')
    self.systems = []
    if system_rows :
      self.systems.append("Wszystkie")
      for system_item in system_rows:
        self.systems.append(system_item[0])
    else:
      self.systems.append("Brak")

    self.combobox_systems.config(values=self.systems)
    self.combobox_systems.current(0)
    if self.select_system != None :
      self.combobox_systems.set(self.select_system)


    print("-> select system : " + str(self.select_system))
    print("-> current object : " + str(self.current_object))
    print("-> select object : " + str(self.select_object))
    print("-> current market : " + str(self.current_market))
    print("-> select market : " + str(self.select_market))
    #---wczytanie listy obiektow -----------------------------------------------------------------------------
       
    self.objects = []
    if self.select_system != None:
      object_rows = self.db.Select('system_objects', 'star_system, stationname, stationname_localised, market_id, progress', f"star_system = \"{self.select_system}\"")
    else:
      object_rows = self.db.Select('system_objects', 'star_system, stationname, stationname_localised, market_id, progress', '')
    if object_rows:
      for object_row in object_rows:
        self.objects.append(object_row[1])
      self.combobox_objects.config(state='readonly')
    else:
      self.objects.append("Brak")
      self.combobox_objects.config(state='disabled')

    self.combobox_objects.config(values=self.objects)
    self.combobox_objects.current(0)
    ConstructionProgress = 0
    if self.select_object != None:
      self.combobox_objects.set(self.select_object['StationName'])
      ConstructionProgress = round(self.select_object['ConstructionProgress']*100,2)
      self.label_progress.config(text="Procent ukończenia : " + str(ConstructionProgress) + " %")

    if self.current_object != None:
      self.label_current_object.config(text="Aktualny obiekt :" + str(self.current_object['StationName']))
    
    #aktualny rynek
    if self.current_market != None:
      self.label_current_market.config(text="Aktualny rynek :"+str(self.current_market['StationName']))

    #---wczytanie listy rynkow -----------------------------------------------------------------------------
    self.markets = []
    market_rows = self.db.Select('markets', 'market_id, name, station_type', '')
    if market_rows:
      self.markets.append("Żaden")
      for market_row in market_rows:
        self.markets.append(market_row[1])
      self.combobox_markets.config(state='readonly')
    else:
      self.markets.append("Brak")
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
          self.treeview_material_list.insert('', 'end', text=material_row['NameLocalised'], values=(material_row['RequiredAmount'], material_row['RequiredAmount']-material_row['ProvidedAmount'], m_stock))
      else:
        self.treeview_material_list.insert('', 'end', text=material_row['NameLocalised'], values=(material_row['RequiredAmount'], material_row['RequiredAmount']-material_row['ProvidedAmount'], m_stock))

  #glowna ramka modulu (glowna zakladka)
  def show(self, parent):
    self.parent = parent
    #frames
    frame_system = tk.LabelFrame(self.parent, text="System")
    frame_system.pack(side="top", fill='x')
    frame_object = tk.LabelFrame(self.parent, text="Obiekt")
    frame_object.pack(side="top", fill='x')
    frame_market = tk.LabelFrame(self.parent, text="Rynek")
    frame_market.pack(side="top", fill='x')
    frame_object_frame1 = tk.Frame(frame_object, height=50)
    frame_object_frame1.pack(side='top', fill='x', expand=True)
    frame_object_frame2 = tk.Frame(frame_object, height=50)
    frame_object_frame2.pack(side='top', fill='x', expand=True)
    frame_object_frame3 = tk.Frame(frame_object, height=50)
    frame_object_frame3.pack(side='top', fill='x', expand=True)
    frame_market_frame1 = tk.Frame(frame_market, height=50)
    frame_market_frame1.pack(side='top', fill='x')
    frame_market_frame2 = tk.Frame(frame_market, height=50)
    frame_market_frame2.pack(side='top', fill='x')
    frame_show_option = tk.Frame(self.parent, height=50)
    frame_show_option.pack(side='top', fill='x')
  
    #frame_system
    self.combobox_systems = ttk.Combobox(frame_system, values = [])
    self.combobox_systems.pack(side='left', fill='x', expand=True)
    self.combobox_systems.config(state='readonly')

    def Select_System_Combo(event):
      system_row = self.db.Select('cmdr_systems', 'star_system', f"star_system = \"{self.combobox_systems.get()}\"", True)
      if system_row:
        self.select_system = self.combobox_systems.get()
      else:
        self.select_system = None
      self.update_widgets()
        

    self.combobox_systems.bind('<<ComboboxSelected>>', Select_System_Combo)

    #frame_object
    self.label_current_object  = tk.Label(frame_object_frame1, text="Aktualny :", anchor='w')
    self.label_current_object.pack(side='left', fill='x', expand=True)

    def current_object_add():
      if self.current_object != None:
        self.select_object = self.current_object
        row = self.db.Select('system_objects', 'star_system, market_id', f"market_id = {self.current_object['MarketID']}", True)
        if not row:
          self.db.Insert('system_objects', 'star_system, stationname, market_id, progress', f"\"{self.current_object['StarSystem']}\", \"{self.current_object['StationName']}\", {self.current_object['MarketID']}, {self.current_object['ConstructionProgress']}")
        self.update_widgets()

    self.button_current_object_add = tk.Button(frame_object_frame1, text="Dodaj", command=current_object_add)
    self.button_current_object_add.pack(side='left', expand=False)

    def current_object_show():
      if self.current_object != None:
        self.select_object = self.current_object
        self.select_object_materials = self.current_object_materials
        self.update_widgets()

    self.button_current_object_show = tk.Button(frame_object_frame1, text="Pokaż", command=current_object_show)
    self.button_current_object_show.pack(side='left', expand=False)

    label_object = tk.Label(frame_object_frame2, text="Obiekt :", anchor='w')
    label_object.pack(side='left', expand=False)

    self.combobox_objects = ttk.Combobox(frame_object_frame2, values = [])
    #self.combobox_objects.config(state='disabled')
    self.combobox_objects.config(state='readonly')
    self.combobox_objects.pack(side='left', fill='x', expand=True)
    
    def Select_Obj_Combo(event):
      if self.select_system != None:
        object_row = self.db.Select('system_objects', 'star_system, stationname, market_id, progress', f"stationname = '{self.combobox_objects.get()}' AND star_system = '{self.select_system}'", True)
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
      self.db.Delete('system_objects', f"stationname = \"{self.select_object['StationName']}\" AND market_id = {self.select_object['MarketID']}")
      self.db.Delete('object_materials', f"market_id = {self.select_object['MarketID']}")
      self.select_object = None
      self.select_object_materials = None
      self.update_widgets()

    button_object_del = tk.Button(frame_object_frame2, text="Usuń", command=select_object_remove)
    button_object_del.pack(side='left', expand=False)
    
    self.label_progress = tk.Label(frame_object_frame3, text="Procent ukończenia :", anchor='w')
    self.label_progress.pack(side='left', anchor='w')


    #----------------
    self.label_current_market  = tk.Label(frame_market_frame1, text="Aktualny rynek :", anchor='w')
    self.label_current_market.pack(side='left', fill='x', expand=True)

    def current_market_add():
      if self.current_market != None :
        self.root.market.load_journal()
        self.select_market = self.current_market
        self.root.market.save()
        self.update_widgets()

    self.button_current_market_add = tk.Button(frame_market_frame1, text="Dodaj", command=current_market_add)
    self.button_current_market_add.pack(side='left', expand=False)

    def current_market_show():
      if self.current_market != None:
        self.root.market.load_journal()
        self.current_market_materials = self.root.market.get_commodity_names() 
        self.select_market = self.current_market
        self.select_market_materials = self.current_market_materials 
        self.update_widgets()

    self.button_current_market_show = tk.Button(frame_market_frame1, text="Pokaż", command=current_market_show)
    self.button_current_market_show.pack(side='left', expand=False)

    label_market = tk.Label(frame_market_frame2, text="Rynek :", anchor='w')
    label_market.pack(side='left', expand=False)

    self.combobox_markets = ttk.Combobox(frame_market_frame2, values = [])
    self.combobox_markets.config(state='readonly')
    self.combobox_markets.pack(side='left', fill='x', expand=True)
    
    def Select_Market_Combo(event):
      market_row = self.db.Select('markets', 'name, market_id', f"name = \"{self.combobox_markets.get()}\"", True)
      self.select_market = None
      if market_row : 
        self.select_market = {'StationName' : market_row[0], 'MarketID' : market_row[1]} 
      self.update_widgets()
    
    self.combobox_markets.bind('<<ComboboxSelected>>', Select_Market_Combo)

    def market_delete():
      if self.select_market != None:
        self.root.market.delete(self.select_market['MarketID'])
        self.select_market = None
        self.select_market_materials = None
        self.update_widgets()

    button_market_del = tk.Button(frame_market_frame2, text="Usuń", command=market_delete)
    button_market_del.pack(side='left', expand=False)

    def update_check_completed():
      self.update_widgets()
    self.checkbutton_completed = tk.Checkbutton(frame_show_option, text='Ukrywaj zasypane materiały', variable=self.check_completed, onvalue=1, offvalue=0, command=update_check_completed)
    self.checkbutton_completed.pack(side='top', anchor='w')
    
    #---------------------------------------------------------------------


    #current markets

    

    #main
    self.mainframe = tk.Frame(self.parent)
    self.mainframe.pack(expand = True, fill ="both")


    self.treeview_material_list = ttk.Treeview(self.mainframe,columns=('CS_RequiredAmount', 'CS_ProvidedAmount', 'FC_State'))
    self.treeview_material_list.pack(side="bottom", expand = True, fill ="both")
    self.treeview_material_list.heading('#0', text= 'Materiał')
    self.treeview_material_list.heading('CS_RequiredAmount', text= 'Wymagane')
    self.treeview_material_list.heading('CS_ProvidedAmount', text= 'Pozostało')
    self.treeview_material_list.heading('FC_State', text= 'Rynek')
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




      #for ResourcesRequired in entry["ResourcesRequired"]:
      #  self.db.Insert("object_materials", "market_id, name_localised, system_id, RequiredAmount, ProvidedAmount, Payment", f"{marketid}, \"{ResourcesRequired["Name"]}\", \"{ResourcesRequired["Name_Localised"]}\", {ResourcesRequired["RequiredAmount"]}, {ResourcesRequired["ProvidedAmount"]}, {ResourcesRequired["Payment"]} ")
   # print(entry['market'])

#pierw ten event daje nazwe obiektu:
    # "event":"SupercruiseDestinationDrop"
    #"Type_Localised":"System Colonisation Ship"
    #"MarketID":3953544706

    #"event":"Docked"
    #"StationName_Localised":"System Colonisation Ship"
    #"StarSystem":"HR 8222"
    # "SystemAddress":112975660228
    # "MarketID":3953544706

#ten event daje wskaznik postepu danego obiektu + materialy 
#materialy nalezy zapisac do osobnej tabelki i przypisac do marketid
    #"event":"ColonisationConstructionDepot"
    #"MarketID":3953544706
    #"ConstructionProgress":0.000000
    #"ResourcesRequired":  []  { "Name":"$aluminium_name;", "Name_Localised":"Aluminium", "RequiredAmount":12003, "ProvidedAmount":0, "Payment":3239 }

#fleet carier
#i reszta w pliku market.json
    #{ "timestamp":"2025-04-09T20:13:52Z", "event":"Market", "MarketID":3710784768, "StationName":"TNB-46F", "StationType":"FleetCarrier", "CarrierDockingAccess":"friends", "StarSystem":"Capricorni Sector NS-U c2-18" }

