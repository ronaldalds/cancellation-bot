from abc import ABC, abstractmethod


class repository(ABC):
    @abstractmethod
    def create_log(self):
        pass

    @abstractmethod
    def read_log(self):
        pass

    @abstractmethod
    def read_user_grupo(self):
        pass

    @abstractmethod
    def read_user_id(self):
        pass