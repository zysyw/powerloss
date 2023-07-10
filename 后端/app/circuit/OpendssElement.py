from abc import ABCMeta, abstractmethod

class OpendssElement(metaclass=ABCMeta):
    @abstractmethod
    def check(self):
        """
        check elements from iterable
        """
    @abstractmethod
    def convert(self):
        """
        convert df to opendss scripts
        """
