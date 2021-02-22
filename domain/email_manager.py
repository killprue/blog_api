from data_access.repos.email_repo import EmailRepo
from domain.base_manager import BaseManager

class EmailManager(BaseManager):
    def __init__(self):
        self.email_repo = EmailRepo()

    def upload_email(self, form):
        form_info = self.populate_dict_from_form(['emailAddress','postSubscribed','howtoSubscribed'], form)
        self.email_repo.upload_email(form_info)

    def get_all_emails(self):
        return self.model_list_to_dict(self.email_repo.get_all_emails())

    def send_email(self, form):
        email_fields = ['content','subject']
        form_info = self.populate_dict_from_form(email_fields, form)
        self.email_repo.send_email(form_info)