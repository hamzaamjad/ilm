class ini():

    def __init__(self, file_path = None, file_name = 'ilm.ini'):
        import os
        import os.path
        import configparser

        if file_path is None:
            self.file_path = os.path.join(os.getcwd(), file_name)
        else:
            self.file_path = os.path.join(file_path, file_name)
        
        self.config = configparser.ConfigParser()
        if os.path.isfile(self.file_path):
            print("Existing INI file found. Loading credentials...")
            self.config.read(self.file_path)
        else:
            print("Creating INI file. File:", self.file_path)
            self.generate(self.file_path)
        

    # Create INI file to store various API credentials
    def generate(self, file_path):
        self.config['Census API'] = {}
        self.config['Google APIs'] = {}
        with open(self.file_path, 'w') as configfile:
            self.config.write(configfile)
        print("INI file created. File:", self.file_path)

    # Insert Google API keys into INI file
    # ini_google({'geocoding' : 'api_key_here'})
    def google(self, api_keys = {}):
        google = self.config['Google APIs']
        try:
            for k, v in api_keys.items():
                google[k] = v
        except:
            print("Error")
        
        with open(self.file_path, 'w') as configfile:
            self.config.write(configfile)

        print("Keys successfuly inserted:")
        print("-------------------------------")
        for k, v in api_keys.items():
            print(k,"|",google[k])

    # Read a specific variable from INI file
    # Typically used in other functions to pass API keys & passwords at runtime
    def read(self, header, variable):
        header_variable = self.config[header][variable]
        return(header_variable)