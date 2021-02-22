from data_access.repos.post_repo import PostRepo
from domain.base_manager import BaseManager
from data_access.repos.email_repo import EmailRepo
from datetime import datetime


class PostManager(BaseManager):
    def __init__(self):
        self.post_repo = PostRepo()

    def get_all_posts_admin(self):
        return self.model_list_to_dict(self.post_repo.get_all_posts_admin())
    
    def get_all_posts(self):
        return self.model_list_to_dict(self.post_repo.get_all_posts())

    def get_single_post(self, post_title):
        return self.post_repo.get_single_post(post_title).to_dict()

    def get_single_post_admin(self, post_id):
        return self.post_repo.get_single_post_admin(post_id).to_dict()

    def get_location_posts(self, post_location):
        return self.model_list_to_dict(self.post_repo.get_location_posts(post_location))

    def create_home_post(self, request_file, post_form):
        post_fields = ['content', 'title', 'location', 'albumLink', 'createDate']
        post_info = self.populate_dict_from_form(post_fields, post_form)
        was_duplicate = self.post_repo.create_home_post(post_info, request_file)
        created_successfully = True if not was_duplicate else False
        return created_successfully

    def delete_post(self, post_id):
        self.post_repo.delete_post(post_id)

    def update_post(self, post_form):
        post_fields = ['content', 'title', 'imageSource', 'publish','location', 'albumLink']
        post_id = post_form['id']
        post_info = self.populate_dict_from_form(post_fields, post_form)
        if post_info['publish'] == "false":
            post_info['publish'] = False
        elif post_info['publish'] == "true":
            post_info['publish'] = True
        self.post_repo.update_post(post_info, post_id)
    
    def add_post_images(self, file_list, post_form):
        post_id = self.populate_dict_from_form(['id'], post_form)['id']
        return self.post_repo.add_post_images(file_list, post_id)
        
    def remove_post_image(self, form):
        form_info = self.populate_dict_from_form(['id','urlSource'], form)
        self.post_repo.remove_post_image(form_info['id'],form_info['urlSource'])
