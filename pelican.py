'''Right now designed to be one driver for each thermostat.
(Could be one driver for every thermostat if we want)
for some reason in BaseRegister class,
the python class for everything is set to int. Reg_types are bit or byte
'''
import requests
import xmltodict
import json

class Pelican_Client():
    def __init__(self, config_file):
        with open(config_file) as json_config:
            self.config_dict = json.load(json_config)

        self.url = self.config_dict.get("url")
        self.username = self.config_dict.get('username')
        self.password = self.config_dict.get('password')
        self.object = self.config_dict.get('object')
        self.thermostat_names = self.config_dict.get('thermostat_names')
        self.object = self.config_dict.get('object','Thermostat')
        self.point_list = self.config_dict.get('point_list')
        self.payload_dict = {'username': self.username,
                             'password': self.password,
                             'request': '',
                             'object': self.object,
                             'value': self.point_list}
    
    def get_points(self, points, thermostat_names):
        payload = self.payload_dict.copy()
        payload['value'] = ';'.join(points)
        payload['request'] = 'get'
        self.get_selection(payload, thermostat_names)
        # print(payload)
        r = requests.get(self.url,payload)
        return xmltodict.parse(r.content).get('result')

    def set_points(self, point_val_dict, thermostat_names):
        payload = self.payload_dict.copy()
        payload['value'] = ''
        for point_name, value in point_val_dict.items():
            payload['value'] += f'{point_name}:{value};'
        
        self.get_selection(payload, thermostat_names)
        payload['request'] = 'set'
        # print(payload)
        r = requests.get(self.url, payload)
        return dict(xmltodict.parse(r.content))
        
    def scrape_all(self):
        # 'all' would also work for the selections, rather than all the names
        point_data = self.get_points(self.point_list, self.thermostat_names)
        return point_data# .get('Thermostat')

    def get_selection(self,payload, thermostat_names):
        if isinstance(thermostat_names, list):
            payload['selections'] = ';'.join([f'name:{x}' for x in thermostat_names])
        else:
            payload['selection'] = f'name:{thermostat_names}'
