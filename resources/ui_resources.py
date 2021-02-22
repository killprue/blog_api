from flask_restful import Resource
from flask import request
from domain.post_manager import PostManager
from domain.howto_manager import HowToManager
from domain.email_manager import EmailManager
from domain.home_page_manager import HomePageManager

class HomePage(Resource):
    def get(self):
        try:
            home_page_manager = HomePageManager()
            return home_page_manager.get_home_page(), 200
        except Exception as e:
            return {'message':'Something Went Wrong'}, 500

class AllPosts(Resource):
    def get(self):
        try:
            post_manager = PostManager()
            return post_manager.get_all_posts(), 200
        except Exception as e:
            return {'message':'Something Went Wrong'}, 500

class SinglePost(Resource):
    def get(self, post_title):
        try:
            post_manager = PostManager()
            return post_manager.get_single_post(post_title), 200
        except Exception as e:
            return {'message':'Something Went Wrong'}, 500

class LocationPosts(Resource):
    def get(self, post_location):
        try:
            post_manager = PostManager()
            return post_manager.get_location_posts(post_location), 200
        except Exception as e:
            return {'message','Something Went Wrong'}, 500

class AllHowTos(Resource):
    def get(self):
        try:
            howto_manager = HowToManager()
            return howto_manager.get_all_how_tos()
        except Exception as e:
            return {'message': 'Something Went Wrong'}, 500

class GetSingleHowTo(Resource):
    def get(self, howto_title):
        try:
            howto_manager = HowToManager()
            return howto_manager.get_single_howto(howto_title)
        except Exception as e:
            return {'message': 'Something Went Wrong'}, 500

class PostEmail(Resource):
    def post(self):
        try:
            email_manager = EmailManager()
            email_manager.upload_email(request.form)
            return {'message':'Email Posted'}, 204
        except Exception as e:
            return {'message':'Something went wrong'}, 500
