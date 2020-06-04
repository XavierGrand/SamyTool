# Samy
Version : 1.1
7th January, 2020.

## Author:
Xavier Grand, 
Master SNS parcours BCD 2019-2020, 
Faculté des Sciences, Université de Montpellier.

## Purpose:
Samy is a python program to parse and filter sam file. Able to handle Single and Paired ends data. Return Statistics about reads quantity, as mapped reads, unmapped reads, partially mapped reads, pairs of reads, with one mapped and not the other, or with one mapped and the other partially mapped.

# Tech

  - Developped under python 3.6.8
  - It's an EDUCATION project, you should better to use Samtools or others professionnal tools.

## Installation

Samy is available on request to Xavier Grand: xavier.grand@etu.umontpellier.fr.

# Usage

```console
usage: Samy.py [-h] [-a] [-p] [-i] [-sA] [-sMNM] [-sMPM] file

positional arguments:
  file                  Input SAM file to parse.

optional arguments:
  -h, --help            show this help message and exit
  -a, --all             Compute and display all statistics.
  -p, --pairs           Compute and display pairs statistics.
  -i, --info            Display header information.
  -sA, --saveAll        Save all filtered pairs (MapNotMap & MapPartMap) in
                        new sam files.
  -sMNM, --saveMapNotMap
                        Save filtered MapNotMap pairs in a new sam file.
  -sMPM, --saveMapPartMap
                        Save filtered MapPartMap pairs in a new sam file.

```

### Todos

 - Lot's of debugs
 - Lot's of optimizations
 - Filters option (MappedMapped, NotMappedNotMapped, etc.)

# License

**Free Software, open source.**