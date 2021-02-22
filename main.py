from flask import Flask
import firebase_admin
from firebase_admin import credentials
from flask_cors import CORS
from flask_restful import Api
from flask_jwt_extended import JWTManager
from resources import ui_resources, admin_resources
app = Flask(__name__)
api = Api(app)
app.config['JWT_SECRET_KEY'] = 'c9f392c7c46e4034bd9d49dd8d526facae9df642c772a384'
app.config['PROPAGATE_EXCEPTIONS'] = True
jwt = JWTManager(app)
# CORS(app, resources={ r"/*": {"origins": ["https://rvawol.com", "https://rvawol-admin-9481a.firebaseapp.com"]}})
CORS(app, resources={ r"/*": {"origins": ["http://localhost:4300", "http://localhost:4200"]}})
cred = credentials.Certificate("./firebase-adminsdk-llegn.json")
firebase_admin.initialize_app(cred, {
    'storageBucket': 'rvawol.appspot.com'
})
#region Admin endpoints
api.add_resource(admin_resources.AllPostsAdmin, '/admin/all-posts')
api.add_resource(admin_resources.AllHowTosAdmin, '/admin/how-tos')
api.add_resource(admin_resources.CreatePost, '/admin/create-post')
api.add_resource(admin_resources.Authenticate, '/admin/authenticate')
api.add_resource(admin_resources.DeletePost, '/admin/delete-post/<post_id>')
api.add_resource(admin_resources.DeleteHowTo, '/admin/delete-how-to/<post_id>')
api.add_resource(admin_resources.SinglePostAdmin, '/admin/single-post/<post_id>')
api.add_resource(admin_resources.SingleHowToAdmin, '/admin/single-how-to/<post_id>')
api.add_resource(admin_resources.UpdatePost, '/admin/update-post')
api.add_resource(admin_resources.UpdateHowTo,'/admin/update-how-to')
api.add_resource(admin_resources.AddPostImages, '/admin/add-post-images')
api.add_resource(admin_resources.AddHowToImages, '/admin/add-howto-images')
api.add_resource(admin_resources.RemovePostImage, '/admin/remove-post-image')
api.add_resource(admin_resources.RemoveHowToImage, '/admin/remove-howto-image')
api.add_resource(admin_resources.CreateHowTo, '/admin/create-how-to')
api.add_resource(admin_resources.SendEmail, '/admin/send-email')
api.add_resource(admin_resources.EditHomePage, '/admin/edit-home-page')
api.add_resource(admin_resources.AddHomeImage, '/admin/add-home-page-image')
api.add_resource(admin_resources.RemoveHomeImage, '/admin/remove-home-page-image')
api.add_resource(admin_resources.GetHomePage, '/admin/get-home-page')
api.add_resource(admin_resources.GetAllEmails, '/admin/get-all-emails')
# endregion

# region Ui endpoints
api.add_resource(ui_resources.HomePage, '/', '/home')
api.add_resource(ui_resources.AllPosts, '/get-all-posts')
api.add_resource(ui_resources.SinglePost, '/single-post/<post_title>')
api.add_resource(ui_resources.LocationPosts, '/location-posts/<post_location>')
api.add_resource(ui_resources.AllHowTos, '/get-all-how-tos')
api.add_resource(ui_resources.GetSingleHowTo, '/get-single-how-to/<howto_title>')
api.add_resource(ui_resources.PostEmail, '/email-sign-up')
# endregion
