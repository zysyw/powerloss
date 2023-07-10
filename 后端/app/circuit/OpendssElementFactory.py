
class OpendssElementFactory:
    def __init__(self):
        self._creators = {}

    def register_opendss_element(self, opendss_element_type):
        def decorator(creator):
            self._creators[opendss_element_type] = creator
            return creator
        return decorator

    def create_opendss_element(self, opendss_element_type, df):
        creator = self._creators.get(opendss_element_type)
        if not creator:
            raise ValueError(opendss_element_type + ' is not registered!')
        return creator(df, opendss_element_type)

ElementFactory = OpendssElementFactory()