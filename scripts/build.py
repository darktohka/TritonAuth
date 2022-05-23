assert __debug__ is False # Run with -OO
import subprocess, sys, os

if sys.version_info < (3, 10, 4):
    print('Your Python compiler is too old. Please upgrade to 3.10.4 or higher.')
    sys.exit()

def sign(*filenames):
    print('Signing {0}...'.format(' '.join(filenames)))

    if sys.platform == 'win32':
        subprocess.call(['signtool', 'sign', '/sm', '/tr', os.environ['SIGN_WIN_TIMESTAMP'], '/td', 'sha256', '/fd', 'sha256', '/n', os.environ['SIGN_WIN_SUBJECT']] + list(filenames))
    elif sys.platform == 'darwin':
        subprocess.call(['codesign', '--deep', '--force', '--verbose', '--sign', os.environ['SIGN_MAC_SUBJECT'], '--timestamp', '--options', 'runtime', '--entitlements', 'entitlements.plist'] + list(filenames))

def main():
    build_cmd = [
        sys.executable, '-OO', '-m', 'nuitka', '--standalone', '--onefile', '--python-flag=-OO', '--assume-yes-for-downloads',
        '--static-libpython=auto', '--windows-disable-console', '--windows-icon-from-ico=scripts/icon.ico', '--windows-product-name=TritonAuth',
        '--windows-company-name=Sapientia', '--windows-file-version=1.0.0.0', '--windows-file-description=TritonAuth',
        '--enable-plugin=pyside6', '--enable-plugin=numpy', '-o', 'TritonAuth.exe', 'main.py'
    ]
    result = subprocess.Popen(build_cmd, shell=True, cwd='..')
    result.wait()

    if sys.platform == 'win32':
        sign('../TritonAuth.exe')
        makensis = os.path.join(os.environ['PROGRAMFILES(X86)'], 'NSIS', 'Bin', 'makensis.exe')

        if not os.path.exists(makensis):
            raise Exception(f'{makensis} does not exist!')

        installer_cmd = [makensis, 'installer.nsi']
        subprocess.call(installer_cmd)
        sign('tritonauth_setup.exe')

if __name__ == '__main__':
    main()