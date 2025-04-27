import sys
import sqlite3
from pathlib import Path
import logging

class BGSMini_DB:
  def __init__(self, plugin_dir):
    self.dbfile_name = 'bgsmini.db'

    self.dbfile_path = Path(plugin_dir) / self.dbfile_name
    createTables = False
    if not self.dbfile_path.exists():
      createTables = True
    self.sqlconn = sqlite3.connect(self.dbfile_path)
    self.sqlcur = self.sqlconn.cursor()

    if createTables == True:
      self.CreateTables()


  def ShowTest(self):
    print(f" !! --> Info TEST <-- !!")

  def Close(self):
    self.sqlconn.close()

  def CreateTables(self):
    try:
      # entry["Factions"]["SquadronFaction"] == True dla TWH
      # system_id = event["SystemAddress"], star_system = event["StarSystem"], faction_name = entry["SystemFaction"]["Name"], faction_state = entry["SystemFaction"]["FactionState"], influence = entry["Factions"]["Influence"]
      self.sqlcur.execute("CREATE TABLE cmdr_systems (system_id INTEGER, group_id INTEGER, star_system TEXT, faction_name TEXT, faction_state TEXT, influence REAL DEFAULT 0, scan_time INTEGER DEFAULT 0)")
      #
      self.sqlcur.execute("CREATE TABLE cmdr_groups (id INTEGER, name TEXT, permission TEXT) PRIMARY KEY(\"id\" AUTOINCREMENT)")
      # system_id = event["SystemAddress"], name = entry["Factions"]["Name"], state = entry["Factions"]["FactionState"], goverment = entry["Factions"]["Government"], happiness_localised = entry["Factions"]["Happiness_Localised"], influence = entry["Factions"]["Influence"]
      self.sqlcur.execute("CREATE TABLE system_factions (system_id INTEGER , name TEXT, state TEXT, goverment TEXT, happiness_localised TEXT, influence REAL DEFAULT 0)")
      # tabela obiektow (marketow)
      self.sqlcur.execute("CREATE TABLE system_objects (system_id INTEGER , stationname TEXT, stationname_localised TEXT, market_id INTEGER DEFAULT 0, progress REAL DEFAULT 0)")
      self.sqlcur.execute("CREATE TABLE object_materials (system_id INTEGER , name TEXT, name_localised TEXT, market_id INTEGER DEFAULT 0, RequiredAmount INTEGER DEFAULT 0, ProvidedAmount INTEGER DEFAULT 0, Payment INTEGER DEFAULT 0)")
      # tabela fleet carrier
      self.sqlcur.execute("CREATE TABLE markets (market_id INTEGER, name TEXT, star_system TEXT, station_type TEXT)")  
      self.sqlcur.execute("CREATE TABLE market_materials (market_id INTEGER, name TEXT, name_localised TEXT, category TEXT, stock INTEGER, BuyPrice INTEGER, SellPrice INTEGER)")
    except sqlite3.OperationalError:
      print(f" !! --> sqlite3.Operational Error when CREATE TABLE")
      #logger.exception('sqlite3.OperationalError when CREATE TABLE entries:')
    return
  
  # SELECT what FROM table where
  def Select(self, table, what, where, one = False):
    if what == '': what = '*' 
    qwhere = ''
    if where != '':
      qwhere = "WHERE " + where    
    try:
      self.sqlcur.execute(f"SELECT {what} FROM {table} {qwhere}")
      print(f" SQL SELECT {what} FROM {table} {qwhere} ")
    except sqlite3.OperationalError:
      print(f" !! --> sqlite3.Operational Error when SELECT {what} FROM {table} {qwhere} ")
    if one == True:
      return self.sqlcur.fetchone()
    else:
      return self.sqlcur.fetchall()
  
  # INSERT INTO table(what) VALUES (values) WHERE (where)
  def Insert(self, table, what, values):  
    try:
      self.sqlcur.execute(f"INSERT INTO {table}({what}) VALUES ({values})")
      self.sqlconn.commit()
      print(f" SQL INSERT INTO {table}({what}) VALUES ({values}) ")
    except sqlite3.OperationalError:
      print(f" !! --> sqlite3.Operational Error when INSERT INTO {table}({what}) VALUES ({values}) ")

  # INSERT INTO table(what) VALUES values WHERE where
  def Update(self, table, values, where):  
    qwhere = ''
    if where != '':
      qwhere = "WHERE " + where    
    try:
      self.sqlcur.execute(f"UPDATE {table} SET {values} {qwhere}")
      self.sqlconn.commit()
      print(f" SQL UPDATE {table} SET {values} {qwhere}:")
    except sqlite3.OperationalError:
      print(f" !! --> sqlite3.Operational Error when UPDATE {table} SET {values} {qwhere}")

  # DELETE FROM table WHERE where
  def Delete(self, table, where) -> bool:  
    qwhere = ''
    if where != '':
      qwhere = "WHERE " + where    
    try:
      self.sqlcur.execute(f"DELETE FROM {table} {qwhere}")
      self.sqlconn.commit()
      print(f" SQL DELETE FROM {table} {qwhere}:")
    except sqlite3.OperationalError:
      print(f" !! --> sqlite3.Operational Error when DELETE FROM {table} {qwhere}")
      return False
    return True

