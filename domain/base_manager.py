class BaseManager():
    
    def populate_dict_from_form(self, dict_keys, form):
        populated_dict = {}
        for field in form:
            if field in dict_keys and form[field]:
                populated_dict[field] = form[field]
        return populated_dict


    def model_list_to_dict(self, model_list):
        dict_list = []
        for model in model_list:
            dict_list.append(model.to_dict())
        return dict_list
