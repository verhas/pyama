from pyama.collector import FileCollector
from pyama.filereader import Factory


class Reader:
    def __init__(self, configurations, factory: Factory, collector: FileCollector):
        self.configurations = configurations
        self.factory = factory
        self.collector = collector

    def read(self):
        filenames = self.collector.collect()
        files = []
        for filename in filenames:
            filereader = self.factory().reader(self.configurations, filename)
            files.append(filereader.read())
        return files
