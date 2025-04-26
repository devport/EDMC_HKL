
from config import config
import tkinter as tk
import sys
from tkinter import ttk
from pathlib import Path
from module_db import BGSMini_DB


# C:\Users\kwiec\Saved Games\Frontier Developments\Elite Dangerous

this = sys.modules[__name__]
class Depot_Page:
  def __init__(self, logger, root):
    self.plugin_dir = root.plugin_dir
    self.logger = logger
    self.root = root
    self.config = root.config
    self.check_completed = tk.IntVar()
    self.db = BGSMini_DB(root.plugin_dir)
    self.current_system = None
    self.current_market = {
      "name" : None,
      "id" : None,
      "stationtype" : None,
      "materials" : None
    }

    self.market_info = {
      "name" :  None,
      "id" : None,
      "stationtype" : None,
      "materials" : None
    }

    self.current_object = {
      "StarSystem" : None,
      "SystemAddress" : None,
      "StationName" : None,
      "StationName_Localised" : None,
      "MarketId" : None,
      "ConstructionProgress" : None,
      "Materials" : None
    }

    self.object_info = {
      "StarSystem" : None,
      "SystemAddress" : None,
      "StationName" : None,
      "StationName_Localised" : None,
      "MarketId" : None,
      "ConstructionProgress" : None,
      "Materials" : None
    }


  #zwraca liste nazw systemow 
  def load_systems(self):
    rows = self.db.Select('cmdr_systems','star_system','')  
    result = []   
    for row in rows:
      result.append(str(row[0]))
    return result

  def load_object_materials(self, marketid, systemid):
    meterial_rows = self.db.Select('object_materials', "name, name_localised, RequiredAmount, ProvidedAmount, Payment", f"system_id = {systemid} AND market_id = {marketid} ")
    if meterial_rows:
      materials = []
      for material_row in meterial_rows:
        material = {
            "SystemId"        : int,
            "Name"            : str,
            "NameLocalised"   : str,
            "MarketId"        : int,
            "RequiredAmount"  : int, 
            "ProvidedAmount"  : int, 
            "Payment"         : int
        }
        material["Name"] = material_row[0] # Remove leading "$" and trailing "_name;"
        material["SystemId"] = systemid
        material["NameLocalised"] = material_row[1]
        material["MarketId"] = marketid
        material["RequiredAmount"] = material_row[2]
        material["ProvidedAmount"] = material_row[3]
        material["Payment"] = material_row[4]
        materials.append(material)
        self.object_info["Materials"] = materials
      print("Pobrano materiały dla System ID: "+ str(systemid) +" i Market ID: "+str(marketid))
    else:
      self.object_info["Materials"] = None
      emptyvalue = ['']
      self.combobox_objects.config(values=emptyvalue)
      self.combobox_objects.config(state='disabled')
      print("Brak materiałów dla System ID: "+ str(systemid) +" i Market ID: "+str(marketid))


#aktualizacja zawartosci widgetow
  def update_widgets(self):
    print("current_obj -> MarketId : " +str(self.current_object['MarketId']))
    print("current_obj -> SystemAddress : " + str(self.current_object['SystemAddress']))

    rows = self.db.Select('cmdr_systems','star_system','')
    systems = []
    for row in rows:
      systems.append(row[0])
    self.combobox_systems['values'] = systems
    if len(systems) > 0 :
      if self.current_system != None :
        self.combobox_systems.set(self.current_system)
      else:
        self.combobox_systems.set(systems[0])


    self.label_current_object.config(text="Aktualny obiekt :" + str(self.current_object['StationName_Localised']))

    #---wczytanie listy rynkow -----------------------------------------------------------------------------
    # to do przeglądu i poprawki 
    market_rows = self.db.Select('markets', 'market_id, name, station_type', '')
    new_objects = []
    new_object_names = []
    for market_row in market_rows:
      new_objects.append(market_row)
      new_object_names.append(market_row[1])
    
        # !- > moze zamiast brac z combobox'a po nazwie nalezy pobrac po index'ie

    print("combobox current: " + str(self.combobox_markets.current()))
    print('market_info_name: '+str(self.market_info['name']))
    print('market_info_id: '+str(self.market_info['id'])) 
    print('current_market_name: '+str(self.current_market['name']))
    print('current_market_id: '+str(self.current_market['id'])) 
    self.combobox_markets['values'] = new_object_names

    if new_objects:
      if self.market_info['name'] != None:
        self.combobox_markets.set(self.market_info['name'])
      else:
        self.market_info['name'] = new_objects[0][1]
        self.market_info['id'] = new_objects[0][0]
        self.market_info['stationtype'] = new_objects[0][2]
      
    #aktualny rynek
    self.label_current_market.config(text="Aktualny rynek :"+str(self.current_market['name']))
    #kasowanie listy materialow
    for i in self.treeview_material_list.get_children():
      self.treeview_material_list.delete(i)

    # wczytanie materialow 

    #get_market_row = self.db.Select('markets', 'name, market_id', f"name = \"{self.combobox_markets.get()}\"", True)
    #self.current_market['name'] = get_market_row[0]
    #self.current_market['id'] = get_market_row[1]
    
    self.market_info['materials'] = None
    if self.market_info['id'] != None: 
      self.market_info['materials']  = self.db.Select('market_materials', 'name, name_localised, stock', f"market_id = {self.market_info['id']}")
    
    # jezeli jest aktualny obiekt to wlacz przyciski
    if self.current_market['name'] == None:
      self.button_current_market_add.config(state='disabled')
      self.button_current_market_show.config(state='disabled')
    else:
      self.button_current_market_add.config(state='normal')
      self.button_current_market_show.config(state='normal')

    #---koniec informacji o obiektach -----------------------------------------------------------------------------
    # jezeli jest aktualny obiekt to wlacz przyciski
    if self.current_object['SystemAddress'] == None:
      self.button_current_object_add.config(state='disabled')
      self.button_current_object_show.config(state='disabled')
    else:
      self.button_current_object_add.config(state='normal')
      self.button_current_object_show.config(state='normal')

    # jezeli obecny system istnieje 
    print("object_info_sysAddress: " + str(self.object_info['SystemAddress']))
    print("object_info_marketId: " + str(self.object_info['MarketId']))

    if self.object_info['SystemAddress'] == None or self.object_info['MarketId'] == None:
      return

    # self.combobox_objects
    self.label_progress.config(text="Procent ukończenia : " + str(round(self.object_info['ConstructionProgress']*100,2) ) + " %")

    if self.object_info['Materials'] == None:
      return
    #wyswietlanie listy z object_info
    for material_row in self.object_info['Materials']:
      m_stock = 0
      for market_material in self.market_info['materials']:
        #print[material_row]
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

    frame_system = tk.Frame(self.parent, width=400, height=50)
    frame_system.pack(side='top', fill='x', expand=True)
    frame_current_object = tk.Frame(self.parent, height=50)
    frame_current_object.pack(side='top', fill='x', expand=True)
    frame_object = tk.Frame(self.parent, height=50)
    frame_object.pack(side='top', fill='x', expand=True)
    frame_object_info = tk.Frame(self.parent, height=50)
    frame_object_info.pack(side='top', fill='x', expand=True)
    frame_current_market = tk.Frame(self.parent, height=50)
    frame_current_market.pack(side='top', fill='x', expand=True)
    frame_market = tk.Frame(self.parent, height=50)
    frame_market.pack(side='top', fill='x', expand=True)
    frame_show_option = tk.Frame(self.parent, height=50)
    frame_show_option.pack(side='top', fill='x', expand=True)
  

    self.combobox_systems = ttk.Combobox(frame_system)
    self.combobox_systems.config(state='readonly')
    self.combobox_systems.pack(side='left', fill='x', expand=True)

#frame_current_object
    self.label_current_object  = tk.Label(frame_current_object, text="Aktualny obiekt :", anchor='w')
    self.label_current_object.pack(side='left', fill='x', expand=True)

    def current_object_add():
      if self.current_object['SystemAddress'] != None and self.current_object['MarketId'] != None:
        self.object_info = self.current_object
        row = self.db.Select('system_objects', 'system_id, market_id', f"system_id = {self.current_object['SystemAddress']} AND market_id = {self.current_object['MarketId']}", True)
        if not row:
          self.db.Insert('system_objects', 'system_id, stationname, stationname_localised, market_id, progress', f"{self.current_object['SystemAddress']}, \"{self.current_object['StationName']}\", \"{self.current_object['StationName_Localised']}\", {self.current_object['MarketId']}, {self.current_object['ConstructionProgress']}")
        self.update_widgets()

    self.button_current_object_add = tk.Button(frame_current_object, text="Dodaj", command=current_object_add)
    self.button_current_object_add.pack(side='left', expand=False)

    def current_object_show():
      if self.current_object['SystemAddress'] != None and self.current_object['MarketId'] != None:
        self.object_info = self.current_object
      self.update_widgets()

    self.button_current_object_show = tk.Button(frame_current_object, text="Pokaż", command=current_object_show)
    self.button_current_object_show.pack(side='left', expand=False)

#----------------
    label_object = tk.Label(frame_object, text="Obiekt :", anchor='w')
    label_object.pack(side='left', expand=False)

    self.combobox_objects = ttk.Combobox(frame_object, values = [])
    self.combobox_objects.config(state='disabled')
    self.combobox_objects.pack(side='left', fill='x', expand=True)

    button_object_del = tk.Button(frame_object, text="Usuń")
    button_object_del.pack(side='left', expand=False)
    
    self.label_progress = tk.Label(frame_object_info, text="Procent ukończenia :", anchor='w')
    self.label_progress.pack(side='left', anchor='w')


#----------------
    self.label_current_market  = tk.Label(frame_current_market, text="Aktualny rynek :", anchor='w')
    self.label_current_market.pack(side='left', fill='x', expand=True)

    def current_market_add():
      if self.current_market['name'] != None and self.current_market['id'] != None :
        self.root.market.load_journal()
        self.current_market['materials'] = self.root.market.get_commodity_names() 
        self.market_info = self.current_market
        self.root.market.save()
        self.update_widgets()

    self.button_current_market_add = tk.Button(frame_current_market, text="Dodaj", command=current_market_add)
    self.button_current_market_add.pack(side='left', expand=False)

    def current_market_show():
      if self.current_market['name'] != None and self.current_market['id'] != None :
        self.root.market.load_journal()
        self.current_market['materials'] = self.root.market.get_commodity_names() 
        self.market_info = self.current_market
        self.update_widgets()

    self.button_current_market_show = tk.Button(frame_current_market, text="Pokaż", command=current_market_show)
    self.button_current_market_show.pack(side='left', expand=False)

    label_market = tk.Label(frame_market, text="Rynek :", anchor='w')
    label_market.pack(side='left', expand=False)

    self.combobox_markets = ttk.Combobox(frame_market, values = [])
    self.combobox_markets.config(state='readonly')
    self.combobox_markets.pack(side='left', fill='x', expand=True)

    def market_delete():
      if str(self.market_info['name']) == self.combobox_markets.get():
        self.root.market.delete(self.market_info['id'])
        self.update_widgets()

    button_market_del = tk.Button(frame_market, text="Usuń", command=market_delete)
    button_market_del.pack(side='left', expand=False)

    def update_check_completed():
      self.update_widgets()
    self.checkbutton_completed = tk.Checkbutton(frame_show_option, text='Ukrywaj zasypane materiały', variable=self.check_completed, onvalue=1, offvalue=0, command=update_check_completed)
    self.checkbutton_completed.pack(side='top', anchor='w')

    #----------------------------------------------------------------------
    def Select_Sys_Combo(event):
      #update data from sql
      system_id = self.db.Select('cmdr_systems', 'system_id', f'star_system = "{self.combobox_systems.get()}"', True)
      object_rows = self.db.Select('system_objects', 'progress, stationname, stationname_localised, market_id', f"system_id = {system_id[0]}")
      #ustaw aktywny system do wyswietlania
      self.object_info['SystemAddress'] = system_id[0]
      if object_rows:
        new_objs = []
        for object in object_rows:
          new_objs.append(object[2])
        
        self.combobox_objects['values'] = new_objs
        if new_objs:
          #defaultowy obiekt
          self.combobox_objects.set(new_objs[0])
        else:
          self.combobox_objects.set('')
        if object_rows[0][2] != None :
          self.object_info['ConstructionProgress'] = object_rows[0][0]
          self.object_info['StationName'] = object_rows[0][1]
          self.object_info['StationName_Localised'] =  object_rows[0][2]
          self.object_info['MarketId'] = object_rows[0][3]  #pierwszy aktywny system
          self.object_info['StarSystem'] = self.combobox_systems.get()
          print(self.object_info)
          self.current_system = self.combobox_systems.get()
          self.combobox_objects.config(state='readonly')
      else:
        print('disabled')
        self.object_info['MarketId'] = None
        self.combobox_objects.config(state='disabled')
      
      self.load_object_materials(self.object_info['MarketId'], self.object_info['SystemAddress'])
      self.update_widgets()

    # jeżeli wykryje zmianę
    self.combobox_systems.bind('<<ComboboxSelected>>', Select_Sys_Combo)
    
    
    #----------------------------------------------------------------------
    def Select_Obj_Combo(event):
      #update data from sql
      if self.object_info['SystemAddress'] == None:
        return
      self.load_object_materials(self.object_info['MarketId'], self.object_info['SystemAddress'])
      self.update_widgets()

    self.combobox_objects.bind('<<ComboboxSelected>>', Select_Obj_Combo)


    def Select_Market_Combo(event):
      print('select market: '+self.combobox_markets.get())
      market_row = self.db.Select('markets', 'name, market_id', f"name = \"{self.combobox_markets.get()}\"", True)
      self.market_info['name'] = market_row[0]
      self.market_info['id'] = market_row[1]
      print('select -> ' + self.market_info['name'] + ' >> ' +str(self.market_info['id']))
      self.update_widgets()
    
    self.combobox_markets.bind('<<ComboboxSelected>>', Select_Market_Combo)

    #current markets

    

    #main
    self.mainframe = tk.Frame(self.parent)
    self.mainframe.pack(padx=10, expand = True, fill ="both")


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
    #sprawdzam aktualny rynek
     #"event":"Market", "MarketID":3710784768, "StationName":"TNB-46F", "StationType":"FleetCarrier"
    if entry['event'] == 'Market':
      self.current_market['name'] = entry['StationName']
      self.current_market['id'] = entry['MarketID']
      self.current_market['stationtype'] = entry['StationType']

    # sprawdzam czy zadokowano
    if entry['event'] == "Docked":
      if 'StationName' in entry:
        if entry["StationName"][11:-10] == "ColonisationShip":
          self.current_object['StarSystem'] = entry["StarSystem"]
          self.current_object['SystemAddress'] = entry["SystemAddress"]
          self.current_object['StationName'] = entry["StationName"]
          self.current_object['StationName_Localised'] = entry["StationName_Localised"]
          self.current_object['MarketId'] = entry["MarketID"]
          self.current_object['Materials']= None

    if entry['event'] == 'Undocked':
      if 'StationName' in entry:
        if entry["StationName"][11:-10] == "ColonisationShip":
          self.current_object['StarSystem'] = None
          self.current_object['SystemAddress'] = None
          self.current_object['StationName'] = None
          self.current_object['StationName_Localised'] = None
          self.current_object['MarketId'] = None
          self.current_object['Materials']= None

    # sprawdzam czy jestem na obiekcie kolonizacyjnym
    if entry['event'] == 'ColonisationConstructionDepot' :
      if entry['MarketID'] == self.current_object['MarketId'] :
        self.current_object['ConstructionProgress'] = entry["ConstructionProgress"]
        print("ConstructionProgress: " +str(self.current_object['ConstructionProgress']))

        objInDb = self.db.Select('system_objects', '*', f"market_id = {self.current_object['MarketId']}", True)
        if objInDb:
          self.db.Delete('object_materials', f"system_id = {self.current_object['SystemAddress']} AND market_id = {self.current_object['MarketId']}")
          self.db.Update('system_objects', f"progress = {self.current_object['ConstructionProgress']}", f"system_id = {self.current_object['SystemAddress']} AND market_id ={self.current_object['MarketId']}")

        materials = []
        for material_row in entry['ResourcesRequired'] :
          material = {
            "SystemId"        : int,
            "Name"            : str,
            "NameLocalised"   : str,
            "MarketId"        : int,
            "RequiredAmount"  : int, 
            "ProvidedAmount"  : int, 
            "Payment"         : int
          }
          material["Name"] = material_row['Name'][1:-6] # Remove leading "$" and trailing "_name;"
          material["SystemId"] = self.current_object['SystemAddress']
          material["NameLocalised"] = material_row['Name_Localised']
          material["MarketId"] = entry['MarketID']
          material["RequiredAmount"] = material_row['RequiredAmount']
          material["ProvidedAmount"] = material_row['ProvidedAmount']
          material["Payment"] = material_row['Payment']
          materials.append(material)
          self.current_object["Materials"] = materials       
       
          if objInDb:
            self.db.Insert('object_materials', 'system_id, name, name_localised, market_id, RequiredAmount, ProvidedAmount, Payment', f"{self.current_object['SystemAddress']}, \"{material['Name']}\", \"{material_row['Name_Localised']}\", {self.current_object['MarketId']}, {material_row['RequiredAmount']}, {material_row['ProvidedAmount']}, {material_row['Payment']}")

      else:  print('Markety sie nie zgadzaja : '+str(entry['MarketID'] ) + " i " +str( self.current_object['MarketId'] ))
        
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

