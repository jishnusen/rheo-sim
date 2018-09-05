# Shear Modulus Spectra Calculator

Implements [this paper](https://arxiv.org/abs/1711.09669)

## Setup
Download and extract [https://github.com/jishnusen/rheo-sim/zipball/master](https://github.com/jishnusen/rheo-sim/zipball/master)

### Windows
It is recommended to use the Anaconda distribution of python for windows, as it
installs many modules by default. Go to [https://www.anaconda.com/download/](https://www.anaconda.com/download) to download anaconda.

Once anaconda is installed, open the program Anaconda Prompt, and type:
```
conda install -c conda-forge lmfit 
```

### Linux/MacOS
Most major distributions of Linux come preinstalled with python3.

On Mac, install with
```
brew install python
```
If the above command does not work, install Homebrew with
```
ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

Open your terminal emulator (Usually Terminal.app on Mac), and type
```
python3 -m pip install -r requirements.txt
```
If on Linux, ensure you have TKinter installed (this can be done with `sudo apt install python3-tk` on ubuntu)

## Usage
Run the script with
```
python3 rheo.py
```
You can make the script save its results to a csv outfile by specifying the file
name as an argument:
```
python3 rheo.py outfile.csv
```
The program will open a file chooser window when it is run. Here, choose a CSV
with all the experimental data. It expects the CSV to have columns: AF, SM, and
LM, for Angular Frequency (rad/s), Storage Modulus (Pa), and Loss Modulus (Pa), respectively.
