from  data_access.models.base_model import BaseModel

class Post(BaseModel):
    @staticmethod
    def from_dict(source):
        post = Post()
        if u'title' in source:
            post.title = source[u'title']
        if u'albumLink' in source:
            post.album_link = source[u'albumLink']
        if u'location' in source:
            post.location = source[u'location']
        if u'content' in source:    
            post.content = source[u'content']
        if u'imageSource' in source:
            post.image_source = source[u'imageSource']
        if u'publish' in source:
            post.publish = source[u'publish']
        if u'id' in source:
            post.id = source[u'id']   
        if u'createDate' in source:
            post.create_date = source[u'createDate']
        return post
        
    def to_dict(self):
        post = {}
        if hasattr(self, 'title'):
            post['title'] = u'{}'.format(self.title)
        if hasattr(self, 'album_link'):
            post['albumLink'] = u'{}'.format(self.album_link)
        if hasattr(self, 'location'):
            post['location'] = u'{}'.format(self.location)
        if hasattr(self, 'content'):    
            post['content'] = u'{}'.format(self.content)
        if hasattr(self, 'image_source'):
            post['imageSource'] = self.image_source
        if hasattr(self, 'publish'):
            post['publish'] = self.publish
        if hasattr(self, 'id'):
            post['id'] = u'{}'.format(self.id)    
        if hasattr(self, 'create_date'):
            post['createDate'] = self.create_date
        return post

    def __repr__(self):
        return(u'Post(title={}, location={}, content={}, image_source={}, id={})'.format(
                    self.title if hasattr(self, 'title') else None,
                    self.location if hasattr(self, 'location') else None,
                    self.content if hasattr(self, 'content') else None,
                    self.image_source if hasattr(self, 'image_source') else None,
                    self.id if hasattr(self, 'id') else None,
                    self.album_link if hasattr(self, 'album_link') else None))
            