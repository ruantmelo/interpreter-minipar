from abc import ABC, abstractmethod

class ILogger(ABC):

  @abstractmethod
  def __init__(self, **kwargs):
      """Construtor."""
      pass
  
  @abstractmethod
  def log(self, message: str):
    pass

  @abstractmethod
  def error(self, message: str):
    pass

  @abstractmethod
  def success(self, message: str):
    pass

  @abstractmethod
  def clear(self):
    pass