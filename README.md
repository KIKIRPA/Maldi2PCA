# Maldi2PCA
Maldi2PCA - Prepares Maldi data for PCA: reduce & normalize TAB-delimited data files

  Author:       Wim Fremout / Royal Institute for Cultural Heritage, Brussels, Belgium (16 Oct 2009)
  Licence:      GNU GPL version 3.0
  
## About

This simple script was written to uniformise sets of MALDI-TOF-MS spectra (ascii format) of tryptic digests from proteïnaceaous binding media, and prepare the data for Principal Component Analysis (PCA) and other chemometrics analysis. Firstly, the mass spectrum can limited to a specific range (standard 900–2000Da). Secondly, to correct for different numbers of datapoints in different measurements and unavoidable small intermeasurement mass shifts, the number of datapoints is reduced to a single datapoint per Dalton. In doing so, the influence of misalignation on the PCA results will be minimal, since a misaligned peak will always coincide with the aligned mass of one of its isotopes. Finally, the data are normalised.

For more information, please consult:
W. Fremout, S. Kuckova, M. Crhova, J. Sanyova, S. Saverwyns, R. Hynek, M. Kodicek, P. Vandenabeele and L. Moens, “Classification of Protein Binders in Artist’s Paints by Matrix‐assisted Laser Desorption/ionisation Time‐of‐flight Mass Spectrometry: An Evaluation of Principal Component Analysis (PCA) and Soft Independent Modelling of Class Analogy (SIMCA).” Rapid Communications in Mass Spectrometry 25, no. 11 (June 15, 2011): 1631–1640. doi:10.1002/rcm.5027.

## Prerequisites

Python v2.x

## Usage
```
Usage: maldi2pca.py [options] INFILES

Options:

  --version      show program's version number and exit
  
  -h, --help     show this help message and exit
  --nolimits     do not set X range
  --low=LOW      lower limit (default: 900)
  --high=HIGH    higher limit (default: 2000)
  -n NORM        normalize Y data, no normalization when zero (default: 999)
  -c COL         display columns (default: 15, 13 in case of -n0)   1-Xround
                 2-Xpeak  3-Ypeak  4-Ysum  5-Ypeak*  6-Ysum*  7-iterations
  --headerless   do not display the table header
  --comma        comma as digital separator
  -o OUTFILE     output file
  -v, --verbose  be very verbose
```
