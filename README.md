pyUtau
======

A complete *bodge* of a Python library made by UtaUtaUtau. Interprets data that UTAU sends through plugins. Made to work for UST Version 1.20 only. I am not an avid programmer, please don't expect much...

To use, it's just one file. Clone or download this repo, and put pyutau.py somewhere in your project. Import it with none other than `import pyutau`

All information used to make this plugin is from [this @wiki page](https://w.atwiki.jp/utaou/pages/64.html) and [this C# library.](https://github.com/delta-kimigatame/utauPlugin "Get this if you know C#") I just translated everything through [DeepL](https://deepl.com/en/translator) to understand how these work.

~~I'll just put the documentation here...~~

How to use
---
```Python
import pyutau
import sys

plugin = pyutau.UtauPlugin(sys.argv[-1])

# Whatever you wanna do

plugin.write(sys.argv[-1])
```

UtauPlugin
-----
UtauPlugin is the main class.

<dl>
  <dt>UtauPlugin(self, fpath)</dt>
  <dd>Reads the UST data sent in by UTAU. The file path is always the second argument or the last argument.</dd>
</dl>

---

### Data descriptors:
<dl>
  <dt>version</dt>
  <dd>Obsolete. Returns UST version. Will be None if not provided.</dd>
  
  <dt>settings</dt>
  <dd>Dictionary of UST settings. These are read-only. Will be empty when not provided.
  Read more about it in the @wiki page.</dd>
  
  <dt>prev_note</dt>
  <dd>Stores the note that precedes the selected notes in the UST. None if there is no PREV note.</dd>
  
  <dt>next_note</dt>
  <dd>Stores the note that succeeds the selected notes in the UST. None if there is no NEXT note.</dd>
  
  <dt>notes</dt>
  <dd>List that stores all notes. This uses the Note class.</dd>
</dl>

---

### Methods:
<dl>
  <dt>__str__(self)</dt>
  <dd>Returns a string representation of the whole UST.</dd>
  
  <dt>write(fpath, withHeader = False)</dt>
  <dd>Writes the UST data to the given file path. Normally doesn't save header info.</dd>
  
  <dt>insert_note(self, idx, note)</dt>
  <dd>Inserts note at the given index. Notes are stored in a list.</dd>
  
  <dt>delete_note(self, idx)</dt>
  <dd>Sets the note at the given index to a DELETE note. Does not remove it from the list</dd>
  
  <dt>get_notes(self)</dt>
  <dd>Returns all notes that are not DELETE notes. I don't think you can modify notes directly without using mutable functions</dd>
</dl>

Note
-----
A class that stores note data.

<dl>
  <dt>Note(self, note_type = 'INSERT')</dt>
  <dd>Makes a default note with the given note type. Note types are PREV, NEXT, INSERT, DELETE and ####.
  The default note is at C4 with lyric あ, and length 480</dd>
  
  <dt>pyutau.create_note(lyric = 'あ', length = 480, note_num = 60, **kwargs)</dt>
  <dd>Makes a new INSERT note. Made for inserting notes specifically. note_num is the key, C4 = 60.
  If the note is not a rest note (lyric "R", "r" or blank), it automatically sets intensity to 100 and mod to 0.
  **kwargs are for extra data. Read the @wiki mentioned above for more info.</dd>
</dl>

---

### Data descriptors:
<dl>
  <dt>note_type</dt>
  <dd>Stores the note type. Does not change to DELETE when delete_note() is used</dd>
  
  <dt>isdeleted</dt>
  <dd>The reason why note_type doesn't change to DELETE with delete_note(). This is made in case someone wants to bring back a deleted note from their data</dd>
  
  <dt>note_data</dt>
  <dd>Where all note data is stored in a dictionary. Blank entries are written as None. Only put string keys and values here.</dd>
</dl>

---

### Methods:
<dl>
  <dt>__str__(self)</dt>
  <dt>get(self)</dt>
  <dd>Returns a string representation of the note in the format of the UST</dd>
  
  <dt>delete_note(self)</dt>
  <dd>Sets a note to a DELETE note without changing the note type.</dd>
  
  <dt>get_note_type(self)</dt>
  <dd>Returns the note type, and also responds to isdeleted. Use this one, don't read note_type directly</dd>
  
  <dt>set_custom_data(self, name, data)</dt>
  <dd>Sets in custom data and saves the string representation of the data under name.</dd>
  
  <dt>get_custom_data(self, name)</dt>
  <dd>Gets the string representation of the custom data under name</dt>
  
  <dt>set_multiple_data(self, **kwargs)</dt>
  <dd>Sets multiple data because note_data is a dictionary. Just.. yeah.</dd>
</dl>

***Setters and Getters***

These are written for data that UTAU can send in and read.
Some of them get initializers because UTAU sends in values for them.
**NOTE:** All floating point data are rounded to 3 decimals when set. Sorry if you still wanted to keep precision.

Legend: **Required**, Not Required, *Read-only*
Data Key | Description | Setter | Getter | Initializer | Value Type
--- | --- | :---: | :---: | :---: | :---: 
**Length** | Note Length.  480 = 1 quarter note. | `set_length(self, length)` | `get_length(self)` | - | `int` 
**Lyric** | Note Lyric. | `set_lyric(self, lyric)` | `get_lyric(self)` | `init_lyric(self)` | `str` 
**NoteNum** | Note key. C4 = 60 | `set_note_num(self, note_num)`| `get_note_num(self)` | - | `int` 
**PreUtterance** | Note pre-utterance in milliseconds. | `set_preutterance(self, preutterance)` | `get_preutterance(self)` | `init_preutterance(self)` | `float`
VoiceOverlap | Note overlap in milliseconds. | `set_overlap(self, overlap)` | `get_overlap(self)` | `init_overlap(self)` | `float`
Intensity | Note intensity in percent. | `set_intensity(self, intensity)` | `get_intensity(self)` | - | `float` 
Modulation | Note modulation in percent. | `set_modulation(self, modulation)` | `get_modulation(self)` | - | `float`
StartPoint | Note start point/time in milliseconds. | `set_start_point(self, start_point)` | `get_start_point(self)` | `init_start_point(self)` | `float` 
Envelope | Note envelope. | `set_envelope(self, envelope)` | `get_envelope(self)` | - | `Envelope`
Tempo | Tempo at note in BPM. | `set_tempo(self, tempo)` | `get_tempo(self)` | - | `float`
Velocity | Note consonant velocity in percent. | `set_velocity(self, velocity)` | `get_velocity(self)` | - | `float`
Label | Label at note. | `set_label(self, label)` | `get_label(self, label)` | - | `str`
$direct | Boolean that enables direct rendering. | `set_direct(self, direct)` | `get_direct(self)` | - | `bool`
PBS, PBW, PBY, PBM | Mode 2 pitchbend data. | `set_mode2pitch(self, mode2pitch)` | `get_mode2pitch(self)` | - | `Mode2Pitch`
VBR | Mode 2 vibrato data. | `set_vibrato(self, vibrato)` | `get_vibrato(self)` | - | `Vibrato`
PitchBend, PBStart | Mode 1 pitchbend data. | `set_mode1pitch(self, mode1pitch)` | `get_mode1pitch(self)` | - | `Mode1Pitch`
*@preuttr* | Re-calculated pre-utterance in milliseconds. | - | `get_at_preutterance(self)` | - | `float`
*@overlap* | Re-calculated overlap in milliseconds. | - | `get_at_overlap(self)` | - | `float`
*@stpoint* | Calculated start point in milliseconds. | - | `get_at_start_point(self)` | - | `float`
*@filename* | Filename of sample. | - | `get_sample_filename(self)` | - | `str`
*@alias* | Alias with prefix map applied. Can also have VCV applied for shareware. | - | `get_alias(self)` | - | `str`
*@cache* | Note cache file path. Not present when the note has no cache. | - | `get_cache_location(self)` | - | `str`

Envelope
-----

A class for storing envelope data. Largely based on how delta's library stores envelopes.

<dl>
  <dt>Envelope(envelope = '')</dt>
  <dd>Makes an envelope from the string representation of it. Default envelope is 0, 5, 35, 0, 100, 100, 0
  Read more about envelopes in the @wiki.</dd>
</dl> 

---

### Data descriptors:
<dl>
  <dt>p</dt>
  <dd>List of floats that store p1, p2, p3, p4, and p5. These are in milliseconds.</dd>
  
  <dt>v</dt>
  <dd>List of floats that store v1, v2, v3, v4, and v5. These are in percentages.</dd>
</dl>

---

### Methods:
<dl>
  <dt>__str__(self)</dt>
  <dt>get(self)</dt>
  <dd>Returns the string representation of the envelope.</dd>
  
  <dt>set_all(self, *args)</dt>
  <dd>Sets all of the parameters of the envelope to the arguments. Order of arguments is p1, p2, p3, v1, v2, v3, v4, (A '%' can be here, copes with UTAU's weirdness), p4, p5, v5.</dd>
</dl>

Mode1Pitch
-----

A class for storing Mode1 pitchbend data. I gave my least efforts on this.

<dl>
  <dt>Mode1Pitch(PBStart = '', PitchBend = '')</dt>
  <dd>Makes a new Mode1 pitchbend class from sting representations of Mode1 pitchbend data. Defaults are PBStart=None and PitchBend=0
  Read more about Mode1Pitch in the @wiki.</dd>
</dl>

---

### Data descriptors:

<dl>
  <dt>start_time</dt>
  <dd>Stores the start time of the pitchbend data anchored around the start of the note in milliseconds.</dd>
  
  <dt>pitches</dt>
  <dd>Stores the pitchbend values. I think the pitchbend data is in cents. I don't know how far two neighboring points are in milliseconds.</dd>
</dl>

---

### Methods:

<dl>
  <dt>set_pitches(self, *args)</dt>
  <dd>Sets the pitchbend data to the arguments. Just use set_pitches(*some_list) when you have a list to put in.</dd>
  
  <dt>get_pitches(self)</dt>
  <dd>Returns the string representation of the pitchbend data. Just use some_mode1pitch_data.pitches to get the pitchbends in a list.</dd>
  
  <dt>set_start_time(self, PBStart)</dt>
  <dd>Sets the pitchbend's start time.</dd>
  
  <dt>get_start_time(self)</dt>
  <dd>Returns the string representation of the pitchbend's start time.</dd>
  
  <dt>get(self)</dt>
  <dd>Returns a dictionary with keys PBStart and PitchBend and values of the string representations.</dd>
</dl>

Mode2Pitch
-----

A class for Mode2 pitchbend data.

<dl>
  <dt>Mode2Pitch(PBS = '-25', PBW = '50', PBY = '0', PBM = '')</dt>
  <dd>Makes a new Mode2 pitchbend class from the string representations of Mode2 pitchbend data.</dd>
</dl>

---

### Data descriptors:
<dl>
  <dt>start_time</dt>
  <dd>Stores the first control point's time anchored around the start of the note in milliseconds.</dd>
  
  <dt>start_pitch</dt>
  <dd>Stores the first control poin's pitch in decacents??? 10 in this value is one semitone or 100 cents.</dd>
  
  <dt>pbw</dt>
  <dd>Stores a list of intervals between the control points in milliseconds.</dd>
  
  <dt>pby</dt>
  <dd>Stores a list of offsets in pitch of the control points in decacents. I guess that's what we're calling it now.</dd>
  
  <dt>pbm</dt>
  <dd>Stores the pitchbend curves as a list of strings. Blank is S-curve, s is straight line/Linear, j is J-curve, and r is R-curve</dd>
</dl>

---

### Methods:

<dl>
  <dt>set_pbs(self, st, sp = 0)</dt>
  <dt>set_pbw(self, *args)</dt>
  <dt>set_pby(self, *args)</dt>
  <dt>set_pbm(self, *args)</dt>
  <dd>Sets the corresponding data.</dd>
  
  <dt>get_pbs(self)</dt>
  <dt>get_pbw(self)</dt>
  <dt>get_pby(self)</dt>
  <dt>get_pbm(self)</dt>
  <dd>Gets the string representation of the corresponding data.</dd>
  
  <dt>get(self)</dt>
  <dd>Returns a dictionary with keys PBS, PBW, PBY, and PBM with its values as their corresponding data in their string representations.</dd>
</dl>

Vibrato
-----

A class for storing Mode2 vibrato data.

<dl>
  <dt>Vibrato(VBR = '')</dt>
  <dd>Makes a new Vibrato class for Mode2 vibrato data.
  Defaults are length 65, cycle 160, depth 35, fade in and out 20, the rest 0.</dd>
</dl>

---

### Data descriptors:
<dl>
  <dt>length</dt>
  <dt>cycle</dt>
  <dt>depth</dt>
  <dt>fade_in</dt>
  <dt>fade_out</dt>
  <dt>phase</dt>
  <dt>offset</dt>
  <dd>These are pretty self explanatory. Offset is the Pitch in the Vibrato window.
  Units for these are percent, millisencond, cent, percent, percent, percent, and cent.</dd>
</dl>

---

### Methods:

<dl>
  <dt>set_all(self, length = None, cycle = None, depth = None, fade_in = None, fade_out = None, phase = None, offset = None)</dt>
  <dd>Sets all vibrato data. I might write separate setters and getters for each but I can't be bothered for now.</dd>

  <dt>__str__(self)</dt>
  <dt>get(self)</dt>
  <dd>Returns the string representation of vibrato.</dd>
</dl>

---

~~You did it. You read through all of it... maybe...~~
