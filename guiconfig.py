import json

class AppConfig():

    FILE = 'config.json'

    def __init__(self, *args, **kwargs):
        self.coordinates = {}
        self.iter_steps = []
        self.cmaps = []
        self.image = {}
        return super().__init__(*args, **kwargs)

    def get_config(self):
        cfg = {}
        with open(AppConfig.FILE, 'r') as f:
            cfg = json.load(f)
        self.coordinates = cfg['coordinates']
        self.iter_steps = cfg['static_data']['iter_steps']
        self.image = cfg['image_settings']
        self.cmaps = cfg['static_data']['cmaps']
        print('loading config...')
        print(cfg)

    def update_config(self, coordinates=None, image=None):
        #COORDINATES
        if coordinates is not None:
            self.coordinates = coordinates
            cfg = {}
            with open(AppConfig.FILE, 'r') as f:
                cfg = json.load(f)
            cfg['coordinates'] = coordinates
            print('saving config...')
            print(cfg)
            with open(AppConfig.FILE, 'w') as f:
                json.dump(cfg, f)
            print('config saved!')
        
        #IMAGE SETTINGS
        if image is not None:
            self.image = image
            cfg = {}
            with open(AppConfig.FILE, 'r') as f:
                cfg = json.load(f)
            cfg['image_settings'] = image
            print('saving config...')
            print(cfg)
            with open(AppConfig.FILE, 'w') as f:
                json.dump(cfg, f)
            print('config saved!')
        
            
