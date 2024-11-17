from interfaces.interface_logger import ILogger 
from tkinter import Text


class TkLogger(ILogger):
  def __init__(self, text_widget: Text):
    self.text_widget = text_widget
  
  def log(self, message: str):
    self.text_widget['state'] = 'normal'
    self.text_widget.insert('end', message + '\n')
    self.text_widget['state'] = 'disabled'
  
  def error(self, message: str):
    self.text_widget['state'] = 'normal'
    self.text_widget.insert('end', message + '\n')
    self.text_widget['state'] = 'disabled'
  
  def success(self, message: str):
    self.text_widget.insert('end', message + '\n')
  
  def clear(self):
    self.text_widget.delete('1.0', 'end')
    