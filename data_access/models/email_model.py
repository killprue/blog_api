from  data_access.models.base_model import BaseModel

class Email(BaseModel):
    @staticmethod
    def from_dict(source):
        email = Email()
        if u'emailAddress' in source:
            email.email_address = source[u'emailAddress']
        if u'postSubscribed' in source:
            email.post_subscribed = True if source[u'postSubscribed'] in ["True", "true", True] else False
        if u'howtoSubscribed' in source:
            email.howto_subscribed = True if source[u'howtoSubscribed'] in ["True", "true", True] else False
        if u'id' in source:
            email.id = source[u'id']
        if u'createDate' in source:
            email.create_date = source[u'createDate']
        if u'lastUpdate' in source:
            email.last_update = source[u'lastUpdate']    
        return email
        
    def to_dict(self):
        email = {}
        if hasattr(self, 'email_address'):
            email['emailAddress'] = u'{}'.format(self.email_address)
        if hasattr(self, 'post_subscribed'):
            email['postSubscribed'] = self.post_subscribed
        if hasattr(self, 'howto_subscribed'):
            email['howtoSubscribed'] = self.howto_subscribed
        if hasattr(self, 'id'):
            email['id'] = u'{}'.format(self.id)
        if hasattr(self, 'create_date'):
            email['createDate'] = self.create_date
        if hasattr(self, 'last_update'):
            email['lastUpdate'] = self.last_update
        return email

    def __repr__(self):
        return(u'Email(emailAddress={}, post_subscribed={}, howto_subscribed={}, id={})'.format(
                    self.email_address if hasattr(self, 'email_address') else None,
                    self.post_subscribed if hasattr(self, 'post_subscribed') else None,
                    self.howto_subscribed if hasattr(self, 'howto_subscribed') else None,
                    self.id if hasattr(self, 'id') else None))
            