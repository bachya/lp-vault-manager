import csv
import random
import string
import StringIO
import subprocess


class LastPassVaultManager:
    ####################################################################
    # Paths
    ####################################################################
    DEFAULT_LPASS_PATH = '/usr/local/bin/lpass'

    ####################################################################
    # lpass Commands
    ####################################################################
    LPASS_COMMAND_LOGIN = 'login'
    LPASS_COMMAND_DOWNLOAD = 'export'
    LPASS_COMMAND_DETAILS = 'show'

    ####################################################################
    # Password Components
    ####################################################################
    DEFAULT_PASSWORD_NUMBER = 10
    DEFAULT_PASSWORD_LENGTH = 20
    CHARS_SYMBOLS = '^!\$%&/()=?{[]}+~#-_.:,;<>|\\'
    CHARS_AMBIGUOUS = '0OIl1'

    ####################################################################
    # Miscellaneous
    ####################################################################
    DEFAULT_CACHE_TIMEOUT = 300

    def __init__(self):
        pass

    def download_data(self):
        fields = ['url', 'hostname']
        try:
            data = subprocess.check_output(
                [self.DEFAULT_LPASS_PATH, self.LPASS_COMMAND_DOWNLOAD]
            )
            r = csv.DictReader(StringIO.StringIO(data))
            return [{k: v for k, v in d.iteritems() if k in fields} for d in r]
        except subprocess.CalledProcessError:
            return []

    def generate_passwords(self, number=10, length=20, upper=True, lower=True,
                           digits=True, symbols=True, avoid_ambiguous=True):
        charsets = []

        # Uppercase ASCII letters:
        if upper:
            charsets.append(string.ascii_uppercase)

        # Lowercase ASCII letters:
        if lower:
            charsets.append(string.ascii_lowercase)

        # Digits:
        if digits:
            charsets.append(string.digits)

        # Symbols
        if symbols:
            charsets.append(self.CHARS_SYMBOLS)

        # Combine all the charsets into one string and remove
        # ambigious chars if requested:
        chars = ''.join(charsets)
        if avoid_ambiguous:
            chars = chars.translate(None, self.CHARS_AMBIGUOUS)

        passwords = []
        for i in xrange(0, number):
            pw = ''.join(random.SystemRandom().choice(chars)
                         for _ in xrange(length))
            passwords.append(pw)

        return passwords

    def get_field_value(self, hostname, field_name):
        details = self.get_item_details(hostname)
        value = [i for i in details.split('\n') if field_name in i][0]
        return value[value.index(': ') + len(': '):]

    def get_item_details(self, hostname):
        return subprocess.check_output(
            [self.DEFAULT_LPASS_PATH, self.LPASS_COMMAND_DETAILS, hostname]
        )
