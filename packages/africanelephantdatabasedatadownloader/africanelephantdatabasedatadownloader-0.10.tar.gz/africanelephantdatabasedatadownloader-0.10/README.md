# Download data from the African Elephant Database

The African Elephant Database ([http://africanelephantdatabase.org/](http://africanelephantdatabase.org/)) is an online effort by the [IUCN SSC African Elephant Specialist Group (AfESG)](http://www.iucn.org/african_elephant) to gather data from different surveys and combine it with past African Elephant Status Reports (published by the same group).

The database is freely accessible online via a web user interface, and released under a [Creative Commons Attribution-NonCommercial-ShareAlike license](http://creativecommons.org/licenses/by-nc-sa/4.0). Unfortunately, at the time of this writing, the AfESG did not have means to access the backend and retrieve raw data.

This script swifts through the online user interface and downloads all data contained in the  “Elephant Estimates” columns as well as the spatial geometry of each *stratum* (the smallest area reported). It retains the hierarchy of spatial units by referencing to the higher-order units in attributes in order to allow the reconstruction of data on the level of *input systems*, *countries*, *regions* and the entire *continent*.

If you use *python-africanelephantdatadownloader* for scientific research, please cite it in your publication: <br>
Fink, C. (2019): *python-africanelephantdatabasedatadownloader: a Python utility to download the most up-to-date data from the African Elephant Database*. [doi:10.5281/zenodo.3243872](https://doi.org/10.5281/zenodo.3243872)

### Dependencies

The script is written in Python 3 and depends on the Python modules [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/bs4/), [GeoPandas](https://geopandas.org/), [Shapely](https://github.com/Toblerity/Shapely) and [requests](https://2.python-requests.org/).

To install all dependencies on a Debian-based system, run:

```shell
apt-get update -y &&
apt-get install -y python3-dev python3-pip python3-virtualenv \
    python3-bs4 python3-geopandas python3-requests python3-shapely
```

(There’s an Archlinux AUR package pulling in all dependencies, see further down)


### Installation

- *using `pip` or similar:*

```shell
pip3 install -u africanelephantdatabasedatadownloader
```

- *OR: manually:*

    - Clone this repository

    ```shell
    git clone https://gitlab.com/helics-lab/python-africanelephantdatabasedatadownloader.git
    ```

    - Change to the cloned directory    
    - Use the Python `setuptools` to install the package:

    ```shell
    cd python-africanelephantdatabasedatadownloader
    python3 ./setup.py install
    ```

- *OR: (Arch Linux only) from [AUR](https://aur.archlinux.org/packages/python-africanelephantdatabasedatadownloader):*

```shell
# e.g. using yaourt
yaourt python-africanelephantdatabasedatadownloader
```


### Usage

Run `aed-downloader [outputFile]`. It will download all data (be patient) and save it in [GeoPackage](http://www.geopackage.org/spec/) format to `outputFile` (default is `output.gpkg` in the current working directory).
