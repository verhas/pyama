class Segment:
    def __init__(self, name, filename):
        # START SNIPPET segment_structure
        self.name = name
        self.filename = filename
        self.text = []
        self.next = None
        self.previous = None
        self.modified = False
        self.parameters = {}
        # END SNIPPET

    def __str__(self):
        return "[Segment %s/%s %s]" % (self.filename, self.name, "(m)" if self.modified else "")

    def add(self, line):
        self.text.append(line)


class File:
    def __init__(self, filename, segments):
        self.name = filename
        self.segments = segments

    def modified(self):
        return any([segment.modified for segment in self.segments])
