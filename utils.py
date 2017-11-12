import os
import requests
from xid import Xid


TOP_DIR = os.path.dirname(os.path.abspath(__file__))
DOWNLOADS_DIR = os.path.join(TOP_DIR, 'downloads')
FINANCE_SHEET_DIR = os.path.join(DOWNLOADS_DIR, 'finance')


def create_path(path):
    if not os.path.exists(path):
        os.makedirs(path)


def get_uuid():
    return Xid().string()


def download_file(url, filename=None):
    if filename is None:
        filename = get_uuid()

    uuid = get_uuid()
    print("downloading from {} to file {} ... -> uuid {}".format(url, filename, uuid))

    data = requests.get(url, stream=True)

    if data is not None and data.ok:
        with open(filename, "wb") as handle:
            handle.write(data.content)

        print("downloaded succeed! -> uuid {}".format(uuid))
    else:
        print("[ERROR]: download failed! -> uuid {}".format(uuid))
