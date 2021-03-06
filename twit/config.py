import os
from configparser import ConfigParser, ExtendedInterpolation

env = os.environ.get("ENV", "DEV")
configuration = ConfigParser(interpolation=ExtendedInterpolation())

if not configuration.read(f"config_{env}.ini"):
    raise OSError(f"Can not load configuration file {os.getcwd()}/config_{env}.ini")

if __name__ == "__main__":
    import sys

    args = sys.argv[1:]
    print(configuration.get(*args))
