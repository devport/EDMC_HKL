import sys
import sqlite3
from pathlib import Path
import logging

class BGSMini_DB:
  def __init__(self, plugin_dir):
    self.dbfile_name = 'local.db'
    self.dbg_mode = True


    self.dbfile_path = Path(plugin_dir) / self.dbfile_name
    create_table = False
    if not Path.exists(self.dbfile_path):
      create_table = True
    self.sqlconn = sqlite3.connect(self.dbfile_path)
    self.sqlcur = self.sqlconn.cursor()
    #
    self.CreateTables()

  def Close(self):
    self.sqlconn.close()

  def CreateTables(self):
    tables = []
    tables.append("CREATE TABLE cmdr_systems (system_id INTEGER, group_id INTEGER, star_system TEXT, faction_name TEXT, faction_state TEXT, influence REAL DEFAULT 0, scan_time INTEGER DEFAULT 0)")  
    tables.append("CREATE TABLE cmdr_groups (id INTEGER, name TEXT, permission TEXT, PRIMARY KEY(\"id\" AUTOINCREMENT))")  
    tables.append("CREATE TABLE system_factions (star_system TEXT , name TEXT, state TEXT, goverment TEXT, happiness_localised TEXT, influence REAL DEFAULT 0)")  
    tables.append("CREATE TABLE system_objects (star_system TEXT, stationname TEXT, stationname_localised TEXT, market_id INTEGER DEFAULT 0, progress REAL DEFAULT 0)")  
    tables.append("CREATE TABLE object_materials (star_system TEXT, name TEXT, name_localised TEXT, market_id INTEGER DEFAULT 0, RequiredAmount INTEGER DEFAULT 0, ProvidedAmount INTEGER DEFAULT 0, Payment INTEGER DEFAULT 0)")  
    
    tables.append("CREATE TABLE markets (market_id INTEGER, name TEXT, star_system TEXT, station_type TEXT)")  
    tables.append("CREATE TABLE market_materials (market_id INTEGER, name TEXT, name_localised TEXT, category TEXT, stock INTEGER, Demand INTEGER, BuyPrice INTEGER, SellPrice INTEGER)")  
    tables.append("CREATE TABLE stations (StarSystem TEXT, SystemAddress INT, StationName TEXT, StationType TEXT, MarketID INT, DistFromStarLS INT, StationFaction TEXT, StationGovernment TEXT, StationGovernment_Localised TEXT, StationEconomy TEXT, StationEconomy_Localised TEXT, StationEconomies TEXT, LandingPads TEXT)")  
    
    for table in tables:
      try:
        self.sqlcur.execute(table)
      except sqlite3.OperationalError:
        if self.dbg_mode : print(f" !! --> sqlite3.Operational Error when ", table)
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
      if self.dbg_mode : print(f" SQL SELECT {what} FROM {table} {qwhere} ")
    except sqlite3.OperationalError:
      if self.dbg_mode : print(f" !! --> sqlite3.Operational Error when SELECT {what} FROM {table} {qwhere} ")
    if one == True:
      return self.sqlcur.fetchone()
    else:
      return self.sqlcur.fetchall()
  
  # INSERT INTO table(what) VALUES (values) WHERE (where)
  def Insert(self, table, what, values):  
    try:
      self.sqlcur.execute(f"INSERT INTO {table}({what}) VALUES ({values})")
      self.sqlconn.commit()
      if self.dbg_mode : print(f" SQL INSERT INTO {table}({what}) VALUES ({values}) ")
    except sqlite3.OperationalError:
      if self.dbg_mode : print(f" !! --> sqlite3.Operational Error when INSERT INTO {table}({what}) VALUES ({values}) ")

  # INSERT INTO table(what) VALUES values WHERE where
  def Update(self, table, values, where):  
    qwhere = ''
    if where != '':
      qwhere = "WHERE " + where    
    try:
      self.sqlcur.execute(f"UPDATE {table} SET {values} {qwhere}")
      self.sqlconn.commit()
      if self.dbg_mode : print(f" SQL UPDATE {table} SET {values} {qwhere} ")
    except sqlite3.OperationalError:
      if self.dbg_mode : print(f" !! --> sqlite3.Operational Error when UPDATE {table} SET {values} {qwhere}")

  # DELETE FROM table WHERE where
  def Delete(self, table, where) -> bool:  
    qwhere = ''
    if where != '':
      qwhere = "WHERE " + where    
    try:
      self.sqlcur.execute(f"DELETE FROM {table} {qwhere}")
      self.sqlconn.commit()
      if self.dbg_mode : print(f" SQL DELETE FROM {table} {qwhere} ")
    except sqlite3.OperationalError:
      if self.dbg_mode : print(f" !! --> sqlite3.Operational Error when DELETE FROM {table} {qwhere}")
      return False
    return True

