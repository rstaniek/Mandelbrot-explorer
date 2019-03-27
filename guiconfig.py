import json, uuid
from time import gmtime, strftime

class AppConfig():

    FILE = 'config.json'

    def __init__(self, *args, **kwargs):
        self.coordinates = {}
        self.iter_steps = []
        self.cmaps = []
        self.image = {}
        self._exportable = {}
        return super().__init__(*args, **kwargs)

    def get_config(self):
        cfg = {}
        print('loading config...')
        with open(AppConfig.FILE, 'r') as f:
            cfg = json.load(f)
        self.coordinates = cfg['coordinates']
        self.iter_steps = cfg['static_data']['iter_steps']
        self.image = cfg['image_settings']
        self.cmaps = cfg['static_data']['cmaps']
        print(cfg)
        #exportable
        self._exportable = dict(cfg)
        self._exportable.pop('static_data')
        

    def update_config(self, coordinates=None, image=None):
        #COORDINATES
        if coordinates is not None:
            self.coordinates = coordinates
            self._exportable['coordinates'] = coordinates
            cfg = {}
            with open(AppConfig.FILE, 'r') as f:
                cfg = json.load(f)
            cfg['coordinates'] = coordinates
            print('saving config... [coordinates]')
            with open(AppConfig.FILE, 'w') as f:
                json.dump(cfg, f, indent=4)
            print('config saved!')
        
        #IMAGE SETTINGS
        if image is not None:
            self.image = image
            self._exportable['image_settings'] = image
            cfg = {}
            with open(AppConfig.FILE, 'r') as f:
                cfg = json.load(f)
            cfg['image_settings'] = image
            print('saving config... [image_settings]')
            with open(AppConfig.FILE, 'w') as f:
                json.dump(cfg, f, indent=4)
            print('config saved!')

    #exports the config from the last render run
    def export_config(self):
        cfg = {}
        cfg['id'] = str(uuid.uuid4())
        cfg['date'] = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        cfg['value'] = self._exportable
        print('Exporting config...')
        with open('config.exported.json', 'r') as f:
            current = json.load(f)
        current['exports'].insert(0, cfg)
        with open('config.exported.json', 'w') as f:
            json.dump(current, f, indent=4)
        print('Config exported!')

        
            
