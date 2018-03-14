from pyama.reader import Reader
from pyama.filereader import Factory
from pyama.collector import FileCollector
from pyama.filewriter import FileWriter
import re
import argparse
import logging

logger = logging.getLogger(__name__)


def handler_tostring(handler):
    string = "%s" % handler
    match = re.search(r"<.*?(\w+)\s+object\s+at\s+0x0*([\dA-F]*)>",string)
    return match.group(1) + ":" + match.group(2) if match else string


class Processor:
    def __init__(self, configs, path):
        parser = argparse.ArgumentParser()
        parser.add_argument("-l", "--level",
                            help="set the logging level explicitly DEBUG, INFO, WARNING, ERROR or CRITICAL")
        parser.add_argument("-n", "--dry", help="do not write the changes back to the files", action="store_true")
        parser.add_argument("-b", "--backup", help="create .BAK for changed files", action="store_true")
        parser.add_argument("-f", "--logfile", help="create .BAK for changed files")
        args = parser.parse_args()
        if args.level:
            logging.basicConfig(level=args.level)
        else:
            logging.basicConfig(level=logging.WARNING)
        if args.logfile:
            logging.getLogger().addHandler(logging.FileHandler(args.logfile))
        self.backup = args.backup
        self.dry_run = args.dry
        if self.dry_run and self.backup:
            logger.warning("Options --backup makes no sense used with --dry")
        self.reader = Reader(configs, Factory, FileCollector(configs, path))
        self.passes = max([x.max_passes for x in configs])
        self.handlers = set()
        self.configs = configs
        for config in configs:
            for handler in config.handlers:
                self.handlers.add(handler)

    def read_files(self):
        self.files = self.reader.read()

    def file_handler_match(self, file, handler):
        for config in self.configs:
            if handler in config.handlers and any(re.search(regex, file.name) for regex in config.filename_regexes):
                return True
        return False

    # START SNIPPET runhandlers
    def run_handlers(self):
        for pass_nr in range(1, self.passes + 1):
            for handler in self.handlers:
                if pass_nr in handler.passes():
                    for file in self.files:
                        if self.file_handler_match(file, handler):
                            for segment in file.segments:
                                # END SNIPPET
                                logger.info("running %s on [%s]:%s" % (
                                    handler_tostring(handler), segment.filename, segment.name))
                                if logger.isEnabledFor(logging.INFO):
                                    original = "".join(segment.text)
                                # START SNIPPET runhandlers
                                handler.handle(pass_nr, segment)
                                # END SNIPPET
                                if segment.modified:
                                    if logger.isEnabledFor(logging.INFO):
                                        new_text = "".join(segment.text)
                                        if new_text == original:
                                            logger.info(
                                                "segment [%s]:%s is intact" % (segment.filename, segment.name))
                                        else:
                                            logger.info(
                                                "segment [%s]:%s is modified" % (segment.filename, segment.name))

    def write_files(self):
        for file in self.files:
            if file.modified():
                writer = FileWriter(file, backup=self.backup)
                writer.write()

    def process(self):
        logger.info("pyama START")
        logger.info("READING FILES")
        self.read_files()
        logger.info("EXECUTING HANDLERS")
        self.run_handlers()
        if self.dry_run:
            logger.info("DRY RUN")
        else:
            logger.info("WRITING FILES")
            self.write_files()
        logger.info("pyama FINISHED")
