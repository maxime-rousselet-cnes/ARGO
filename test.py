"""
To test the package. To be called by pytest test.py.
"""

from argo import BASE_URL, BASINS, FS


def test_find_argo_files():
    """
    Verifies the NOAA arborescence is reachable.
    """

    remote_root = f"{BASE_URL}/{BASINS[0]}"

    try:

        FS.find(path=remote_root + "/2000/01")

    except OSError:

        assert False
