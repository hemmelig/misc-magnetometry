# Miscellaneous magnetometry scripts

## How to use these scripts
1. Clone this repository and navigate to it, e.g.:

```
git clone https://github.com/hemmelig/misc-magnetometry
cd misc-magnetometry
```

2. Create a virtual environment and install the required dependencies. I use conda to create environments:

```
conda create --name magnetometry python=3.9
conda install obspy
conda install numpy
conda install matplotlib
conda install requests
```

3. Each script can be run with the command-line argument `-h` to see an overview of the required and optional arguments. For example, navigate into the `data_access` dir and run:

```
python download_from_iris.py -h
```

To download, for example, one day of data from the magnetometer at Okmok (OKBR) and save it in the current working directory, one would use the following:

```
python download_from_iris.py --archive_path . --network AV --station OKBR --starttime 2023-03-12 --endtime 2023-03-13
```

I have used the ObsPy package, since I am most familiar with this for reading/writing/manipulating time-series data.

The script for downloading data from the Edinburgh GIN is only tested for downloading 1-minute data from the global magnetometer network site at Shumagin. Mileage may vary.