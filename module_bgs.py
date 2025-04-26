import tkinter as tk
from tkinter import Tk
from tkinter import ttk
import logging
import sys
from pathlib import Path
import datetime
from config import config

from module_db import BGSMini_DB

# C:\Users\kwiec\Saved Games\Frontier Developments\Elite Dangerous

this = sys.modules[__name__]


class BGS_Page:

  def __init__(self, logger, root):
    self.SquadronStartup = ''
    self.logger = logger
    self.plugin_dir = root.plugin_dir
    self.dbfile_name = 'bgsmini.db'
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


#okno do dodawania systemu
  def system_management_window_add(self):
    new_system_name = tk.StringVar()
    def system_management_add():
      if new_system_name.get() == "":
        return
      self.db.Insert('cmdr_systems','star_system, group', f"'{new_system_name.get()}', 0")
      add_wnd.destroy()
      add_wnd.update()
      self.system_management_window_update()
      self.update_widgets()

    add_wnd = tk.Toplevel(self.parent)
    add_wnd.title("Dodaj system")
    add_wnd.geometry("300x150")

    frame = ttk.Frame(add_wnd)
    frame.pack(padx=10, pady=10, fill='x', expand=True)

    system_name_label = tk.Label(frame, text="Nazwa systemu:")
    system_name_label.pack(fill='x', expand=True)
    
    system_name_entry = tk.Entry(frame, textvariable=new_system_name)
    system_name_entry.pack(fill='x', expand=True)
    system_name_entry.focus()

    button_add = tk.Button(frame, text="Dodaj", command=system_management_add, height=20, width= 30)
    button_add.pack(fill='x', expand=True, pady=10)
    button_cancel = tk.Button(frame, text="Anuluj", command=add_wnd.destroy)
    button_cancel.pack(fill='x', expand=True, pady=10)

  def delete_system_from_sql(self, system_name) -> bool:
    row = self.db.Select('cmdr_systems', '', f"star_system = '{system_name}'", True)
    system_id = row[0]
    print(system_id)
    print(system_name)

    if self.db.Delete('system_factions', f"system_id = {system_id}") & self.db.Delete('cmdr_systems', f"system_id = {system_id} AND star_system = '{system_name}'"):
      return True
    else:
      return False
    
#okno do zarzadzania systemami
  def system_management_window_update(self):
      for i in self.system_management_treeview.get_children():
          self.system_management_treeview.delete(i)
      rows = self.db.Select('cmdr_systems', '', '')
      for row in rows:
        self.system_management_treeview.insert('', index = "end", values = (row[1], str(row[4])+'%'))  

  def system_management_window(self):
    
    if self.management_wnd != None:
      if self.management_wnd.winfo_exists() == False:
        self.management_wnd = None
      
    self.management_wnd = tk.Toplevel(self.parent)
    self.management_wnd.title("System manager")
    self.management_wnd.geometry("300x300")
    #close window
    def close_windows():
      self.management_wnd.destroy()
      self.management_wnd.update()
      self.management_wnd = None

    mainframe = tk.Frame(self.management_wnd, background="pink3")
    self.system_management_treeview = ttk.Treeview(mainframe, height= 5,columns=('System_Name', 'Factions_Influence'), show = 'headings', selectmode="browse")
    
    # delete item
    def mainframe_treeview_delete():
      #self.tview_selection = self.treeview.selection()
      selected = self.system_management_treeview.focus() 
      print(self.system_management_treeview.item(selected)['values'][0])
      #usuniecie z bazy
      if self.delete_system_from_sql(self.system_management_treeview.item(selected)['values'][0]) == True :
        # usuniecie z listy
       # self.system_management_treeview.delete(selected)
        self.system_management_window_update()
        self.update_widgets() 

    topframe = tk.Frame(self.management_wnd, height=50, background="green1")
    topframe.pack(fill ="x")
    button_close = tk.Button(topframe, text="Zamknij", command=close_windows)
    button_close.pack(side="right")
    button_add = tk.Button(topframe, text="Dodaj", command=self.system_management_window_add)
    button_add.pack(side="left")
    button_delete = tk.Button(topframe, text="Usuń", command=mainframe_treeview_delete)
    button_delete.pack(side="left")

  
    mainframe.pack(expand = True, fill ="both")
    mainframe_label_frac = tk.Label(mainframe, text="Systemy :", anchor='w')
    mainframe_label_frac.pack()
  
    self.system_management_treeview.pack(expand = True, fill ="both")
    self.system_management_treeview.heading('System_Name', text= 'Nazwa')
    self.system_management_treeview.heading('Factions_Influence', text= 'Wpływy')
    self.system_management_treeview.column('System_Name', minwidth=50, width=150)
    self.system_management_treeview.column('Factions_Influence', minwidth=20, width=20)

    for i in self.system_management_treeview.get_children():
        self.system_management_treeview.delete(i)
    
    rows = self.db.Select('cmdr_systems','', '')
    for row in rows:
      self.system_management_treeview.insert('', index = "end", values = (row[1], str(row[4])+'%'))

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

    def Select_Group_Combo(event):
      group_row = self.db.Select('cmdr_groups', 'id', f"name = '{self.combobox_current_group.get()}' ", True)
      self.current_group = None
      if group_row:
        self.current_group = group_row[0]
      self.update_widgets()

    self.combobox_current_group.bind('<<ComboboxSelected>>', Select_Group_Combo)

    self.button_config = tk.Button(self.topframe, text="Zarzadzaj", command=self.system_management_window)
    self.button_config.pack(side="right")

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
    print(self.treeview.item(selected)['text'])
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
    self.groups = []
    if group_rows :
      for group_item in group_rows:
        self.groups.append(group_item[0])
    else:
      self.groups.append("Wszystkie")

    self.combobox_current_group.config(values=self.groups)

    self.combobox_current_group.current(0)
    if self.current_group != None :
      self.combobox_current_group.current(self.current_group)

  # -- Systemy
    system_rows = self.db.Select('cmdr_systems', '', '')
    for system_row in system_rows:
      self.system_id += 1
      #robimy lokalna zmienna z id systemu, nazwa
      self.systems.append((system_row[0], system_row[1]))
      #sprawdzanie czasu wygasniecia
      dt = datetime.datetime.now()
      seq = int(dt.strftime("%Y%m%d%H%M%S"))
      print(seq)
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
      faction_rows = self.db.Select('system_factions', '', f"system_id = {system_row[0]}")
      for faction_row in faction_rows:
        fact_tag = 'normal'
        if faction_row[1].upper() == system_row[1]:
          if round(faction_row[4],2) > self.high_level :
            fact_tag = 'high'
          elif round(faction_row[4],2) < self.low_level:
            fact_tag = 'low'
          else:
            fact_tag = 'faction'
        self.faction_item.append(self.treeview.insert(self.system_item[self.system_id-1], 'end',  text= faction_row[1], values = (faction_row[2], str(round(faction_row[5], 2))+'%') , tags=fact_tag))
    

#aktualizacja ze zdarzenia dziennika gry
  def update(self, cmdrname: str, is_beta: bool, system: str, station: str, entry: dict, state: dict):
    if entry['event'] == 'FSDJump':
      self.db.Delete('system_factions', f"system_id = {entry['SystemAddress']}")  
      #dodaje nowe wpisy  
      if 'Factions' in entry:
        for faction in entry['Factions']:
          #aktualizacja danych 
          dt = datetime.datetime.now()
          seq = int(dt.strftime("%Y%m%d%H%M%S"))
          if 'SquadronFaction' in faction:
            if faction["SquadronFaction"] :
              self.db.Update('cmdr_systems', f"system_id = {entry['SystemAddress']}, faction_name = \"{faction['Name']}\", faction_state = \"{faction['FactionState']}\", influence = {faction['Influence'] * 100}, scan_time = {seq+240000}", f" star_system = \"{entry['StarSystem']}\"")
          self.db.Insert('system_factions', 'system_id, name, state, goverment, happiness_localised, influence', f"{entry['SystemAddress']}, \"{faction['Name']}\", \"{faction['FactionState']}\", \"{faction['Government']}\", \"{faction['Happiness_Localised']}\", {faction['Influence'] * 100}")
      self.update_widgets()    
    
