from functools import reduce
from operator import getitem

from jsondler import JsonEntry


class ModelScheme(JsonEntry):

    method_name_key = "method_name"
    model_path_key = "model_path"
    params_dict_key = "params_dict"
    basic_models_key = "basic_models"

    method_name_0 = None
    model_path_0 = None
    params_dict_0 = dict()
    basic_models_0 = dict()

    def __init__(self, method_name=method_name_0, model_path=model_path_0, params_dict=None, basic_models=None):
        if basic_models is None:
            basic_models = self.basic_models_0
        if params_dict is None:
            params_dict = self.params_dict_0

        self.method_name = method_name
        self.model_path = model_path
        self.params_dict = params_dict
        self.basic_models = basic_models

    @classmethod
    def attr_scheme(cls):
        attr_scheme={
            'method_name': (cls.method_name_key,),
            'model_path': (cls.model_path_key,),
            'params_dict': (cls.params_dict_key,),
            'basic_models': (cls.basic_models_key,),
        }
        return attr_scheme

    @classmethod
    def load_from_dict(cls, in_dict):
        model_scheme = super(ModelScheme, cls).load_from_dict(in_dict=in_dict)
        for basic_model_key in model_scheme.basic_models:
            model_scheme.basic_models[basic_model_key] = \
                cls.load_from_dict(in_dict=model_scheme.basic_models[basic_model_key])
        return model_scheme

    def get_json(self):
        got_json = super(ModelScheme, self).get_json()
        for basic_model_key in reduce(getitem, self.attr_scheme()["basic_models"], got_json):
            reduce(getitem, self.attr_scheme()["basic_models"], got_json)[basic_model_key] = \
                reduce(getitem, self.attr_scheme()["basic_models"], got_json)[basic_model_key].get_json()
        return got_json
