from abc import ABC, abstractmethod

class BaseModel(ABC):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    @abstractmethod
    def from_dict(source):
        pass

    @abstractmethod
    def to_dict(self):
        pass

    @abstractmethod
    def __repr__(self):
        pass
