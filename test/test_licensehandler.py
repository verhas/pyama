from pyama.licensehandler import LicenseHandler
from pyama.configuration import Configuration

license_handler = LicenseHandler()
license_handler.license("LICENSE.txt")
JAVA = Configuration() \
    .file(".*\\.java") \
    .handler(JavaHandler(), license_handler)

configs = [JAVA]
processor = Processor(configs, "../test/*.java")
processor.process()