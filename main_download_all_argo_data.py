"""
Downloads every available ARGO profile files from the NOAA website if possible.
"""

import os

from argo import BASE_URL, BASINS, FS, LOCAL_ROOT, safe_download

YEARS_TO_DOWNLOAD = range(2000, 2021)


if __name__ == "__main__":

    for basin in BASINS:

        remote_root = f"{BASE_URL}/{basin}"
        print(f"\nScanning {remote_root}")

        try:

            all_files: list[str] = FS.find(path=remote_root)

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
