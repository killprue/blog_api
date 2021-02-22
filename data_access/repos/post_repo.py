from data_access.models.post_model import Post
from datetime import datetime
from data_access.repos.base_repo import BaseRepo
from data_access.repos.email_repo import EmailRepo
import smtplib
import string
import uuid

class PostRepo(BaseRepo):
    def get_all_posts_admin(self):
        post_list = []
        for post in self.db.collection(u'posts').stream():
            admin_post = Post.from_dict(post.to_dict())
            admin_post.id = post.id            
            post_list.append(admin_post)
        return post_list
    
    def get_all_posts(self):
        post_list = []
        for post in self.db.collection(u'posts').stream():
            post_info = post.to_dict()
            ui_post = Post.from_dict(post_info)
            if ui_post.publish:
                ui_post.create_date = post_info['date']
                post_list.append(ui_post)
        return post_list
    
    def get_single_post(self, post_title):
        posts = []
        post = self.db.collection(u'posts')
        post_title = post_title.replace('-',' ')
        for post in post.where(u'title',u'==',u'{}'.format(post_title)).stream():
            post = post.to_dict()
            post_model = Post.from_dict(post)
            if post_model.publish:
                posts.append(post_model)
        single_post = posts[0] if len(posts) > 0 else Post.from_dict({})
        return single_post

    def get_single_post_admin(self, post_id):
        post = self.db.collection(u'posts').document(u'{}'.format(post_id)).get()
        admin_post = Post.from_dict(post.to_dict())
        admin_post.id = post_id
        return admin_post

    def get_location_posts(self, post_location):
        posts = []
        post = self.db.collection(u'posts')
        post_location = post_location.replace('-', " ")
        normal_case_posts = post.where(u'location',u'==',u'{}'.format(post_location)).stream()
        upper_case_posts = post.where(u'location',u'==',u'{}'.format(string.capwords(post_location))).stream()
        for post in normal_case_posts:
            location_post = Post.from_dict(post.to_dict())
            posts.append(location_post)
        for post in upper_case_posts:
            location_post = Post.from_dict(post.to_dict())
            posts.append(location_post)
        return posts

    def create_home_post(self, post_info, request_file):
        duplicate_title = False
        posts = self.db.collection(u'posts')
        title = post_info['title']
        for post in posts.where(u'title',u'==',u'{}'.format(title)).stream():
            duplicate_title = True

        if not duplicate_title:
            doc_ref = self.db.collection(u'posts').document()
            if request_file is not None:
                blob = self.bucket.blob(u'{}'.format(str(uuid.uuid4()) + '_' + request_file.filename) )
                blob.upload_from_string(
                    request_file.read(),
                    request_file.content_type
                )
                blob.make_public()
                post_info['imageSource'] = [blob.public_url]
            post_model = Post.from_dict(post_info)
            post_model = post_model.to_dict()
            som = post_info['createDate'].split("T")
            create_date = post_info['createDate'].split("T")[0] + " " + "12:00"
            post_model['date'] = create_date
            post_model['publish'] = False
            doc_ref.set(post_model)
        return duplicate_title
                
    def delete_post(self, post_id):
        post_to_delete = self.db.collection(u'posts').document(u'{}'.format(post_id))
        post_to_delete_dict = post_to_delete.get().to_dict()
        if 'imageSource' in post_to_delete_dict.keys():
            for urlSource in post_to_delete_dict['imageSource']:
                blob_name = urlSource.split('/')[-1]
                blob = self.bucket.blob(blob_name)
                blob.delete()
        post_to_delete.delete()

    def update_post(self, post_info, post_id):
        post_to_update = self.db.collection(u'posts').document(u'{}'.format(post_id))
        post_info_to_transfer = post_to_update.get().to_dict()
        post_info['imageSource'] = post_info_to_transfer['imageSource']
        if post_info['publish'] == True and post_info_to_transfer['publish'] == False:
            email_manager = EmailRepo()
            subject = post_info['title']
            img = post_info['imageSource'][0]
            body = post_info['content']
            content = f"\n\n <div><h4>RV-AWOL Has a New Post!<h4></div>"
            email_manager.send_all_notification(subject, content, 'post', img, body)
        if bool(post_info_to_transfer['publish']) == True:
            post_info['publish'] = True
        current_date = datetime.now()
        current_date = u'{}'.format(current_date.strftime("%x") +" "+current_date.strftime("%X"))
        post_info['updated'] = current_date
        post_to_update.update(post_info)
        
    def add_post_images(self, file_list, post_id):
        post_to_update = self.db.collection(u'posts').document(u'{}'.format(post_id))
        post_info = post_to_update.get().to_dict()

        for image in file_list:
            blob = self.bucket.blob(u'{}'.format(str(uuid.uuid4()) + '_' + image.filename))
            blob.upload_from_string(
                image.read(),
                image.content_type
            )
            blob.make_public()
            if 'imageSource' in post_info:
                post_info['imageSource'].append(blob.public_url)
            else:
                post_info['imageSource'] = [blob.public_url]

        post_to_update.update(post_info)
        return blob.public_url

    def remove_post_image(self, post_id, url_source):
        post_to_update = self.db.collection(u'posts').document(u'{}'.format(post_id))
        post_info = post_to_update.get().to_dict()
        post_info['imageSource'].remove(url_source)
        blob_name = url_source.split('/')[-1]
        blob = self.bucket.blob(blob_name)
        blob.delete()
        post_to_update.update(post_info)
