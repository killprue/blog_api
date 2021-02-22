from domain.base_manager import BaseManager
from data_access.repos.home_page_repo import HomePageRepo

class HomePageManager(BaseManager):
    def __init__(self):
        self.home_page_repo = HomePageRepo()

    def edit_home_page(self, home_form):
        text_fields = ['mainSection', 'section1', 'section2', 'section3',
        'section4', 'section5']
        home_text_info = self.populate_dict_from_form(text_fields, home_form)
        self.home_page_repo.edit_home_page(home_text_info)

    def add_image(self, image_file):
        file_fields = ['mainSectionImageSource','section1ImageSource','section2ImageSource',
            'section3ImageSource', 'section4ImageSource', 'section5ImageSource']
        home_file_info = self.populate_dict_from_form(file_fields, image_file)
        return self.home_page_repo.add_image(home_file_info)

    def get_home_page(self):
        return self.home_page_repo.get_home_page().to_dict()

    def remove_image(self, form):
        fields = ['urlSource']
        image_source_url = self.populate_dict_from_form(fields, form)
        self.home_page_repo.remove_single_image_by_source(image_source_url['urlSource'])
