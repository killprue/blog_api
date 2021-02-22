from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required
from firebase_admin import auth
from domain.post_manager import PostManager
from domain.howto_manager import HowToManager
from domain.email_manager import EmailManager
from domain.home_page_manager import HomePageManager
import datetime

VALID_CONTENT_TYPES = ['image/jpeg','image/png','image/jpg','image/jfif', 'image/pjp', 'image/pjpeg']


class Authenticate(Resource):
    def post(self):
        try:
            user_id = request.form['uid']
            current_user = auth.get_user(user_id)
            expires = datetime.timedelta(days=3)
            access_token = create_access_token(identity=current_user.uid, expires_delta=expires)
            return {
                    'message': 'Logged in as {}'.format(current_user.email),
                    'access_token': access_token
                    }
        except Exception as e:
            return {'message': 'Unauthorized'}, 401

class AllPostsAdmin(Resource):
    @jwt_required
    def get(self):
        try:
            post_manager = PostManager()
            return post_manager.get_all_posts_admin(), 200
        except Exception as e:
            return {'message': 'Something went wrong'}, 500

class AllHowTosAdmin(Resource):
    @jwt_required
    def get(self):
        try:
            howto_manager = HowToManager()
            return howto_manager.get_all_how_tos_admin(), 200
        except Exception as e:
            return {'message':'Something Went Wrong'}, 500

class SinglePostAdmin(Resource):
    @jwt_required
    def get(self, post_id):
        try:
            post_manager = PostManager()
            return post_manager.get_single_post_admin(post_id), 200
        except Exception as e:
            return {'message': 'Something Went wrong'}, 500

class SingleHowToAdmin(Resource):
    @jwt_required
    def get(self, post_id):
        try:
            howto_manager = HowToManager()
            return howto_manager.get_single_howto_admin(post_id),200
        except Exception as e:
            return {'message': 'Something Went Wrong'}, 500

class CreatePost(Resource):
    @jwt_required
    def post(self):
        try:
            post_manager = PostManager()
            request_file = request.files['file'] if len(request.files) > 0 else None
            created = post_manager.create_home_post(request_file, request.form)
            print(created)
            if created:
                return {'message': 'Post Created'}, 201
            else:
                return {'message': 'Bad Request -- Duplicate Title!'}, 400
        except Exception as e:
            return {'message': 'Something went wrong'}, 500

class CreateHowTo(Resource):
    @jwt_required
    def post(self):
        try:
            howto_manager = HowToManager()
            request_file = request.files['file'] if len(request.files) > 0 else None
            howto_manager.create_home_HowTo(request_file, request.form)
            return {'message':'HowTo Created'}, 201
        except Exception as e:
            return {'message':'Something went wrong'}, 500
            
class DeletePost(Resource):
    @jwt_required
    def delete(self, post_id):
        try:
            post_manager = PostManager()
            post_manager.delete_post(post_id)
            return {'message': 'Post Deleted'}, 204
        except Exception as e:
            return {'message': 'Something went wrong'}, 500

class DeleteHowTo(Resource):
    @jwt_required
    def delete(self, post_id):
        try:
            howto_manager = HowToManager()
            howto_manager.delete_howto(post_id)
            return {'message':'How To Deleted'}, 204
        except Exception as e:
            return {'message': 'Something went wrong'}, 500

class UpdatePost(Resource):
    @jwt_required
    def put(self):
        try:
            post_form = request.form
            post_manager = PostManager()
            post_manager.update_post(post_form)
            return {'message': 'Post Updated'}, 204
        except Exception as e:
            return {'message': 'Something went wrong'}, 500

class UpdateHowTo(Resource):
    @jwt_required
    def put(self):
        try:
            howto_form = request.form
            howto_manager = HowToManager()
            howto_manager.update_how_to(howto_form)
            return {'message':'Post Updated'}, 204
        except Exception as e:
            return {'message': 'Something Went Wrong'}, 500

class AddPostImages(Resource):
    @jwt_required
    def post(self):
        try:
            file_list = [request.files[image_file] for image_file in request.files]
            if file_list[0].content_type not in VALID_CONTENT_TYPES:
                return {'message': F'File type: "{file_list[0].content_type}" is not accepted. Please upload an image file.'}, 400
            post_manager = PostManager()
            url = post_manager.add_post_images(file_list, request.form)
            return {'message': 'Post Updated', 'newUrl': url}, 200
        except Exception as e:
            return {'message': 'Something went wrong'}, 500

class AddHowToImages(Resource):
    @jwt_required
    def post(self):
        try:
            file_list = []
            for image_file in request.files:
                file_list.append(request.files[image_file])
            howto_manager = HowToManager()
            howto_manager.add_howto_images(file_list, request.form)
            return {'message': 'Post Updated'}, 204
        except Exception as e:
            return {'message': 'Something went wrong'}, 500

class RemovePostImage(Resource):
    @jwt_required
    def post(self):
        try:
            post_manager = PostManager()
            post_manager.remove_post_image(request.form)
            return {'message': 'Post Updated'}, 204
        except Exception as e:
            return {'message': 'Something went wrong'}, 500

class RemoveHowToImage(Resource):
    @jwt_required
    def post(self):
        try:
            howto_manager = HowToManager()
            howto_manager.remove_howto_image(request.form)
            return {'message':'How To Updated'}, 204
        except Exception as e:
            return {'message':'Something went wrong'}, 500

class SendEmail(Resource):
    @jwt_required
    def post(self):
        try:
            email_manager = EmailManager()
            email_manager.send_email(request.form)
            return {'message':'Email Send'}, 204
        except Exception as e:
            return {'message':'Something went wrong'}, 500

class EditHomePage(Resource):
    @jwt_required
    def post(self):
        try:
            home_page_manager = HomePageManager()
            home_page_manager.edit_home_page(request.form)
            return {'message':'Home Page Edited'}, 204
        except Exception as e:
            return {'message':'Something went wrong'}, 500

class AddHomeImage(Resource):
    @jwt_required
    def post(self):
        try:
            file_list = [request.files[image_file] for image_file in request.files]
                
            if file_list[0].content_type not in VALID_CONTENT_TYPES:
                return {'message': F'File type: "{file_list[0].content_type}" is not accepted. Please upload an image file.'}, 400

            home_page_manager = HomePageManager()
            url = home_page_manager.add_image(request.files)
            return {'message':'Home Page Edited', 'newUrl': url}, 200
        except Exception as e:
            return {'message':'Something went wrong'}, 500

class RemoveHomeImage(Resource):
    @jwt_required
    def post(self):
        try:
            home_page_manager = HomePageManager()
            home_page_manager.remove_image(request.form)
            return {'message':'Home Page Edited'}, 204
        except Exception as e:
            return {'message':'Something went wrong'}, 500

class GetHomePage(Resource):
    @jwt_required
    def get(self):
        try:
            home_page_manager = HomePageManager()
            return home_page_manager.get_home_page(), 200
        except Exception as e:
            return {'message':'Something went wrong'}, 500

class GetAllEmails(Resource):
    @jwt_required
    def get(self):
        try:
            email_manager = EmailManager()
            return email_manager.get_all_emails()
        except Exception as e:
            return {'message':'Something went wrong'}, 500
