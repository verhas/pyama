class Segment:
    def __init__(self, name, filename):
        self.name = name
        self.filename = filename
        self.text = []
        self.next = None
        self.previous = None
        self.modified = False

    def add(self, line):
        self.text.append(line)


class File:
    def __init__(self, filename, segments):
        self.name = filename
        self.segments = segments

    def modified(self):
        return any([segment.modified for segment in self.segments])
