import subprocess
import os

class Lipsync():
  def __init__(self, rhubarb_path="Rhubarb-Lip-Sync-1.13.0-macOS", file=None):
    self.file = file
    self.rhubarb_path = rhubarb_path
    
  def get_features(self):
    if self.rhubarb_path == None:
      c = subprocess.run(["rhubarb", os.path.join("..", "speech.wav"), "-d", os.path.join("..", "text.txt"), "-o", os.path.join("..", "lipoutput.txt")])
    else:
      # c = subprocess.run([os.path.join(self.rhubarb_path, "rhubarb.exe"), os.path.join("..", "speech.wav"), "-d", os.path.join("..", "text.txt"), "-o", os.path.join("..", "lipoutput.txt"), "-q"])
      c = subprocess.run([os.path.join(self.rhubarb_path, "rhubarb"), os.path.join(".", "speech.wav"), "-d", os.path.join(".", "text.txt"), "-o", os.path.join(".", "lipoutput.txt"), "-q"])
      print(os.path.join("..", "speech.wav"))
    with open("lipoutput.txt", "r") as f:
      data = f.read()
      lines = data.split("\n")
      features = []
      for line in lines:
        features.append(line.split("\t"))
    return features[0:-1]


if __name__ == "__main__":
  lipsync = Lipsync("Rhubarb-Lip-Sync-1.13.0-Windows")
  print(lipsync.get_features())