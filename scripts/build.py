assert __debug__ is False # Run with -OO
import hashlib, traceback, shutil, subprocess, sys, os, glob
import requests

if sys.version_info < (3, 7, 3):
    print('Your python compiler is too old. Please upgrade to 3.7.3 or higher.')
    sys.exit()

class UploadAPI(object):

    def __init__(self, endpoint, auth_secret, chunk_size=8*1024*1024):
        self.endpoint = endpoint
        self.auth_secret = auth_secret
        self.chunk_size = chunk_size

    def post(self, *args, **kwargs):
        for i in range(10):
            try:
                req = requests.post(*args, **kwargs)
                
                if req.status_code != 200:
                    raise Exception('Error code {0}: {1}'.format(req.status_code, req.text))

                return req.json()
            except:
                print(traceback.format_exc())
                print('Trying again...')

        raise Exception('Failed to post data.')

    def upload_file(self, filename, target_filename=None):
        if target_filename is None:
            target_filename = os.path.basename(filename)

        md5 = hashlib.md5()
        start = 0
        end = -1
        length = os.path.getsize(filename)
        end_index = length - 1
        data = {'auth': self.auth_secret}

        with open(filename, 'rb') as f:
            for chunk in iter(lambda: f.read(self.chunk_size), b''):
                md5.update(chunk)

                chunk_size = len(chunk)
                end += chunk_size

                headers = {'Content-Range': 'bytes {0}-{1}/{2}'.format(start, end, length)}
                start += chunk_size

                if end == end_index:
                    data['md5'] = md5.hexdigest()

                resp = self.post(self.endpoint, data=data, headers=headers, files={'file': (target_filename, chunk)})

                if 'url' in resp:
                    return resp['url']

                data['upload_id'] = resp['upload_id']

def sign(*filenames):
    print('Signing {0}...'.format(' '.join(filenames)))

    if sys.platform == 'win32':
        subprocess.call(['signtool', 'sign', '/sm', '/tr', os.environ['SIGN_WIN_TIMESTAMP'], '/td', 'sha256', '/fd', 'sha256', '/n', os.environ['SIGN_WIN_SUBJECT']] + list(filenames))
    elif sys.platform == 'darwin':
        subprocess.call(['codesign', '--deep', '--force', '--verbose', '--sign', os.environ['SIGN_MAC_SUBJECT'], '--timestamp', '--options', 'runtime', '--entitlements', 'entitlements.plist'] + list(filenames))

def cleanup():
    if os.path.exists('build'):
        shutil.rmtree('build')
    if os.path.exists('dist'):
        shutil.rmtree('dist')

def main():
    cleanup()

    build_cmd = ['pyinstaller', '--icon=icon.ico', '--onefile', 'tritonauth.spec']
    result = subprocess.Popen(build_cmd, shell=True)
    result.wait()

    api_endpoint = os.environ.get('DEPLOY_ENDPOINT')
    api_key = os.environ.get('DEPLOY_LOGIN')

    if not api_endpoint or not api_key:
        return

    if sys.platform == 'win32':
        sign(*glob.glob(os.path.join('dist', '*.exe')))
        makensis = os.path.join(os.environ['PROGRAMFILES(X86)'], 'NSIS', 'Bin', 'makensis.exe')

        if not os.path.exists(makensis):
            raise Exception(f'{makensis} does not exist!')

        installer_cmd = [makensis, 'installer.nsi']

        subprocess.call(installer_cmd)
        upload = 'tritonauth_setup.exe'

        sign(upload)

    api = UploadAPI(api_endpoint, api_key)
    print(api.upload_file(upload, upload))

    os.remove(upload)
    cleanup()

if __name__ == '__main__':
    main()