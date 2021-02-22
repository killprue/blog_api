from data_access.models.howto_model import HowTo
from datetime import datetime
from data_access.repos.base_repo import BaseRepo
from data_access.repos.email_repo import EmailRepo
import smtplib
import string
import uuid


class HowToRepo(BaseRepo):
    
    def get_all_how_tos_admin(self):
        howto_list = []
        for howto in self.db.collection(u'howtos').stream():
            admin_howto = HowTo.from_dict(howto.to_dict())
            admin_howto.id = howto.id
            admin_howto.last_update = datetime.utcfromtimestamp(int(howto.update_time.seconds)).strftime('%Y-%m-%d %H:%M:%S')
            admin_howto.create_date = datetime.utcfromtimestamp(int(howto.create_time.seconds)).strftime('%Y-%m-%d %H:%M:%S')
            howto_list.append(admin_howto)
        return howto_list

    def get_all_how_tos(self):
        howto_list = []
        for howto in self.db.collection(u'howtos').stream():
            howto_info = howto.to_dict()
            ui_howto = HowTo.from_dict(howto_info)
            if ui_howto.publish:
                ui_howto.last_update = datetime.utcfromtimestamp(int(howto.update_time.seconds)).strftime('%Y-%m-%d %H:%M:%S')
                ui_howto.create_date = howto_info['date']
                howto_list.append(ui_howto)
        return howto_list

    def get_single_howto_admin(self, post_id):
        howto = self.db.collection(u'howtos').document(u'{}'.format(post_id)).get()
        admin_howto = HowTo.from_dict(howto.to_dict())
        admin_howto.id = post_id
        return admin_howto

    def get_single_howto(self, howto_title):
        howtos = []
        howto = self.db.collection(u'howtos')
        howto_title = howto_title.replace('-',' ')
        for howto in howto.where(u'title',u'==',u'{}'.format(howto_title)).stream():
            how_to = howto.to_dict()
            how_to_model = HowTo.from_dict(how_to)
            if how_to_model.publish:
                howtos.append(how_to_model)
        single_howto = howtos[0] if len(howtos) > 0 else HowTo.from_dict({})
        return single_howto

    def create_home_HowTo(self, howto_info, request_file):
        doc_ref = self.db.collection(u'howtos').document()
        if request_file is not None:
            blob = self.bucket.blob(u'{}'.format(str(uuid.uuid4()) + '_' + request_file.filename) )
            blob.upload_from_string(
                request_file.read(),
                request_file.content_type
            )
            blob.make_public()
            howto_info['imageSource'] = [blob.public_url]
        howto_model = HowTo.from_dict(howto_info)
        howto_model = howto_model.to_dict()
        current_date = datetime.now()
        current_date = current_date.strftime("%x") + " " + current_date.strftime("%X")
        howto_model['date'] = current_date
        howto_model['updated'] = current_date
        howto_model['publish'] = False
        doc_ref.set(howto_model)


    def delete_howto(self, howto_id):
        howto_to_delete = self.db.collection(u'howtos').document(u'{}'.format(howto_id))
        howto_to_delete_dict = howto_to_delete.get().to_dict()
        if 'imageSource' in howto_to_delete_dict.keys():
            for urlSource in howto_to_delete_dict['imageSource']:
                blob_name= urlSource.split('/')[-1]
                blob = self.bucket.blob(blob_name)
                blob.delete()
        howto_to_delete.delete()

    def update_how_to(self, howto_info, howto_id):
        how_to_item = self.db.collection(u'howtos').document(u'{}'.format(howto_id))
        how_to_info_transfer = how_to_item.get().to_dict()
        howto_info['imageSource'] = how_to_info_transfer['imageSource']
        if howto_info['publish'] == True and how_to_info_transfer['publish'] == False:
            email_manager = EmailRepo()
            title = howto_info['title']
            msg = f'Subject: {title}\n\n Rvawol Has A New How To!'
            email_manager.send_all_notification(msg, 'howto')
        if bool(how_to_info_transfer['publish']) == True:
            howto_info['publish'] = True
        current_date = datetime.now()
        current_date = u'{}'.format(current_date.strftime("%x") +" "+current_date.strftime("%X"))
        howto_info['updated'] = current_date
        how_to_item.update(howto_info)
    
    def add_howto_images(self, file_list, howto_id):
        howto_to_update = self.db.collection(u'howtos').document(u'{}'.format(howto_id))
        howto_info = howto_to_update.get().to_dict()

        for image in file_list:
            blob = self.bucket.blob(u'{}'.format(str(uuid.uuid4()) + '_' + image.filename))
            blob.upload_from_string(
                image.read(),
                image.content_type
            )
            blob.make_public()
            if 'imageSource' in howto_info:
                howto_info['imageSource'].append(blob.public_url)
            else:
                howto_info['imageSource'] = [blob.public_url]

        howto_to_update.update(howto_info)

    def remove_howto_image(self, howto_id, url_source):
        howto_to_update = self.db.collection(u'howtos').document(u'{}'.format(howto_id))
        howto_info = howto_to_update.get().to_dict()
        howto_info['imageSource'].remove(url_source)
        blob_name = url_source.split('/')[-1]
        blob = self.bucket.blob(blob_name)
        blob.delete()
        howto_to_update.update(howto_info)
