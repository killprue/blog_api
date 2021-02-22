from  data_access.models.base_model import BaseModel

class HowTo(BaseModel):
    @staticmethod
    def from_dict(source):
        howto = HowTo()
        if u'title' in source:
            howto.title = source[u'title']
        if u'introduction' in source:
            howto.introduction = source[u'introduction']
        if u'subject' in source:
            howto.subject = source[u'subject']
        if u'content' in source:    
            howto.content = source[u'content']
        if u'imageSource' in source:
            howto.image_source = source[u'imageSource']
        if u'publish' in source:
            howto.publish = source[u'publish']
        if u'id' in source:
            howto.id = source[u'id']
        if u'createDate' in source:
            howto.create_date = source[u'createDate']
        if u'lastUpdate' in source:
            howto.last_update = source[u'lastUpdate']
        return howto
        
    def to_dict(self):
        howto = {}
        if hasattr(self, 'title'):
            howto['title'] = u'{}'.format(self.title)
        if hasattr(self, 'introduction'):
            howto['introduction'] = u'{}'.format(self.introduction)
        if hasattr(self, 'subject'):
            howto['subject'] = u'{}'.format(self.subject)
        if hasattr(self, 'content'):    
            howto['content'] = u'{}'.format(self.content)
        if hasattr(self, 'image_source'):
            howto['imageSource'] = self.image_source
        if hasattr(self, 'publish'):
            howto['publish'] = self.publish
        if hasattr(self, 'id'):
            howto['id'] = u'{}'.format(self.id)
        if hasattr(self, 'create_date'):
            howto['createDate'] = self.create_date
        if hasattr(self, 'last_update'):
            howto['lastUpdate'] = self.last_update    
        return howto

    def __repr__(self):
        return(u'Howto(title={}, content={}, introduction={}, subject={} image_source={}, id={})'.format(
                    self.title if hasattr(self, 'title') else None,
                    self.content if hasattr(self, 'content') else None,
                    self.introduction if hasattr(self, 'introduction') else None,
                    self.subject if hasattr(self, 'subject') else None,
                    self.image_source if hasattr(self, 'image_source') else None,
                    self.id if hasattr(self, 'id') else None))
            