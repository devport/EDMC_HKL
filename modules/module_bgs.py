import tkinter as tk
from tkinter import Tk
from tkinter import ttk
import logging
import sys
from pathlib import Path
import datetime
from config import config

from modules.module_db import BGSMini_DB

this = sys.modules[__name__]


class BGS_Page:

  def __init__(self, logger, root):
    self.SquadronStartup = ''
    self.logger = logger
    self.plugin_dir = root.plugin_dir
    self.tview_selection = 0
    self.management_wnd = None
    self.systems = []
    self.high_level = 60
    self.low_level = 40
    self.config = root.config
    self.db = BGSMini_DB(root.plugin_dir)
    self.root = root
    self.groups = []
    self.current_group = None
    


    #  self.dbfile_sqlc.execute('CREATE TABLE cmdr_systems (id INTEGER PRIMARY KEY , name TEXT, state TEXT, influence REAL DEFAULT 0, scan_time INTEGER DEFAULT 0)')
    #  self.dbfile_sqlc.execute('CREATE TABLE system_factions (id INTEGER PRIMARY KEY , name TEXT, system_id INTEGER DEFAULT 0, state TEXT, influence REAL DEFAULT 0)')


#glowna ramka modulu (glowna zakladka)
  def show(self, parent):
    self.parent = parent
   
    #top
    self.topframe = tk.Frame(self.parent, height=20)
    self.topframe.pack(fill='x')

    self.label_group = tk.Label(self.topframe, text="Grupa : ")
    self.label_group.pack(side="left", expand=False)
    
    self.combobox_current_group = ttk.Combobox(self.topframe)
    self.combobox_current_group.pack(side="left", fill="x", expand=True)
    self.combobox_current_group.config(state='readonly')

    def Select_Group_Combo(event):
      group_row = self.db.Select('cmdr_groups', 'id, name', f"name = '{self.combobox_current_group.get()}' ", True)
      self.current_group = None
      if group_row:
        self.current_group = {"id" : group_row[0], "name" :group_row[1]}
      self.update_widgets()

    self.combobox_current_group.bind('<<ComboboxSelected>>', Select_Group_Combo)

    #main
    self.mainframe = tk.Frame(self.parent)
    self.mainframe.pack(padx=10, expand = True, fill ="both")
    self.label_system = tk.Label(self.mainframe, text="Systemy :", anchor='w')
    self.label_system.pack()

    self.treeview = ttk.Treeview(self.mainframe,columns=('Factions_State', 'Factions_Influence'), show = 'tree', selectmode="browse")
    self.treeview.pack(side="bottom", expand = True, fill ="both")
    self.treeview.heading('#0', text= 'Nazwa')
    self.treeview.heading('Factions_State', text= 'Stan')
    self.treeview.heading('Factions_Influence', text= 'Wpływy')
    self.treeview.column('#0', minwidth=50, width=150)
    self.treeview.column('Factions_State', minwidth=20, width=20)
    self.treeview.column('Factions_Influence', minwidth=20, width=20)
    self.treeview.tag_configure('normal', background='white')
    self.treeview.tag_configure('faction', background='palegreen')
    self.treeview.tag_configure('high', background='pink')
    self.treeview.tag_configure('low', background='coral')
    self.treeview.bind("<Double-1>", self.treeview_OnDoubleClick)
    self.update_widgets() 

#reakcja na podwojne klikniecie w liste systemow
  def treeview_OnDoubleClick(self, event):
    #self.tview_selection = self.treeview.selection()
    selected = self.treeview.focus() 
    copiedText = (self.treeview.item(selected)['text'])
    r = Tk()
    r.withdraw()
    r.clipboard_clear()
    r.clipboard_append(copiedText)
    r.destroy()

#aktualizacja zawartosci widgetow
  def update_widgets(self):
    if config.get_str("BGSMini_tag_fact_color") != "None" :
      self.treeview.tag_configure('faction', background=config.get_str("BGSMini_tag_fact_color"))
    if config.get_str("BGSMini_tag_high_color") != "None" :
      self.treeview.tag_configure('high', background=config.get_str("BGSMini_tag_high_color"))
    if config.get_str("BGSMini_tag_low_color") != "None" :
      self.treeview.tag_configure('low', background=config.get_str("BGSMini_tag_low_color"))
    #main widgets
    for i in self.treeview.get_children():
      self.treeview.delete(i)

    self.systems.clear()
    self.system_id = 0
    self.system_item = []
    self.system_item.clear()
    self.faction_item = []
    self.faction_item.clear()
    self.check_img = []
    self.check_img.clear()

  # -- Grupy
    group_rows = self.db.Select('cmdr_groups', 'id, name', '')
    groups = []
    if group_rows :
      groups.append("Wszystkie")
      for group_item in group_rows:
         groups.append(group_item[1])
    else:
       groups.append("Wszystkie")
    
    self.combobox_current_group.config(values=groups)
    self.combobox_current_group.current(0)
    if self.current_group != None :
      self.combobox_current_group.set(self.current_group['name'])

  # -- Systemy
    if self.current_group != None :
      system_rows = self.db.Select('cmdr_systems', 'system_id, star_system, faction_name, faction_state, influence, scan_time', F"group_id = {self.current_group['id']}")
    else:
      system_rows = self.db.Select('cmdr_systems', 'system_id, star_system, faction_name, faction_state, influence, scan_time', '')
    if system_rows == None:
      return
    for system_row in system_rows:
      self.system_id += 1
      #robimy lokalna zmienna z id systemu, nazwa
      self.systems.append((system_row[0], system_row[1]))
      #sprawdzanie czasu wygasniecia
      dt = datetime.datetime.now()
      seq = int(dt.strftime("%Y%m%d%H%M%S"))

      if system_row[5] > seq :
        self.check_img.append(tk.PhotoImage(file=f"{Path(self.plugin_dir)}/img/check_ok16.png"))
      elif system_row[5] == 0:
        self.check_img.append(tk.PhotoImage(file=f"{Path(self.plugin_dir)}/img/info16.png"))
      else:
        self.check_img.append(tk.PhotoImage(file=f"{Path(self.plugin_dir)}/img/check_no16.png"))
      #sprawdzanie poziomow influence  
      if round(system_row[4],2) > self.high_level:
        sys_tag = 'high'
      elif round(system_row[4],2) < self.low_level:
        sys_tag = 'low'
      else:
        sys_tag = 'normal'

      self.system_item.append(self.treeview.insert('', index='end', text=system_row[1], values = (str(system_row[3]), str(round(system_row[4],2))+'%'), image=self.check_img[self.system_id-1], tags=sys_tag))
      #ladowanie frakcji
      faction_rows = self.db.Select('system_factions', '', f"star_system = \"{system_row[1]}\"")
      if faction_rows:
        for faction_row in faction_rows:
          fact_tag = 'normal'
          #print(faction_row[1].upper() + " == " + system_row[2].upper())
          if faction_row[1].upper() == system_row[2].upper():
            if round(faction_row[5],2) > self.high_level :
              fact_tag = 'high'
            elif round(faction_row[5],2) < self.low_level:
              fact_tag = 'low'
            else:
              fact_tag = 'faction'
          self.faction_item.append(self.treeview.insert(self.system_item[self.system_id-1], 'end',  text= faction_row[1], values = (faction_row[2], str(round(faction_row[5], 2))+'%') , tags=fact_tag))
      

#aktualizacja ze zdarzenia dziennika gry
  def update(self, cmdrname: str, is_beta: bool, system: str, station: str, entry: dict, state: dict):
    if entry['event'] == 'FSDJump':

      check_system_row = self.db.Select('cmdr_systems', 'system_id', f'star_system = "{system}"', True)
      if check_system_row:
        #self.db.Update('cmdr_systems', f"faction_name = \"{faction['Name']}\", faction_state = \"{faction['FactionState']}\", influence = {faction['Influence'] * 100}, scan_time = {seq+240000}", f"star_system = \"{system}\"")

        self.db.Delete('system_factions', f"star_system = \"{system}\"")  
        #dodaje nowe wpisy  

        #if 'SystemFaction' in entry:
        #  self.db.Update('cmdr_systems', f"star_system = \"{system}\", faction_name = \"{entry['SystemFaction']['Name']}\", faction_state = \"{entry['SystemFaction']['FactionState']}\", scan_time = {seq+240000}", f" star_system = \"{entry['StarSystem']}\"")

        if 'Factions' in entry:
          for faction in entry['Factions']:
            #aktualizacja danych 
            dt = datetime.datetime.now()
            seq = int(dt.strftime("%Y%m%d%H%M%S"))
            if 'SquadronFaction' in faction:
              if faction["SquadronFaction"] :
                self.db.Update('cmdr_systems', f"star_system = \"{system}\", faction_name = \"{faction['Name']}\", faction_state = \"{faction['FactionState']}\", influence = {faction['Influence'] * 100}, scan_time = {seq+240000}", f" star_system = \"{entry['StarSystem']}\"")
            Happiness_Localised = ''
            if 'Happiness_Localised' in faction:
              Happiness_Localised = faction['Happiness_Localised']
            
            self.db.Insert('system_factions', 'star_system, name, state, goverment, happiness_localised, influence', f"\"{system}\", \"{faction['Name']}\", \"{faction['FactionState']}\", \"{faction['Government']}\", \"{Happiness_Localised}\", {faction['Influence'] * 100}")
      self.update_widgets()    
    
