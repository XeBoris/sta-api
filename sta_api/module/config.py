import configparser



class HandleConfiguration():
    def __init__(self):
        self.config_path = None
        self.config_parser = configparser.ConfigParser()

    def set_path(self, path):
        self.config_path = path
        self.config_parser.read(self.config_path)

    def get_port(self):
        if 'SERVER CONFIGURATION' in self.config_parser:
            return self.config_parser["SERVER CONFIGURATION"].get("port", 5000)

    def flask_debug(self):
        if 'SERVER CONFIGURATION' in self.config_parser:
            deb = self.config_parser["SERVER CONFIGURATION"].get("debug", "on")
            if deb == "on":
                return True
            else:
                return False

    def get_sta_db_name(self):
        if 'STA CORE CONFIGURATION' in self.config_parser:
            deb = self.config_parser['STA CORE CONFIGURATION'].get("db-name")
            return deb

    def get_sta_db_type(self):
        if 'STA CORE CONFIGURATION' in self.config_parser:
            deb = self.config_parser['STA CORE CONFIGURATION'].get("db-type")
            return deb

    def get_sta_db_path(self):
        if 'STA CORE CONFIGURATION' in self.config_parser:
            deb = self.config_parser['STA CORE CONFIGURATION'].get("db-path")
            return deb
