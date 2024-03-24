pyUtau
======

A complete *bodge* of a Python library made by UtaUtaUtau. Interprets data that UTAU sends through plugins. Made to work for UST Version 1.20 only. I am not an avid programmer, please don't expect much...

~~To use, it's just one file. Clone or download this repo, and put pyutau.py somewhere in your project. Import it with none other than `import pyutau`~~

To use, you can now install this as a Python package through pip by using:
```cmd
pip install pyutau
```
You can still get the `pyutau.py` file from the folders but I recommend doing this instead.

All information used to make this plugin is from [this @wiki page](https://w.atwiki.jp/utaou/pages/64.html) and [this C# library.](https://github.com/delta-kimigatame/utauPlugin "Get this if you know C#") I just translated everything through [DeepL](https://deepl.com/en/translator) to understand how these work.

How to use
---
```Python
import pyutau
import sys

plugin = pyutau.UtauPlugin(sys.argv[-1])

# Whatever you wanna do

plugin.write(sys.argv[-1])
```

You may use `pydoc` to get an HTML version of the docstrings within the module.