"""
To safely download ARGO profile files from NOAA with retries and error handling.
"""

import os
import time

import fsspec
from aiohttp.client_exceptions import ClientResponseError
from fsspec.implementations.http import HTTPFileSystem

BASE_URL = "https://www.ncei.noaa.gov/data/oceans/argo/gadr/data"
BASINS = ["pacific", "atlantic", "indian"]
LOCAL_ROOT = "./data"
MAX_RETRIES = 5
RETRY_DELAY = 5
FS: HTTPFileSystem = fsspec.filesystem("https")


def safe_download(remote_path: str, local_path: str) -> None:
    """
    Downloads an ARGO profile file with time buffers and retries in case of failure.
    """

    retries = 0

    while retries < MAX_RETRIES:

        try:

            FS.get(rpath=remote_path, lpath=local_path)
            return

        except (OSError, IOError, ClientResponseError) as e:  # Transient errors worth retrying.

            retries += 1
            print(f"Error downloading {remote_path}: {e}")

            if os.path.exists(path=local_path):

                os.remove(path=local_path)

            print(f"Retrying ({retries}/{MAX_RETRIES}) after {RETRY_DELAY}s...")
            time.sleep(RETRY_DELAY)

    print(f"Failed to download {remote_path} after {MAX_RETRIES} retries.")
