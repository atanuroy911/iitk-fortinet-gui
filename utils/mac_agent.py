import os.path
import shutil

basedir = os.path.dirname(__file__)
plist_source = os.path.join(basedir, 'utils/com.iitk.fortinet.auth.plist')
plist_dest = '~/Library/LaunchAgents/com.iitk.fortinet.auth.plist'


def install_agent(val):
    try:
        if val:
            shutil.copy(plist_source, plist_dest)
        else:
            os.remove(plist_dest)
    except Exception as e:
        print(f'Error: {e}')
        pass
