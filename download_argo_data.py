"""
Downloads every available ARGO profile files from the NOAA website if possible.
"""

import os
import time

import fsspec
from fsspec.implementations.http import HTTPFileSystem

BASE_URL = "https://www.ncei.noaa.gov/data/oceans/argo/gadr/data"
BASINS = ["pacific", "atlantic", "indian"]
LOCAL_ROOT = "./data"
YEARS_TO_DOWNLOAD = range(2000, 2021)
MAX_RETRIES = 5
RETRY_DELAY = 5

fs: HTTPFileSystem = fsspec.filesystem("https")


def safe_download(remote_path: str, local_path: str) -> None:
    """
    Downloads an ARGO profile file with time buffers and retries in case of failure.
    """

    retries = 0

    while retries < MAX_RETRIES:

        try:

            fs.get(rpath=remote_path, lpath=local_path)
            return

        except (OSError, IOError) as e:

            retries += 1
            print(f"Error downloading {remote_path}: {e}")

            if os.path.exists(path=local_path):

                os.remove(path=local_path)

            print(f"Retrying ({retries}/{MAX_RETRIES}) after {RETRY_DELAY}s...")
            time.sleep(seconds=RETRY_DELAY)

    print(f"Failed to download {remote_path} after {MAX_RETRIES} retries.")


if __name__ == "__main__":

    for basin in BASINS:

        remote_root = f"{BASE_URL}/{basin}"
        print(f"\nScanning {remote_root}")

        try:

            all_files: list[str] = fs.find(path=remote_root)

        except OSError as e:

            print(f"Could not list {remote_root}: {e}")
            continue

        for path in all_files:

            if not path.endswith(".nc"):

                continue

            parts = path.split(sep="/")

            try:

                year = int(parts[-3])

            except (ValueError, IndexError) as e:

                continue

            if year not in YEARS_TO_DOWNLOAD:

                continue

            relative_path = path.replace(BASE_URL + "/", "")
            redefined_local_path = os.path.join(LOCAL_ROOT, relative_path)
            os.makedirs(name=os.path.dirname(p=redefined_local_path), exist_ok=True)

            if os.path.exists(path=redefined_local_path):

                print(f"Already exists: {relative_path}")
                continue

            print(f"Downloading {relative_path} ...")
            safe_download(remote_path=path, local_path=redefined_local_path)
