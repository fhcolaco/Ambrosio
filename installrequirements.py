import warnings
with warnings.catch_warnings():
    warnings.filterwarnings("ignore",category=DeprecationWarning)
import pkg_resources
import subprocess
import sys

def is_installed(package):
    try:
        pkg_resources.get_distribution(package)
        return True
    except pkg_resources.DistributionNotFound:
        return False

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", package])

def install_requirements():
    with open('adittional_files/requirements.txt', 'r') as f:
        for line in f:
            package = line.strip()
            if not is_installed(package):
                install(package)