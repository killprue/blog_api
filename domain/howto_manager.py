from data_access.repos.howto_repo import HowToRepo
from data_access.repos.email_repo import EmailRepo
from domain.base_manager import BaseManager
from datetime import datetime


class HowToManager(BaseManager):
    def __init__(self):
        self.howto_repo = HowToRepo()

    def get_all_how_tos_admin(self):
        return self.model_list_to_dict(self.howto_repo.get_all_how_tos_admin())

    def get_all_how_tos(self):
        return self.model_list_to_dict(self.howto_repo.get_all_how_tos())

    def get_single_howto_admin(self, post_id):
        return self.howto_repo.get_single_howto_admin(post_id).to_dict()

    def get_single_howto(self, howto_title):
        return self.howto_repo.get_single_howto(howto_title).to_dict()

    def create_home_HowTo(self, request_file, howto_form):
        howto_fields = ['content','introduction','subject','title']
        howto_info = self.populate_dict_from_form(howto_fields, howto_form)
        self.howto_repo.create_home_HowTo(howto_info, request_file)

    def delete_howto(self, howto_id):
        self.howto_repo.delete_howto(howto_id)

    def update_how_to(self, howto_form):
        howto_fields = ['content','title','subject','introduction','publish','imageSource']
        howto_id = howto_form['id']
        howto_info = self.populate_dict_from_form(howto_fields, howto_form)
        if howto_info['publish'] == "false":
            howto_info['publish'] = False
        elif howto_info['publish'] == "true":
            howto_info['publish'] = True
        self.howto_repo.update_how_to(howto_info, howto_id)

    def add_howto_images(self, file_list, howto_form):
        howto_id = self.populate_dict_from_form(['id'], howto_form)['id']
        self.howto_repo.add_howto_images(file_list, howto_id)

    def remove_howto_image(self, form):
        form_info = self.populate_dict_from_form(['id','urlSource'], form)
        self.howto_repo.remove_howto_image(form_info['id'],form_info['urlSource'])
