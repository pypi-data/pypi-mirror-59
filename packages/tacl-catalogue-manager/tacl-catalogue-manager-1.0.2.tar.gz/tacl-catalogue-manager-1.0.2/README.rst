Manager for TACL catalogue files
================================

This package provides a library and script to merge multiple lists of
TACL works together in a specified order, and output one or more
catalogue files using supplied labels.

The merging process applies the name of the first file to list a work
to that work; all subsequent names for that work are ignored. This
allows for different categorisations of works to be put in a priority
order.

The process of creating catalogue files makes use of mappings between
the filenames of the work lists and labels to be used in the
catalogue. Multiple filenames may map onto a single label. The order
of the labels in the mapping is maintained in the catalogue file.


Usage
-----

Run ``tcm -h`` for help on the command and the files used.
