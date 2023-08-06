# LocusHandler

This package was created to automate Locus coded data processing steps. It provides functions to parse and validate
Locus codes. It also allows to process entire data files that use the Locus classification system or other common economic
classification systems such as NAICS or SOC.

[![PyPI version](https://badge.fury.io/py/locushandler.svg)](https://badge.fury.io/py/locushandler)
[![Build Status](https://semaphoreci.com/api/v1/projects/f153f328-ef80-4f95-b85a-408e1a8d13ba/2377361/badge.svg)](https://semaphoreci.com/locusanalytics/locushandler)

## Getting Started

### Installation

The package can be downloaded and installed using pip.

```
pip install locushandler
```

You will then be able to import the package in your Python scripts.

```
import locushandler as lh
```

You can also import specific parts of the package.

```
import locushandler.string_parser as sp
import locushandler.file_handler as fh
```

### Prerequisites

The LocusHandler is coded in Python 3.
Using pip install, all Python libraries required to use the LocusHandler should be automatically installed on your machine.

## How to use the LocusHandler

#### Granularity

The granularity parameters takes in a string with the format \<a>x\<r> with \<a>
in \[1,4,12,36\] and \<r> in \[1,6,6x4,6x4x3\]

##### Activity

- '1' : no activity
- '4' : 4 phases activty cycle
- '12' : 12 phases activity cycle
- '36' : 36 phases activity cycle

##### Resource

- '1' : no resource
- '6' : resource categories
- '6x4' : resource categories staged
- '6x4x3' : resource categories sub-staged

##### Examples

- Work Locus : - 4x6 : 1 B, 3 F - 12x6x4 : (B4) 1.2 B4, 2.2 C3 - 36x6x4x3 : 3.3.1 E3ii, (B4ii) 3.1.2 Div
- Resource Locus : - 1x6 : B, F - 12x6x4 : B4 2.2 B4, A4 1.3 C3 - 36x6x4x3 : B4ii 1.2.2 E3ii, B4ii 2.2.2 Div

##### Input syntax

- The LocusHandler assumes that all work loci contain parentheses around the Distinguishing Resources and the Information Outputs.
  Please make sure that the input data follows that syntax.

#### Parsing a Locus code

The string_parser module allows you to parse any work or resource Loci, in a string format, such as

```
'(B4ii) 1.2.2 B4i'
'B4ii 2.2.2 F'
```

and get a list, a dictionary or a string of that code at the required granularity.

##### Parsing to a dictionary

```
sp.string_parser('(B4ii) 1.2.2 B4Div', 'dict', '36x6x4x3', show_dr=True, show_io=True))
```

will return the following dictionary

```
{'dr': {'r1': 'B', 'r2': '4', 'r3': 'ii'},
 'act': {'a1': '1', 'a2': '2', 'a3': '2'},
 'obj': {'r1': 'B',  'r2': '4', 'r3': 'V'},
 'io':  {'r1': '',  'r2': '', 'r3': ''}
 }
```

make use of the `merge_fields` parameter to return (field, field value) pairs:

```
sp.string_parser('(B4ii) 1.2.2 B4Div', 'dict', '36x6x4x3', show_dr=True, show_io=True))
```

will return the following dictionary

```
{'dr': 'B4ii',
 'act': '1.2.2',
 'obj': 'B4V',
 'io': ''
}
```

##### Parsing to a list

```
sp.string_parser('(B4ii) 1.2.2 B4Div', 'list', '4x6', show_dr=True, show_io=True))
```

will return the following list

```
['B','2','B','']
```

##### Parsing to a string

```
sp.string_parser('(B4ii) 1.2.2 B4Div', 'string', '12x6x4', show_dr=False, show_io=False))
```

will return the following string

```
'1.2 B4'
```

#### Parsing a Locus code column in a file

The file_handler module allows you to parse an entire column of a .csv file. If the input file contains Locus code as strings
the function parse_file can parse it and return a Dataframe or a name of a new saved .csv file with columns containing
each element the Locus code at the required granularity.
An example of input data would be the following table.

|  Enterprise_Locus  | Employment level | ... | Area | Year |
| :----------------: | :--------------: | :-: | :--: | :--: |
| '(B4ii) 1.2.2 B4i' |       1366       | ... |  NY  | 2010 |
| (A4iii) 3.3.2 B3ii |       235        | ... |  VA  | 2008 |
|        ...         |       ...        | ... | ...  | ...  |
|  '(B4ii) 1.3.2 F'  |        78        | ... |  KS  | 2010 |

##### Parsing to a Pandas dataframe

```
fh.parse_file('file.csv', 'Enterprise_Locus', 'df', '12x6x4x3', show_dr=False, show_io=False)
```

would return a Pandas dataframe with the following information

| a1  | a2  | r1  | r2  | r3  | Employment level | ... | Area | Year |
| :-: | --- | --- | --- | --- | :--------------: | :-: | :--: | :--: |
|  1  | 2   | B   | 4   | i   |       1366       | ... |  NY  | 2010 |
|  3  | 3   | B   | 3   | ii  |       235        | ... |  VA  | 2008 |
| ... | ... | ... | ... | ... |       ...        | ... | ...  | ...  |
|  1  | 3   | F   |     |     |        78        | ... |  KS  | 2010 |

##### Parsing to a new .csv file

```
fh.parse_file('file.csv', 'Enterprise_Locus', 'path', '12x6x4x3', show_dr=False, show_io=False)
```

would return the path of the new .csv file that contain the same information as above. In this case, the path would be
'file_parsed_12x6x4x3_Enterprise_Locus.csv'

#### Mapping to Locus codes

If the input data uses a common classification system, the LocusHandler provide a function to map the input data
to Locus code at the desired granularity.
An example of input data would be the following table.

| Naics | Employment level | ... |  Area   | Year |
| :---: | :--------------: | :-: | :-----: | :--: |
| 13589 |     3468735      | ... |   USA   | 2010 |
| 78621 |      87685       | ... | FRANCE  | 2008 |
|  ...  |       ...        | ... |   ...   | ...  |
| 34697 |      34786       | ... | NIGERIA | 2010 |

To call the map_to_locus you need the path of your input file (file_naics.csv), the name of the column with the classification system you map from (Naics)
, the name of the column of the classification sytem in the crosswalk file (NAICS5), the path to the crosswalk file (naics2locus.csv),
the barcode field you are interested in (enterprise_locus), the granularity (4x6) and the need for dr and io.

```
fh.map_to_locus('file_naics.csv', 'Naics', 'NAICS5', 'naics2locus.csv', 'entreprise_locus','4x6', show_dr=True, show_io=True)
```

would return a Pandas dataframe with the following information\*.

| dr1 | a1  | r1  | io1 | Employment level | ... |  Area   | Year |
| :-: | --- | --- | --- | :--------------: | :-: | :-----: | :--: |
|  B  | 1   | B   |     |     3468735      | ... |   USA   | 2010 |
|     | 2   | A   | C   |      87685       | ... | FRANCE  | 2008 |
| ... | ... | ... | ... |       ...        | ... |   ...   | ...  |
|  A  | 3   | B   |     |      34786       | ... | NIGERIA | 2010 |

<sub>\*Naics to Locus mapping not accurate here</sub>

## Documentation

- Please read the [Technical Brief](https://docs.google.com/document/d/1g6RVpLE9jD7m-sXWsKmVoSy5to0a9FnqfS2JWlOnsTk/edit) for details on the project.
- Please read the [Specs](https://docs.google.com/document/d/15FfZJx9haLjSG1PLc4e9lLvEul713Eela-s5Uq7Wp1A/edit?usp=sharing) for details on the functions available.

## Authors

- **[Phillip Nguyen](mailto:pnguyen@locus.co)** - _String parsing_
- **[Olivia Dalglish](mailto:odalglish@locus.co)** - _Code validation_
- **[Emeline Floc'h](mailto:efloch@locus.co)** - _File handling_

## Contributors

- **Vinharng Chew** - **Stefanie Bourland** - **Chris Haack** - **Aaron Lee** - **Atul Prasad** - _Reviewers_
