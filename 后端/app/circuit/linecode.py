from .OpendssElement import OpendssElement
from .OpendssElementFactory import ElementFactory
from .df2opendss import create_scripts_from_df

@ElementFactory.register_opendss_element('LINECODE')
class Linecode(OpendssElement):
    def __init__(self, df, element_type):
        self.df = df
        self.element_type = element_type
    
    def check(self):
        print("Linecode is OK.")
        return True
    
    def convert(self):
        return create_scripts_from_df(self.df, self.element_type)

    