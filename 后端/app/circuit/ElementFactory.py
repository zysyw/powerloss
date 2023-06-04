from linecode import Linecode
from line import Line

class ElementFactory:
    def create_element(self, type, df):
        if type == "LINECODE":
            return Linecode(df)
        elif type == "LINE":
            return Line(df)
        else:
            raise ValueError("Invalid type")