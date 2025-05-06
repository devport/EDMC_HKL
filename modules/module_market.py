import json
from os.path import join
from typing import Dict, List

from config import config
from modules.module_db import BGSMini_DB

FILENAME_MARKET = "Market.json"

class Market:
    def __init__(self, root):
        self.root = root
        self.db = BGSMini_DB(root.plugin_dir)
        self.name:str = None
        self.id:int = None
        self.new_market = True
        self.station_type:str = None
        self.star_system:str = None
        self.commodities:Dict = {}
        self.commodity_names = [] 

    def create_table(self):
        self.db.CreateTables()

    def _clear_data(self):
        self.name = None
        self.id = None
        self.station_type:str = None
        self.star_system:str = None
        self.commodities = {}
        self.commodity_names.clear()
        
    # pobieranie z pliku Market.json
    def load_journal(self):
        self._clear_data()
        self._parse()

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
            material['Demand'] = material_row[3]
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

    def update(self, cmdrname: str, is_beta: bool, system: str, station: str, entry: dict, state: dict):
        #"event":"Market", "MarketID":3710784768, "StationName":"TNB-46F", "StationType":"FleetCarrier"
        if entry['event'] == 'Market':      
            market_row = self.db.Select('markets', 'name, star_system, station_type', f"market_id = {entry['MarketID']} ", True)    
            if market_row:
                self.load_journal()
                self.save()
        return