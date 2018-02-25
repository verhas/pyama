from pyama.reader import Reader
from pyama.filereader import Factory
from pyama.collector import FileCollector
from pyama.filewriter import FileWriter


class Processor:
    def __init__(self, configs, path):
        self.reader = Reader(configs, Factory, FileCollector(configs, path))
        self.passes = max([x.max_passes for x in configs])
        self.handlers = set()
        for config in configs:
            for handler in config.handlers:
                self.handlers.add(handler)

    def read_files(self):
        self.files = self.reader.read()

    # START SNIPPET runhandlers
    def run_handlers(self):
        for pass_nr in range(1, self.passes + 1):
            for handler in self.handlers:
                if pass_nr in handler.passes():
                    for file in self.files:
                        for segment in file.segments:
                            handler.handle(pass_nr, segment)

    # END SNIPPET

    def write_files(self):
        for file in self.files:
            if file.modified():
                writer = FileWriter(file)
                writer.write()

    def process(self):
        self.read_files()
        self.run_handlers()
        self.write_files()
