
# TBDBpy
Python API to TalkBankDB

The TBDBpy package provides access to TalkBankDB data
from Python.

TalkBankDB (www.talkbank.org/DB) is a database and set of tools for
exploring TalkBank’s media and transcripts, specify data to be
extracted, and pass these data on to statistical programs for further
analysis. The TBDBpy package (TalkBankDataBase - Python) provides easy access
to all information within TalkBankDB, including clinical collections.
Clinical Banks are password protected. Visit www.talkbank.org to learn
about gaining access to these collections.

## Installation

You can install TBDBpy from GitHub using pip:
``` python
pip install git+https://github.com/TalkBank/TBDBpy.git
```
Then import tbdb:
``` python
import tbdb
```


## Functionality

TBDBpy allows access to data from TalkBankDB through several functions.
For example, to get a table of utterances from a particular transcript
in the childes/Eng-NA/MacWhinney collection:

``` python
import tbdb
utts = tbdb.getTranscripts( {"corpusName": "childes", "corpora": [['childes', 'Eng-NA', 'MacWhinney', '010411a']]} )
utts
{
'colHeadings': ['path', 'filename', 'languages', 'media', 'date', 'pid', 'designType', 'activityType', 'groupType'], 
'data': [['childes/Eng-NA/MacWhinney/010411a', '010411a', 'eng', 'audio', '1979-05-06', '11312/c-00016447-1', 'long', 'toyplay', 'TD']]}
```

The available functions for accessing different data sets are below. Each function has documentation
accessible through help(functionName), for example:

``` python
import tbdb

# View docs for tbdb module:
help(tbdb)

# View docs for getTranscripts:
help(tbdb.getTranscripts)
```

Functions to extract data from TalkBankDB are:
``` python
tbdb.getTranscripts()
tbdb.getParticipants()
tbdb.getTokens()
tbdb.getTokenTypes()
tbdb.getUtterances()
tbdb.getNgrams()
tbdb.getCQL()
```

Each of these functions take a dictionary parameter defining a corpusName and 
a set of optional fields to define a TalkBankDB request.  Each returns a dictionary with 
two members: 
``` python
{'colHeadings': [], 'data': [[]]}
```
* colHeadings: List of strings describing columns in data.
* data: List of lists, where each list represents a table row.

Additional functions return metadata about TalkBankDB:
```python
tbdb.getPathTrees()
tbdb.validPath()
```

For troubleshooting, an additional function, validPath(), will return
whether a given path is valid.

``` python
tbdb.validPath(['childes', 'childes', 'Clinical']);

```

If the path is not valid, it will return which level of the query is
incorrect

``` python
tbdb.validPath(['childes', 'childes', 'somethingThatDoesNotExist'])

```

To access clinical collections, use the argument *'auth': True*. A dialog
will ask you to enter the clinical bank you are trying to access and to
enter the correct username and password for that database.  If credentials
are incorrect, a response describing the error is returned.

``` python
aphasia_transcrips = tbdb.getTranscripts(
{'corpusName': 'aphasia', 
 'corpora': [['aphasia', 'English', 'Aphasia', 'Adler']], 
 'auth': True})
```
