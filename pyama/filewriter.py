

class FileWriter:
    def __init__(self,file):
        self.file = file

    def write(self):
        with open(self.file.name,"w") as f:
            for segment in self.file.segments:
                f.write("".join(segment.text))
