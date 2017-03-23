# Detection
**Austin Cawley-Edwards  
Stevens Institute of Technology  
CS 558: Computer Vision  
Prof. Enrique Dunn**  

A basic feature and edge detection implementation in __Python3__.

## Install
If you do not want do install, you can run with:
`$ python3 detection/cli.py [...]`

### With pip
 * Run `sudo pip3 install -e .[test]` to install a local, 'in place' copy.
 * Run `sudo pip3 uninstall detection` to uninstall.

### With setup.py
* Run `python3 setup.py develop` to install a local, 'in place' copy.
* Run `python3 setup.py develop --uninstall` to uninstall this copy.

* Run `python3 setup.py install` to install a local immutable copy.  

## Dependencies
Needs PIL / Pillow install on the system to work with images. 

## Dev Dependencies
* Doxygen
* Pandoc
* Latex

## Running

The cli is available with a few options.

```bash
$ detection --help # Prints options
$ detection -i [INPUT FILE] -o [OUTPUT DEST] [OPTIONS]
```

### Options

* `-t [NUMBER]` : Specify a threshold for the various suppression
* `-gs [NUMBER]` : Specify the sigma to be used for the Gaussian filter
* `-op [OPERATION]` : Specify the operation to perform
* Many others found in with `-h` flags

## Documentation
Look for a doxygen-generated pdf called [`refman.pdf`](./refman.pdf) for full source documentation.  

Source Code can be found in the `detection` directory.  
