# pyaXeHelper

Installation
    
    pip install pyaxehelper
    
This package contains functions helping pyaXe. This works with:

    - pyaxe version '0.1.dev29+gf57de55.d20200106'

    - sextractor version 2.19.5 (2014-11-16)

Functions include:

    - change_catalog_order() edits and removes column order in a sextractor catalog. This is required by pyaxe as discussed in [#5](https://github.com/spacetelescope/pyaxe/issues/5) and [#6](https://github.com/spacetelescope/pyaxe/issues/6).
    
    - change_magiso2magwavelength() edits a column in a sextractor catalog from MAG_ISO to MAG_F[WAVELENGTH] (e.g., MAG_F1392 for F140W images). This is required by pyaxe as discussed in [#5](https://github.com/spacetelescope/pyaxe/issues/5) and [#6](https://github.com/spacetelescope/pyaxe/issues/6).
    
    - write_catalog() saves a text file similar to a sextractor catalog given a pandas dataframe.
    
    - read_catalog() returns pandas dataframe of information in a sextractor catalog.
    
    - select_source() returns an object from a sextractor catalog which is the closest to a given RADEC.
    
    - make_meta() takes a list of files (both grism and direct) and reads their headers. Necessary information (e.g., filepath, filter, and expstart) are extracted and recorded in a dictionary form. This also calls _make_pairs() to make a suggestion for grism-direct pairs by selecting the grism-direct images having the closest expstart.
    
    - _make_pairs() is internally used by make_meta() to return a suggestion of grism-direct pairs.
    
    - prepare_folders() helps preparing folders GRISM/ and DIRECT/. It takes the dictionary output from make_meta() with the grism-direct pair suggestion (i.e., only GID is the input for this function), and processes grism and direct files stated in the dictionary. Each file is copied to the corresponding location. GRISM.lis and DIRECT.lis are constructed at the end.
    
    - make_axelis() constructs an aXe.lis file. It takes GID (i.e., an output from make_meta) and utilizes grism-direct pair info.
    
    - calculate_median() calculates median fluxes with sigma clipping using common wavelength grids (i.e., [WMIN,WMAX] with DW bin width. It reads lambdas and fluxes from pyaxe outputs (i.e., OUTPUT/*2.SPC.fits or OUTPUT/*2_opt.SPC.fits) given an object ID and the file list (i.e., FILES). Interp1d model is constructed, and is used to interpolate fluxes to the common grids. It returns WGRID and dataframe containing the common wavelength grids and dataframe of fluxes (columns: image number and median at the last column, row: parallel to the common wavelength grids), respectively.
        
Known issues:
    
    - ?

v.1.2.0

    - Implement: calculate_median

v.1.1.0

    - This version mainly implement helpers to reduce the amount of manual works required such as making grism-direct pairs, copying files to folders, and making .lis files.

    - Implement: make_meta, _make_pairs, prepare_folders, make_axelis
    
v.1.0.0

    - This version mainly implements helpers to construct a sextractor catalog to be complied with pyaxe requirements.
    
    - Implement: change_catalog_order, change_magiso2magwavelength, write_catalog, read_catalog, select_source
    
