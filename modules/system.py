import sys
import sqlite3
import tkinter as tk
from tkinter import ttk
from pathlib import Path
import logging

from tools import ptl

class System_Page:
    def __init__(self, parent):
        #podstawa kazdej klasy
        self.app = parent
        self.db = self.app.db

        self.groups = []
        self.current_group = None 

        self.current_system = None
        self.selected_system = None

    def show(self, parent):
        self.parent = parent
        # frames
        self.frame_group = tk.LabelFrame(self.parent)
        self.frame_group.pack(fill='x')

        
        self.frame_system = tk.LabelFrame(self.parent)
        self.frame_system.pack(fill="both", expand=True)
        frame_system_frame1 = tk.Frame(self.frame_system)
        frame_system_frame1.pack(side='top', fill='x')
        frame_system_frame2 = tk.Frame(self.frame_system)
        frame_system_frame2.pack(side='top', fill='both', expand=True)
        
        # frame group
        self.combobox_groups = ttk.Combobox(self.frame_group)
        self.combobox_groups.config(state='readonly')
        self.combobox_groups.pack(side='left', fill='x', expand=True)
        self.button_group_add = tk.Button(self.frame_group, command=self.window_group_add)
        self.button_group_add.pack(side='left', expand=False)
        self.button_group_edit = tk.Button(self.frame_group, command=self.window_group_edit)
        self.button_group_edit.pack(side='left', expand=False)
        self.button_group_remove = tk.Button(self.frame_group, command=self.window_group_remove)
        self.button_group_remove.pack(side='left', expand=False)

        def Select_Group_Combo(event):
            group_row = self.db.Select('cmdr_groups', 'id, name', f"name = '{self.combobox_groups.get()}' ", True)
            self.current_group = None
            if group_row:
                self.current_group = {"id" : group_row[0], "name" :group_row[1]}
            self.update_widgets()

        self.combobox_groups.bind('<<ComboboxSelected>>', Select_Group_Combo)

        # frame system
        self.label_system_title = tk.Label(frame_system_frame1)
        self.label_system_title.pack(side='left', expand=False)
        self.label_system_current_name = tk.Label(frame_system_frame1, text="-")
        self.label_system_current_name.pack(side='left', expand=True)

        self.button_system_remove = tk.Button(frame_system_frame1, text="Usuń", command=self.window_system_remove)
        self.button_system_remove.pack(side='right', expand=False)
        self.button_system_add = tk.Button(frame_system_frame1, text="Dodaj", command=self.window_system_add)
        self.button_system_add.pack(side='right', expand=False)
        self.button_system_edit = tk.Button(frame_system_frame1, text="Edytuj", command=self.window_system_edit)
        self.button_system_edit.pack(side='right', expand=False)

        self.treeview_systems = ttk.Treeview(frame_system_frame2, columns=('MajorFaction'), selectmode="browse")
        self.treeview_systems.column('#0', minwidth=100, width=50)
        self.treeview_systems.column('MajorFaction', minwidth=100, width=50)
        self.treeview_systems.pack(fill ="both", expand = True)

        def select_system(event):
            selected = self.treeview_systems.focus() 
            self.selected_system = self.treeview_systems.item(selected)['text']
            print("-->>select : " + self.selected_system)
        self.treeview_systems.bind("<<TreeviewSelect>>", select_system)

        self.update_widgets()

    def update_widgets(self):

        self.frame_group.config(text = ptl("Group"))
        self.frame_system.config(text = ptl("Systems"))
        self.label_system_title.config(text= ptl("Current : "))

        self.button_group_add.config(text = ptl("Add"))
        self.button_group_edit.config(text = ptl("Edit"))
        self.button_group_remove.config(text = ptl("Delete"))

        self.button_system_add.config(text = ptl("Add"))
        self.button_system_edit.config(text = ptl("Edit"))
        self.button_system_remove.config(text = ptl("Delete"))

        self.treeview_systems.heading('#0', text= ptl("Name"))
        self.treeview_systems.heading('MajorFaction', text= ptl("Major Faction"))
        
        # frame group
        group_rows = self.db.Select('cmdr_groups', 'id, name', '')
        self.groups = []
        if group_rows :
            self.groups.append(ptl("All"))
            for group_item in group_rows:
                self.groups.append(group_item[1])
        else:
            self.groups.append(ptl("None"))

        self.combobox_groups.config(values=self.groups)
        self.combobox_groups.current(0)   
        if self.current_group != None:
            self.combobox_groups.set(self.current_group['name'])   
        
        
        # frame system
        for i in self.treeview_systems.get_children():
            self.treeview_systems.delete(i)

        if self.current_system:
            self.label_system_current_name.config(text=self.current_system)

        self.system_items = []
        if self.current_group != None:
            system_rows = self.db.Select('cmdr_systems', 'star_system, faction_name', f"group_id = {self.current_group['id']}")
        else:
            system_rows = self.db.Select('cmdr_systems', 'star_system, faction_name', '')
        if system_rows:
            for system_row in system_rows:
                self.system_items.append(self.treeview_systems.insert('', index='end', text=system_row[0], values=(system_row[1],)))    

    def window_group_add(self):
        new_name = tk.StringVar()
        add_wnd = tk.Toplevel(self.parent)

        def system_management_add():
            if new_name.get() == "":
                return            
            self.db.Insert('cmdr_groups','name, permission', f"'{new_name.get()}', '' ")
            add_wnd.destroy()
            add_wnd.update()
            self.app.update_widgets()

        
        add_wnd.title(ptl("Add group"))
        add_wnd.resizable(width=False, height=False)
        add_wnd.minsize(300,100)

        frame = tk.Frame(add_wnd)
        frame.pack(padx=5, fill='both', expand=True)

        system_name_label = tk.Label(frame, text= ptl("Group name"))
        system_name_label.pack(side='top', fill='x', expand=True)
        
        system_name_entry = tk.Entry(frame, textvariable=new_name)
        system_name_entry.pack(side='top', fill='x', expand=True)
        system_name_entry.focus()

        button_add = tk.Button(frame, text= ptl("Add"), command=system_management_add)
        button_add.pack(side='top', fill='x', expand=True)
        button_cancel = tk.Button(frame, text= ptl("Cancel"), command=add_wnd.destroy)
        button_cancel.pack(side='top', fill='x', expand=True)
    
    def window_group_edit(self):
        if self.current_group == None:
            return
        edit_wnd = tk.Toplevel(self.parent)
        edit_name = tk.StringVar()
        system_group_row = self.db.Select('cmdr_groups', 'name', f"id = {self.current_group['id']}", True)
        if system_group_row:
            edit_name.set(system_group_row[0])
        def window_group_save():
            if edit_name.get() == "":
                return            
            self.db.Update('cmdr_groups',f'name = "{edit_name.get()}"', f"id = {self.current_group['id']}")
            edit_wnd.destroy()
            edit_wnd.update()
            self.app.update_widgets()

        edit_wnd.title(ptl("Edit group"))
        edit_wnd.resizable(width=False, height=False)
        edit_wnd.minsize(300,100)

        frame = tk.Frame(edit_wnd)
        frame.pack(padx=5, fill='both', expand=True)
        
        group_name_label = tk.Label(frame, text=ptl("Group name"))
        group_name_label.pack(side='top', fill='x', expand=True)

        group_name_entry = tk.Entry(frame, textvariable=edit_name)
        group_name_entry.pack(side='top', fill='x', expand=True)
        group_name_entry.focus()

        button_add = tk.Button(frame, text= ptl("Save"), command=window_group_save)
        button_add.pack(side='top', fill='x', expand=True)
        button_cancel = tk.Button(frame, text= ptl("Cancel"), command=edit_wnd.destroy)
        button_cancel.pack(side='top', fill='x', expand=True)

    def window_group_remove(self):
        self.db.Delete('cmdr_groups', f"name = '{self.combobox_groups.get()}'")
        self.current_group = None
        self.app.update_widgets()

#systems
    def window_system_add(self):
        new_name = tk.StringVar()
        if self.current_system:
            new_name.set(self.current_system)
        add_wnd = tk.Toplevel(self.parent)
        add_wnd.minsize(300,100)
        
        def system_management_add():
            if new_name.get() == "":
                return
            group_id_row = self.db.Select('cmdr_groups','id', f"name = '{combobox_groups.get()}'",True)
            if group_id_row:
                group_id = group_id_row[0]
            else:
                group_id = 'NULL'
            self.db.Insert('cmdr_systems','star_system, group_id', f"'{new_name.get()}', {group_id}")
            add_wnd.destroy()
            add_wnd.update()
            self.app.update_widgets()

        add_wnd.title(ptl("Add system"))
        add_wnd.resizable(width=False, height=False)
        frame = tk.Frame(add_wnd)
        frame.pack(padx=5, fill='both', expand=True)
        combobox_groups = ttk.Combobox(frame)

        system_name_label = tk.Label(frame, text= ptl("System name"))
        system_name_label.pack(side='top', fill='x', expand=True)
    
        system_name_entry = tk.Entry(frame, textvariable=new_name)
        system_name_entry.pack(side='top', fill='x', expand=True)
        system_name_entry.focus()

        system_group_label = tk.Label(frame, text= ptl("Group"))
        system_group_label.pack(side='top', )

        group_rows = self.db.Select('cmdr_groups', 'id, name', '')
        groups = []
        if group_rows :
            groups.append(ptl("None"))
            for group_item in group_rows:
                groups.append(group_item[1])
        else:
            groups.append(ptl("None"))
        
        combobox_groups.config(state='readonly')
        combobox_groups.pack(side='top', fill='x', expand=True)
        combobox_groups.config(values=groups)
        combobox_groups.current(0)   

        button_add = tk.Button(frame, text= ptl("Add"), command=system_management_add)
        button_add.pack(side='top', fill='x', expand=True)
        button_cancel = tk.Button(frame, text= ptl("Cancel"), command=add_wnd.destroy)
        button_cancel.pack(side='top', fill='x', expand=True)

    def window_system_remove(self):
        remove_wnd = tk.Toplevel(self.parent)

        def system_query_remove_yes():
            self.db.Delete('cmdr_systems', f"UPPER(star_system) = '{self.selected_system.upper()}'")
            self.db.Delete('system_factions', f"UPPER(star_system) = \"{self.selected_system.upper()}\"")  
            remove_wnd.destroy()
            remove_wnd.update()
            self.app.update_widgets()
            
        remove_wnd.title(ptl("Delete system"))
        remove_wnd.minsize(300,100)
        remove_wnd.resizable(width=False, height=False)
        remove_wnd_frame = tk.Frame(remove_wnd)
        remove_wnd_frame.pack(padx=5, fill='both', expand=True)
        label_remove_query = tk.Label(remove_wnd_frame, text= ptl("Are you sure you want to remove the system:"))
        label_remove_query.pack(side='top', fill='x', expand=True)
        label_remove_system_name = tk.Label(remove_wnd_frame, text=f'"{self.selected_system}"')
        label_remove_system_name.pack(side='top', fill='x', expand=True)
        button_remove_yes = tk.Button(remove_wnd_frame, text= ptl("Yes"), command=system_query_remove_yes)
        button_remove_yes.pack(side='top', fill='x', expand=True)
        button_remove_no = tk.Button(remove_wnd_frame, text= ptl("No"), command=remove_wnd.destroy)
        button_remove_no.pack(side='top', fill='x', expand=True)

    def window_system_edit(self):
        if self.selected_system == None:
            return
        system_row = self.db.Select('cmdr_systems', 'star_system, group_id', F"UPPER(star_system) = '{self.selected_system.upper()}'", True)
        system_group_row = self.db.Select('cmdr_groups', 'name, id', F"id = {system_row[1]}", True)
        sys_name = tk.StringVar()
        sys_name.set(system_row[0])
        edit_wnd = tk.Toplevel(self.parent)
        frame = tk.Frame(edit_wnd)
        edit_wnd.minsize(300,100)

        combobox_groups = ttk.Combobox(frame)
        
        def system_management_save():
            if sys_name.get() == "":
                return
            group_id_row = self.db.Select('cmdr_groups','id', f"name = '{combobox_groups.get()}'",True)
            if group_id_row:
                group_id = group_id_row[0]
            else:
                group_id = 'NULL'
            self.db.Update('cmdr_systems', f"star_system = '{sys_name.get()}', group_id = {group_id}", f"UPPER(star_system) = '{self.selected_system.upper()}'")
            edit_wnd.destroy()
            edit_wnd.update()
            self.app.update_widgets()

        edit_wnd.title(ptl("Edit system"))
        edit_wnd.resizable(width=False, height=False)
        frame.pack(padx=5, fill='both', expand=True)
    
        system_name_label = tk.Label(frame, text= ptl("System name"))
        system_name_label.pack(side='top', fill='x', expand=True)
    
        system_name_entry = tk.Entry(frame, textvariable=sys_name)
        system_name_entry.pack(side='top', fill='x', expand=True)
        system_name_entry.focus()

        system_group_label = tk.Label(frame, text= ptl("Group"))
        system_group_label.pack(side='top', )

        group_rows = self.db.Select('cmdr_groups', 'id, name', '')
        groups = []
        if group_rows :
            groups.append(ptl("None"))
            for group_item in group_rows:
                groups.append(group_item[1])
        else:
            groups.append(ptl("None"))
        
        combobox_groups.config(state='readonly')
        combobox_groups.pack(side='top', fill='x', expand=True)
        combobox_groups.config(values=groups)
        combobox_groups.current(0)   
        if system_row[1] != None:
            combobox_groups.set(system_group_row[0])    
        button_add = tk.Button(frame, text= ptl("Save"), command=system_management_save)
        button_add.pack(side='top', fill='x', expand=True)
        button_cancel = tk.Button(frame, text= ptl("Cancel"), command=edit_wnd.destroy)
        button_cancel.pack(side='top', fill='x', expand=True)

    #aktualizacja ze zdarzenia dziennika gry
    def update(self, cmdrname: str, is_beta: bool, system: str, station: str, entry: dict, state: dict):
        self.current_system = system
        self.update_widgets()
