from data_access.repos.base_repo import BaseRepo
from data_access.models.home_info_model import HomeInfo
import uuid


class HomePageRepo(BaseRepo):
    def __init__(self):
        super(HomePageRepo, self).__init__()
        self.collection_ref = self.db.collection(u'home')
        for doc in self.collection_ref.stream():
            self.home_doc_ref = doc

    def edit_home_page(self, home_text_info): 
        doc_ref = self.collection_ref.document(self.home_doc_ref.id)
        doc_ref.update(home_text_info)

    def add_image(self, file_info):
        populated_file_info = {}
        doc_ref = self.collection_ref.document(self.home_doc_ref.id)
        for key, upload_file in file_info.items():
                blob = self.bucket.blob(u'{}'.format(str(uuid.uuid4()) + '_' + key) )
                blob.upload_from_string(
                    upload_file.read(),
                    upload_file.content_type
                )
                blob.make_public()
                home_info = doc_ref.get().to_dict()
                if home_info[key]:
                    home_info[key].append(blob.public_url)
                else:
                    home_info[key] = [blob.public_url]

                doc_ref.update(home_info)
        return blob.public_url

    def remove_single_image_by_source(self, image_source_url):
        doc_ref = self.collection_ref.document(self.home_doc_ref.id)
        field_key = image_source_url.split('_')[1]
        blob_name = image_source_url.split('/')[-1]
        blob = self.bucket.blob(blob_name)
        blob.delete()
        home_page_info = doc_ref.get().to_dict()
        home_page_info[field_key].remove(image_source_url)
        doc_ref.update(home_page_info)

    def get_home_page(self):
        home_page = self.home_doc_ref.to_dict()
        return HomeInfo.from_dict(home_page)
