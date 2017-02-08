# Edges

A basic edge detection implementation in __Python3__.

## Install
If you do not want do install, you can run with:
`$ python3 edges/cli.py [...]`

### With pip
 * Run `sudo pip3 install -e .[test]` to install a local, 'in place' copy.
 * Run `sudo pip3 uninstall edges` to uninstall.

### With setup.py
* Run `python3 setup.py develop` to install a local, 'in place' copy.
* Run `python3 setup.py develop --uninstall` to uninstall this copy.

* Run `python3 setup.py install` to install a local immutable copy.  

## Dependencies
Needs PIL / Pillow install on the system to work with images. 

## Running

The cli is available with a few options.

```bash
$ edges --help # Prints options
$ edges -i [INPUT FILE] -o [OUTPUT DEST] [OPTIONS]
```

### Options

* `-t [NUMBER]` : Specify a threshold for the gradient filtering
* `-gs [NUMBER]` : Specify the sigma to be used for the Gaussian filter
* `-og ` : Only apply Gaussian filtering
* `-ogm ` : Only apply Gradient magnitude filtering
