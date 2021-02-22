from  data_access.models.base_model import BaseModel


class HomeInfo(BaseModel):
    @staticmethod
    def from_dict(source):
        home_info = HomeInfo()
        if u'mainSection' in source:
            home_info.main_section = u'{}'.format(source[u'mainSection'])
        if u'mainSectionImageSource':
            home_info.main_section_image_source = source[u'mainSectionImageSource']
        if u'section1' in source:
            home_info.section_1 = u'{}'.format(source[u'section1'])
        if u'section1ImageSource' in source:
            home_info.section_1_image_source = source[u'section1ImageSource']
        if u'section2' in source:
            home_info.section_2 = u'{}'.format(source[u'section2'])
        if u'section2ImageSource' in source:
            home_info.section_2_image_source = source[u'section2ImageSource']
        if u'section3' in source:
            home_info.section_3 = u'{}'.format(source[u'section3'])
        if u'section3ImageSource' in source:
            home_info.section_3_image_source = source[u'section3ImageSource']
        if u'section4' in source:
            home_info.section_4 = u'{}'.format(source[u'section4'])
        if u'section4ImageSource' in source:
            home_info.section_4_image_source = source[u'section4ImageSource']
        if u'section5' in source:
            home_info.section_5 = u'{}'.format(source[u'section5'])
        if u'section5ImageSource' in source:
            home_info.section_5_image_source = source[u'section5ImageSource']
        return home_info
        
    def to_dict(self):
        home_info = {}
        if hasattr(self, 'main_section'):
            home_info['mainSection'] = u'{}'.format(self.main_section)
        if hasattr(self, 'main_section_image_source'):
            home_info['mainSectionImageSource'] = self.main_section_image_source
        if hasattr(self, 'section_1'):
            home_info['section1'] = u'{}'.format(self.section_1)
        if hasattr(self, 'section_1_image_source'):
            home_info['section1ImageSource'] = self.section_1_image_source
        if hasattr(self, 'section_2'):
            home_info['section2'] = u'{}'.format(self.section_2)
        if hasattr(self, 'section_2_image_source'):
            home_info['section2ImageSource'] = self.section_2_image_source
        if hasattr(self, 'section_3'):
            home_info['section3'] = u'{}'.format(self.section_3)
        if hasattr(self, 'section_3_image_source'):
            home_info['section3ImageSource'] = self.section_3_image_source
        if hasattr(self, 'section_4'):
            home_info['section4'] = u'{}'.format(self.section_4)
        if hasattr(self, 'section_4_image_source'):
            home_info['section4ImageSource'] = self.section_4_image_source
        if hasattr(self, 'section_5'):
            home_info['section5'] = u'{}'.format(self.section_5)
        if hasattr(self, 'section_5_image_source'):
            home_info['section5ImageSource'] = self.section_5_image_source
        return home_info

    def __repr__(self):
        return(u'HomeInfo()'.format())
            