import abc

class TargetStatusListener:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def OnTargetStatusUpdate(targetState):
        """ Implement this in your class """
