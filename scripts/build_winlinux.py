assert __debug__ is False # Run with -OO
import subprocess, sys, os

if not sys.platform.startswith('win') and not sys.platform.startswith('linux'):
    print('You\'re not on a Windows or a Linux PC! Please use the correct script instead.')
    sys.exit()

if sys.version_info < (3, 7, 3):
    print('Your python compiler is too old. Please upgrade to 3.7.3 or higher.')
    sys.exit()

if sys.platform.startswith('win'):
    pyinstaller = os.path.join(sys.exec_prefix, 'scripts', 'pyinstaller')
else:
    pyinstaller = 'pyinstaller'

build_cmd = [pyinstaller, '--icon=icon.ico', '--onefile', 'tritonauth.spec']

print(subprocess.Popen(build_cmd, shell=True, stdout=subprocess.PIPE).stdout.read())
print('If all went well, check in the dist folder for the exe.')