import logging
import os

logger = logging.getLogger(__name__)


class FileWriter:
    def __init__(self, file, backup=False):
        self.file = file
        self.backup = backup

    def write(self):
        with open(self.file.name, "r") as f:
            text = f.read()

        new_text = ""
        for segment in self.file.segments:
            new_text += "".join(segment.text)

        if text == new_text:
            logger.info("content not changed %s" % self.file.name)
            return

        if self.backup:
            os.rename(self.file.name, self.file.name + ".BAK")
            logger.info("BAK file created for %s" % self.file.name)

        logger.info("writing the file %s" % self.file.name)
        with open(self.file.name, "w") as f:
            f.write(new_text)
