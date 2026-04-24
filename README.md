 Spell Right ✨

Spell Right is a simple Python desktop application built using Tkinter. It helps users correct spelling mistakes and quickly find word meanings and synonyms.

 Features

* Spelling correction using TextBlob
* Word meaning using Dictionary API
* Synonyms using Datamuse API
* Dark mode and light mode
* Simple and user-friendly interface

 Requirements

* Python
* Tkinter
* textblob
* requests

Installation

Install the required libraries:

```
pip install textblob requests
```

Download TextBlob data (if needed):

```
python -m textblob.download_corpora
```

How to Run

Run the main file:

```
python main.py
```

How to Use

* Type a word in the search bar
* Press Enter or click the search icon
* A new window will show:

  * Corrected spelling
  * Meaning of the word
  * Synonyms

Note

* Internet connection is required for API results
* Some words may not return results
