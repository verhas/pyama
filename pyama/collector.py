import glob
import re


class FileCollector:
    def __init__(self, configurations, *patterns):
        """
        Collect the file names parse recursively into subdirectories
        and selecting the files that match any of the patterns
        :param configurations: the configurations
        :param patterns: array of patterns to match the file names
        """
        self.configurations = configurations
        self.patterns = patterns

    def collect(self):
        files = set()
        for pattern in self.patterns:
            for file in glob.glob(pattern, recursive=True):
                for configuration in self.configurations:
                    for regex in configuration.filename_regexes:
                        if re.search(regex, file):
                            files.add(file)

        return files
