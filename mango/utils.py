BASE_URL = "https://mangooapi.onrender.com"

def gpt_4o():
    return 'gpt-4o'

def blackbox():
    return 'blackbox'
    
class Models:
  def __init__(self):
      self.gpt4o = gpt_4o()
      self.blackbox = blackbox()
