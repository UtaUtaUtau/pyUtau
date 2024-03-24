from __future__ import annotations
import re
import os

__all__ = [
    'Envelope',
    'Mode1Pitch',
    'Mode2Pitch',
    'Vibrato',
    'Note',
    'UtauPlugin'
    ]

#Envelope class. Largely based on how Delta stores Envelope data.
class Envelope:
    """
    A class for envelope data. Largely based on how delta's library stores envelopes.

    Attributes
    ----------
    p : list of float
        List that stores p1, p2, p3, p4, and p5. These are in milliseconds.
    
    v : list of float
        List that stores v1, v2, v3, v4, and v5. These are in percent.
    """
    def __init__(self, envelope: str = ''):
        """
        Makes an envelope from the string representation of it.

        Parameters
        ----------
        envelope : str
            The string represenation of the envelope. Default is '', which is interpreted as [0, 5, 35, 0, 100, 100, 0].
        """
        self.p: list[float] = []
        self.v: list[float] = []
        self.set_all(*envelope.split(','))
    
    def set_all(self, *args: float | str) -> None:
        """
        Sets all of the parameters of the envelope to the arguments.
        Order of arguments is p1, p2, p3, v1, v2, v3, v4, an optional '%', p4, p5, v5.

        Parameters
        *args : float or str
            The envelope parameters.
        """
        tmp = []
        self.p = []
        self.v = []
        if len(args) > 1 and args[0] != '':
            tmp.extend(args)

        if len(tmp) < 3:
            tmp.extend(['0', '5', '35'])

        if len(tmp) < 7:
            tmp.extend(['0', '100', '100', '0'])

        self.p.extend([float(x) for x in tmp[:3]])
        self.v.extend([float(x) for x in tmp[3:7]])

        if '%' in tmp:
            if len(tmp) > 8:
                self.p.append(float(tmp[8]))
            if len(tmp) > 9:
                self.p.append(float(tmp[9]))
            if len(tmp) > 10:
                self.v.append(float(tmp[10]))
        else:
            if len(tmp) > 7:
                self.p.append(float(tmp[7]))
            if len(tmp) > 8:
                self.p.append(float(tmp[8]))
            if len(tmp) > 9:
                self.v.append(float(tmp[9]))

    def __str__(self) -> str:
        '''Unparses the envelope data to a string.'''
        res = [f'{x:.3f}'.rstrip('0').rstrip('.') for x in [*self.p[:3], *self.v[:4]]]
        if len(self.p) >= 4:
            res.extend(['%', f'{self.p[3]:.3f}'.rstrip('0').rstrip('.')])
        if len(self.p) == 5:
            res.extend([f'{x:.3f}'.rstrip('0').rstrip('.') for x in [self.p[4], self.v[4]]])
        return ','.join(res)

    def get(self) -> str:
        '''Unparses the envelope data to a string.'''
        return str(self)

    def copy(self) -> Envelope:
        '''Returns a deep copy of the envelope.'''
        return Envelope(self.get())

#Mode1 Pitch Class. Honestly, I don't really like Mode1. I feel like someone's gonna need this tho so.
class Mode1Pitch:
    """
    A class for Mode1 pitchbend data.

    Attributes
    ----------
    start_time : float or None
        The start time in milliseconds of the pitchbend data relative to the start of the note.
    
    pitches : list of float
        The pitchbend offsets in cents. Each pitchbend point is 5 ticks apart.
    """
    def __init__(self, PBStart: str = '', PitchBend: str = ''):
        """
        Makes a new Mode1 pitchbend class from sting representations of Mode1 pitchbend data.

        Parameters
        ----------
        PBStart : str
            The data in PBStart. Default is '', which is interpreted as None.

        PitchBend : str
            The data in PitchBend. Default is '', which is interpreted as [0].
        """
        self.start_time: float | None = None if PBStart == '' else float(PBStart)
        self.pitches: list[float] = [float(x) if x != '' else 0 for x in PitchBend.split(',')]

    def set_pitches(self, *args: float | str) -> None:
        """
        Sets the pitchbend values.

        Parameters
        ----------
        *args : float or str
            The pitchbend points.
        """
        self.pitches = [float(x) if x != '' else 0 for x in args]

    def get_pitches(self) -> str:
        '''Unparses the pitchbend points to a string.'''
        return ','.join([f'{x:.3f}'.rstrip('0').rstrip('.') for x in self.pitches])

    def set_start_time(self, PBStart: float | str) -> None:
        """
        Sets the start time of the pitchbend.

        Parameters
        ----------
        PBStart : float or str
            The start time of the pitchbend.
        """
        self.start_time = None if PBStart == '' else float(PBStart)

    def get_start_time(self) -> str:
        '''Unparses the pitchbend start time to a string.'''
        return f'{self.start_time:.3f}'.rstrip('0').rstrip('.') if self.start_time != None else ''

    def get(self) -> dict[str, str]:
        '''Unparses all the data needed for Mode1 pitchbends into a dictionary.'''
        res = {}
        res['PitchBend'] = self.get_pitches()
        res['PBStart'] = self.get_start_time()
        return res

    def copy(self) -> Mode1Pitch:
        '''Returns a deep copy of the Mode1 pitchbend.'''
        return Mode1Pitch(self.get_start_time(), self.get_pitches())

#Mode2 Pitch class. Returns a dictionary of string values for get
class Mode2Pitch:
    """
    A class for Mode2 pitchbend data.

    Attributes
    ----------
    start_time : float
        The time of the first control point in milliseconds.
    
    start_pitch : float
        The pitch offset of the first control point.
    
    pbw : list of float
        The list of intervals between control points in milliseconds.

    pby : list of float
        The list of pitch offsets for each control point.

    pbm : list of str
        The list of pitchbend types for each interval. A blank string is the S-curve, linear is 's', R and J curve are 'r' and 'j'.

    Notes
    -----
    The pitch offset for Mode2 pitchbends is cents divided by 10, which means that 1 unit is 10 cents.
    """
    def __init__(self, PBS : str = '-25', PBW : str = '50', PBY : str = '0', PBM : str = ''):
        """
        Makes a new Mode2 pitchbend class from sting representations of Mode2 pitchbend data.

        Parameters
        ----------
        PBS : str
            The data in PBS. Default is '-25'.

        PBW : str
            The data in PBW. Default is '50'.

        PBY : str
            The data in PBY. Default is '0'.

        PBM : str
            The data in PBW. Default is ''.
        """
        pbst = PBS.split(';')
        self.start_time: float = float(pbst[0])
        self.start_pitch: float = 0
        if len(pbst) == 2:
            self.start_pitch = 0 if pbst[1] == '' else float(pbst[1])
        self.pbw: list[float] = [float(x) if x != '' else 0 for x in PBW.split(',')]
        self.pby: list[float] = [float(x) if x != '' else 0 for x in PBY.split(',')]
        self.pbm: list[str] = PBM.split(',')

    #TODO: Add append and extend for PBW, PBY, PBM maybe.

    def set_pbs(self, st: float, sp: float = 0) -> None:
        """
        Sets the values included within PBS.

        Parameters
        ----------
        st : float
            The time of the first control point in milliseconds.
        
        sp : float
            The pitch offset of the first control point.
        """
        self.start_time = st
        self.start_pitch = sp

    def get_pbs(self) -> str:
        '''Unparses the data needed for PBS into a string.'''
        if self.start_pitch == 0:
            return f'{self.start_time:.3f}'.rstrip('0').rstrip('.')
        else:
            return f'{self.start_time:.3f}'.rstrip('0').rstrip('.') + f';{self.start_pitch:.3f}'.rstrip('0').rstrip('.')

    def set_pbw(self, *args: float | str) -> None:
        """
        Sets the values for PBW.

        Parameters
        ----------
        *args : float or str
            The list of intervals between control points in milliseconds.
        """
        self.pbw = [float(x) if x != '' else 0 for x in args]

    def get_pbw(self) -> str:
        '''Unparses the data needed for PBW into a string.'''
        return ','.join([f'{x:.3f}'.rstrip('0').rstrip('.') for x in self.pbw])

    def set_pby(self, *args: float | str) -> None:
        """
        Sets the values for PBY.

        Parameters
        ----------
        *args : float or str
            The list of pitch offsets for each control point.
        """
        self.pby = [float(x) if x != '' else 0 for x in args]

    def get_pby(self) -> str:
        '''Unparses the data needed for PBY into a string.'''
        return ','.join([f'{x:.3f}'.rstrip('0').rstrip('.') for x in self.pby])

    def set_pbm(self, *args: str):
        """
        Sets the values for PBM.

        Parameters
        ----------
        *args : str
            The list of pitchbend types for each interval. A blank string is the S-curve, linear is 's', R and J curve are 'r' and 'j'.
        """
        self.pbm = [str(x) for x in args]

    def get_pbm(self):
        '''Unparses the data needed for PBM into a string.'''
        return ','.join(self.pbm)

    def get(self) -> dict[str, str]:
        '''Unparses all the data needed for Mode2 pitchbends into a dictionary.'''
        res = {}
        res['PBS'] = self.get_pbs()
        res['PBW'] = self.get_pbw()
        res['PBY'] = self.get_pby()
        res['PBM'] = self.get_pbm()

        return res

    def copy(self):
        '''Returns a deep copy of the Mode2 pitchbend.'''
        return Mode2Pitch(self.get_pbs(), self.get_pbw(), self.get_pby(), self.get_pbm())    
    
#Mode2 Vibrato class. This just deals with vibrato.
class Vibrato:
    """
    A class for Mode2 vibrato data.

    Attributes
    ----------
    length : float
        The length of the vibrato in percent. Default is 65.

    cycle : float
        The period of the vibrato in milliseconds. Default is 180.

    depth : float
        The depth of the vibrato in cents. Default is 35.
    
    fade_in : float
        The length of the fade in of the vibrato in percent. Default is 20.

    fade_out : float
        The length of the fade out of the vibrato in percent. Default is 20.

    phase : float
        The phase of the vibrato in percent. 100% phase is the same as 0% phase. Default is 0.

    offset : float
        The offset of the vibrato in percent. Default is 0.
    """
    def __init__(self, VBR: str = ''):
        """
        Makes a new Vibrato class from sting representations of Vibrato data.

        Parameters
        ----------
        VBR : str
            The data in VBR. Default is '', which is interpreted as '65, 180, 35, 20, 20, 0, 0'.
        """
        tmp = [float(x) if x != '' else 0 for x in VBR.split(',')]
        if len(tmp) < 7:
            tmp = [65, 180, 35, 20, 20, 0, 0]
        self.length: float = tmp[0]
        self.cycle: float = tmp[1]
        self.depth: float = tmp[2]
        self.fade_in: float = tmp[3]
        self.fade_out: float = tmp[4]
        self.phase: float = tmp[5]
        self.offset: float = tmp[6]

    def set_all(self, length: float | None = None, cycle: float | None = None, depth: float | None = None, fade_in: float | None = None, fade_out: float | None = None, phase: float | None = None, offset: float | None = None):
        """
        Sets all the relevant data for the vibrato.

        Parameters
        ----------
        length : float or None
        The length of the vibrato in percent. Default is None.

        cycle : float or None
            The period of the vibrato in milliseconds. Default is  None.

        depth : float or None
            The depth of the vibrato in cents. Default is None.
        
        fade_in : float or None
            The length of the fade in of the vibrato in percent. Default is None.

        fade_out : float or None
            The length of the fade out of the vibrato in percent. Default is None.

        phase : float or None
            The phase of the vibrato in percent. 100% phase is the same as 0% phase. Default is None.

        offset : float or None
            The offset of the vibrato in percent. Default is None.
        """
        self.length = length if length != None else self.length
        self.cycle = cycle if cycle != None else self.cycle
        self.depth = depth if depth != None else self.depth
        self.fade_in = fade_in if fade_in != None else self.fade_in
        self.fade_out = fade_out if fade_out != None else self.fade_out
        self.phase = phase if phase != None else self.phase
        self.offset = offset if offset != None else self.offset
    
    def __str__(self):
        '''Unparses the data needed for VBR into a string.'''
        tmp = [self.length, self.cycle, self.depth, self.fade_in, self.fade_out, self.phase, self.offset]
        return ','.join([f'{x:.3f}'.rstrip('0').rstrip('.') for x in tmp]) + ',0'

    def get(self):
        '''Unparses the data needed for VBR into a string.'''
        return str(self)

    def copy(self):
        '''Returns a deep copy of the Vibrato.'''
        return Vibrato(self.get())
    

#Note class. Biggest class of all. Stores note data with corresponding classes for "special" data.
class Note:
    """
    A class that stores note data.

    Attributes
    ----------
    note_type : str
        Stores the note type. Does not change to DELETE when delete_note() is used.

    is_deleted : bool
        If the note is the DELETE note type or not.
    
    note_data : dict[str, str or None]
        Where all note data is stored. Blank entries are written as None. Only put string keys and values here.
    """
    def __init__(self, note_type: str = 'INSERT'):
        """
        Creates a note with defaults set.

        Parameters
        ----------
        note_type : str
            The note type. Default is INSERT.
        """
        #I have no idea on how I'd deal with this. The easiest way is to just let it be a string...
        self.note_type: str = note_type
        #In case it's needed to bring back a delete note... I don't even know if anyone needs it at all.
        #Not writing a function just to set this back to False. Just keep in mind when you're reading this.
        self.is_deleted: bool = False
        #Needed note data. Intensity and Modulation are just preferences.
        self.note_data: dict[str, str | None] = {
            'Length' : '480',
            'Lyric' : 'あ',
            'NoteNum' : '60',
            'PreUtterance' : None
        }
    
    def copy(self) -> Note:
        '''Returns a deep copy of the note.'''
        res = Note(self.note_type)
        res.is_deleted = self.is_deleted
        res.set_multiple_data(**self.note_data)
        return res

    #Clears all properties except essential ones
    def clear_note(self) -> Note:
        """
        Returns a clean slate note copy of the note with INSERT as its note type.

        Notes
        -----
        Clean slate means it only has the required parameters plus intensity, modulation, and tempo.
        I think those are default essential. This is good for cleaning extra properties by removing
        the existing note and inserting the clean note, as UTAU never considers a property cleared
        when it's not returned.
        """
        new_data = {}
        for k, v in self.note_data.items():
            if k in ['Length', 'Lyric', 'NoteNum', 'PreUtterance', 'Intensity', 'Modulation', 'Tempo']:
                new_data[k] = v
        res = Note()
        res.set_multiple_data(**new_data)
        return res

    def delete_note(self) -> None:
        '''Sets a note to a DELETE note without changing the note type.'''
        #Sets Note type to DELETE. This deletes the note... I hope I don't need to change note order for this.
        self.is_deleted = True

    def get_note_type(self) -> str:
        '''Returns the note type, and also responds to is_deleted. Use this if you need to find DELETE notes.'''
        #Please use this, because it returns DELETE when the note is deleted
        if self.is_deleted:
            return 'DELETE'
        else:
            return self.note_type

    #For custom data. Must only be given data with __str__ or __repr__. Please kindly make your own data class.
    def set_custom_data(self, name: str, data: str) -> None:
        """
        Sets in custom data and saves the string representation of the data under that name.

        Parameters
        ----------
        name : str
            The name of the custom property.
        
        data : str
            The data stored for the property.
        """
        self.note_data[name] = str(data)

    #Also make the data class interpret its string representation...
    def get_custom_data(self, name: str) -> str | None:
        """
        Gets the string representation of the custom data under name.

        Parameters
        ----------
        name : str
            The name of the custom property.
        
        Returns
        -------
        data : str or None
            The data, if it exists.
        """
        return self.note_data.get(name, None)

    #For setting multiple data. Must only be given data with __str__ or __repr__
    def set_multiple_data(self, **kwargs) -> None:
        '''Sets multiple custom data in the note. Mainly added for the parsing process.'''
        for k, v in kwargs.items():
            self.note_data[k] = str(v)

    #For converting the Note class back to UTAU formatting
    def __str__(self) -> str:
        '''Unparses the note to a string.'''
        string = f'[#{self.note_type}]\n' if not self.is_deleted else '[#DELETE]\n'
        for k, v in self.note_data.items():
            string += f'{k}='
            if v:
                string += f'{v}\n'
            else:
                string += '\n'

        return string

    def get(self) -> str:
        '''Unparses the note to a string.'''
        return str(self)

    #Setters and Getters. Converts data on the fly. Probably not a good idea.
    #The following setters and getters are for required note data.
    def set_length(self, length: int) -> None:
        self.note_data['Length'] = f'{length:d}'

    def get_length(self) -> int:
        '''The note's length. 480 = 1 quarter note.'''
        return int(self.note_data['Length'])

    length = property(get_length, set_length)

    def set_lyric(self, lyric: str) -> None:
        self.note_data['Lyric'] = lyric

    def get_lyric(self) -> str:
        '''The note's lyric.'''
        return self.note_data['Lyric']

    lyric = property(get_lyric, set_lyric)

    def init_lyric(self) -> None:
        '''Sets the lyric of the note with the prefix map applied and with automatic VCV chaining applied for shareware.'''
        if '@alias' in self.note_data:
            self.note_data['Lyric'] = self.note_data['@alias']

    def set_note_num(self, note_num: int) -> None:
        self.note_data['NoteNum'] = f'{note_num:d}'
    
    def get_note_num(self) -> int:
        '''The note's pitch. C4 = 60'''
        return int(self.note_data['NoteNum'])

    note_num = property(get_note_num, set_note_num)

    def set_preutterance(self, preutterance: float) -> None:

        #Some might prefer using decimals.
        #This isn't as elegant as {preutterance:.3g} but it switches to e when needed
        #I also know this truncates preutterance to 3 decimals but... Come on...
        self.note_data['PreUtterance'] = f'{preutterance:.3f}'.rstrip('0').rstrip('.')

    def get_preutterance(self) -> float | None:
        '''The note's pre-utterance in milliseconds.'''
        #The PreUtterance value can be blank, but is required.
        #The way I store this blank is by making it None.
        if self.note_data['PreUtterance']:
            return float(self.note_data['PreUtterance'])
        else:
            return None

    preutterance = property(get_preutterance, set_preutterance)

    def init_preutterance(self) -> None:
        '''Sets the pre-utterance of the note calculated by UTAU to the pre-utterance property.'''
        #UTAU sends in preutterance values, this initializes it on the PreUtterance data
        #Is obsolete for INSERT notes unless somehow you generate the read-only data
        #I mean I guess you can get this data through the oto...
        self.note_data['PreUtterance'] = self.note_data['@preuttr']

    #The following setters and getters are optional note data, and must be checked if present.
    def set_overlap(self, overlap: float) -> None:
        self.note_data['VoiceOverlap'] = f'{overlap:.3f}'.rstrip('0').rstrip('.')

    def get_overlap(self) -> float | None:
        '''The note's overlap in milliseconds.'''
        if 'VoiceOverlap' in self.note_data:
            return float(self.note_data['VoiceOverlap'])
        else:
            return None

    overlap = property(get_overlap, set_overlap)

    def init_overlap(self) -> None:
        '''Sets the overlap of the note calculated by UTAU to the overlap property.'''
        #Same for init_preutterance
        self.note_data['VoiceOverlap'] = self.note_data['@overlap']

    def set_intensity(self, intensity: float) -> None:
        self.note_data['Intensity'] = f'{intensity:.3f}'.rstrip('0').rstrip('.')

    def get_intensity(self) -> float | None:
        '''The note's intensity in percent.'''
        if 'Intensity' in self.note_data:
            return float(self.note_data['Intensity'])
        else:
            return None

    intensity = property(get_intensity, set_intensity)

    def set_modulation(self, modulation: float) -> None:
        self.note_data['Modulation'] = f'{modulation:.3f}'.rstrip('0').rstrip('.')

    def get_modulation(self) -> float | None:
        '''The note's modulation in percent.'''
        if 'Modulation' in self.note_data:
            return float(self.note_data['Modulation'])
        else:
            return None

    modulation = property(get_modulation, set_modulation)

    def set_start_point(self, start_point: float) -> None:
        self.note_data['StartPoint'] = f'{start_point:.3f}'.rstrip('0').rstrip('.')

    def get_start_point(self) -> float | None:
        '''The note's start point/offset in milliseconds. The offset is relative to the offset of the oto.'''
        if 'StartPoint' in self.note_data:
            return float(self.note_data['StartPoint'])
        else:
            return None

    start_point = property(get_start_point, set_start_point)

    def init_start_point(self) -> None:
        '''Sets the start point of the note calculated by UTAU to the start point property.'''
        self.note_data['StartPoint'] = self.note_data['@stpoint']

    def set_envelope(self, envelope: str | Envelope) -> None:

        #Using str makes it able to accept both string envelopes and the Envelope class... I hope
        self.note_data['Envelope'] = str(envelope)

    def get_envelope(self) -> Envelope | None:
        '''The note's envelope.'''
        if 'Envelope' in self.note_data:
            return Envelope(self.note_data['Envelope'])
        else:
            return None

    envelope = property(get_envelope, set_envelope)

    def set_tempo(self, tempo: float) -> None:
        self.note_data['Tempo'] = f'{tempo:.3f}'.rstrip('0').rstrip('.')

    def get_tempo(self) -> float | None:
        '''The tempo at this note.'''
        if 'Tempo' in self.note_data:
            return float(self.note_data['Tempo'])
        else:
            return None

    tempo = property(get_tempo, set_tempo)

    def set_velocity(self, velocity: float) -> None:
        self.note_data['Velocity'] = f'{velocity:.3f}'.rstrip('0').rstrip('.')

    def get_velocity(self) -> float | None:
        '''The note's consonant velocity.'''
        if 'Velocity' in self.note_data:
            return float(self.note_data['Velocity'])
        else:
            return None

    velocity = property(get_velocity, set_velocity)

    def set_label(self, label: str) -> None:
        self.note_data['Label'] = label

    def get_label(self) -> str | None:
        '''The label at this note.'''
        return self.note_data.get('Label', None)

    label = property(get_label, set_label)

    def set_direct(self, direct: bool) -> None:
        self.note_data['$direct'] = str(direct).lower()

    def get_direct(self) -> bool | None:
        '''If the note is rendered without going through the resampler or not.'''
        if '$direct' in self.note_data:
            return self.note_data['$direct'] == 'true'
        else:
            return None

    direct = property(get_direct, set_direct)

    def set_flags(self, flags: str) -> None:
        self.note_data['Flags'] = str(flags)

    def get_flags(self) -> str | None:
        '''The note's flags.'''
        return self.note_data.get('Flags', None)

    flags = property(get_flags, set_flags)

    def set_mode2pitch(self, mode2pitch: Mode2Pitch | dict[str, str]) -> None:
        if isinstance(mode2pitch, Mode2Pitch):
            self.set_multiple_data(**mode2pitch.get())
        else:
            self.set_multiple_data(**mode2pitch)

    def get_mode2pitch(self) -> Mode2Pitch | None:
        '''Mode2 pitchbend data.'''
        if 'PBS' in self.note_data:
            res = Mode2Pitch(self.note_data['PBS'], self.note_data['PBW'])
            if 'PBY' in self.note_data:
                res.set_pby(*self.note_data['PBY'].split(','))
            if 'PBM' in self.note_data:
                res.set_pbm(*self.note_data['PBM'].split(','))
            return res
        else:
            return None

    mode2pitch = property(get_mode2pitch, set_mode2pitch)

    def set_vibrato(self, vibrato: str | Vibrato) -> None:
        self.note_data['VBR'] = str(vibrato)

    def get_vibrato(self) -> Vibrato | None:
        '''Mode2 vibrato data.'''
        if 'VBR' in self.note_data:
            return Vibrato(self.note_data['VBR'])
        else:
            return None

    vibrato = property(get_vibrato, set_vibrato)

    def set_mode1pitch(self, mode1pitch: Mode1Pitch | dict[str, str]) -> None:
        if isinstance(mode1pitch, Mode1Pitch):
            self.set_multiple_data(**mode1pitch.get())
        else:
            self.set_multiple_data(**mode1pitch)

        self.note_data['PBType'] = '5'

    def get_mode1pitch(self) -> Mode1Pitch | None:
        '''Mode1 pitchbend data.'''
        if 'PitchBend' in self.note_data:
            res = Mode1Pitch(PitchBend = self.note_data['PitchBend'])
            if 'PBStart' in self.note_data:
                res.set_start_time(self.note_data['PBStart'])
            
            return res
        else:
            return None

    mode1pitch = property(get_mode1pitch, set_mode1pitch)

    #Getters for read-only data. All of these start with @
    def get_at_preutterance(self) -> float:
        '''Re-calculated pre-utterance in milliseconds.'''
        return float(self.note_data['@preuttr'])

    def get_at_overlap(self) -> float:
        '''Re-calculated overlap in milliseconds.'''
        return float(self.note_data['@overlap'])

    def get_at_start_point(self) -> float:
        '''Calculated start point in milliseconds.'''
        return float(self.note_data['@stpoint'])

    #These do not exist when the note is a rest note
    def get_sample_filename(self) -> str | None:
        '''Filename of sample. Does not exists if note is a rest note.'''
        if '@filename' in self.note_data:
            return self.note_data['@filename']

    def get_alias(self) -> str | None:
        '''Alias with prefix map applied. Can also have VCV applied for shareware.'''
        if '@alias' in self.note_data:
            return self.note_data['@alias']

    #This also doesn't exists when there is no cache for the note
    def get_cache_location(self) -> str | None:
        '''Note cache file path. Not present when the note has no cache.'''
        if '@cache' in self.note_data:
            return self.note_data['@cache']
            
def create_note(lyric: str = 'あ', length: int = 480, note_num: int = 60, **kwargs) -> Note:
    """
    Makes a new INSERT note. Made for inserting notes specifically.

    Parameters
    ----------
    lyric : str
        The note's lyric. Defaults to 'あ'. Set to 'R' or a blank string if you want a rest note.

    length : int
        The note's length. 480 = 1 quarter note. Default is 480
    
    note_num : int
        The note's pitch. C4 = 60. Default is 60.
    
    **kwargs
        Other note data to insert.
    """
    #Creates a new INSERT note.
    note = Note()
    note.set_note_num(note_num)
    note.set_lyric(lyric)
    note.set_length(length)
    #Sets intensity and modulation data to 100 and 0 if new note is not a rest note
    if not lyric or lyric.lower() != 'r':
        note.set_intensity(100)
        note.set_modulation(0)
    note.set_multiple_data(**kwargs)

    return note
    
#UtauPlugin class. Has data for everything UTAU sends in.
class UtauPlugin:
    """
    The main class that parses the UST.

    Attributes
    ----------
    version : str or None
        Obsolete. Returns UST version. Will be None if not provided.
    
    settings : dict
        Dictionary of UST settings. These are read-only. Will be empty when not provided. Read more about it in the @wiki page.

    prev_note : Note or None
        Stores the note that precedes the selected notes in the UST. None if there is no PREV note.
    
    next_note : Note or None
        Stores the note that succeeds the selected notes in the UST. None if there is no NEXT note.

    notes : list of Note
        List that stores all notes.

    is_ust : bool
        If the parsed UST is the plugin format or not.
    """
    def __init__(self, fpath: str | os.PathLike, encoding: str = 'shiftjis'):
        """
        Initializes and parses the UST given.

        Parameters
        ----------
        fpath : str or path-like
            The path to the UST.
        
        encoding : str
            The encoding of the UST. Defaults to 'shiftjis'
        """
        data_string = open(fpath, encoding = encoding).readlines()
        phase = 0
        self.settings: dict = {}
        self.prev_note: Note | None = None
        self.next_note: Note | None = None
        self.version: str | None = None
        self.notes: list[Note] = []
        self.is_ust: bool = False
        #I'm sorry if you're disgusted by this parsing. Even if rewritten, my statement still holds.
        for line in data_string:
            sectionMatch = re.match('\[#(.+)\]', line)
            if sectionMatch:
                sectionName = sectionMatch.group(1)
                if sectionName == 'VERSION':
                    phase = 1
                elif sectionName == 'SETTING':
                    phase = 2
                elif sectionName == 'TRACKEND':
                    phase = 4
                    self.is_ust = True
                else:
                    phase = 3
                    self.notes.append(Note(sectionName))
                continue
            
            if phase == 1:
                self.version = line[:-1]
            elif phase == 2:
                setStr = line.split('=')
                self.settings[setStr[0]] = setStr[1][:-1]
            elif phase == 3:
                setStr = line.split('=')
                self.notes[-1].set_custom_data(setStr[0], setStr[1][:-1])

        if self.notes:
            if self.notes[0].get_note_type() == 'PREV':
                self.prev_note = self.notes.pop(0)

            if self.notes[-1].get_note_type() == 'NEXT':
                self.next_note = self.notes.pop()
    
    def insert_note(self, idx: int, note: Note) -> None:
        """
        Inserts note at the given index.

        Parameters
        ----------
        idx : int
            The index for where to insert the note.

        note : Note
            The note.
        """
        self.notes.insert(idx, note)

    def delete_note(self, idx : int) -> None:
        """
        Sets the note at the given index to a DELETE note. Does not remove it from the list.

        Parameters
        ----------
        idx : int
            The index of the note to delete.
        """
        self.notes[idx].delete_note()

    def get_notes(self) -> list[Note]:
        """
        Returns all notes that are not DELETE notes.

        Parameters
        ----------
        None

        Returns
        -------
        notes : list[Note]
            List of notes excluding DELETE notes.
        """
        notes = []
        for note in self.notes:
            if not note.is_deleted:
                notes.append(note)
        return notes

    def __str__(self) -> str:
        '''Unparses the whole class to a string for writing as a UST.'''
        string = ''
        if self.prev_note:
            string += str(self.prev_note)

        for note in self.notes:
            string += str(note)

        if self.next_note:
            string += str(self.next_note)
        
        if self.is_ust:
            string += '[#TRACKEND]'

        return string

    def write(self, fpath : str | os.PathLike, encoding: str = 'shiftjis', with_header: bool = False) -> None:
        """
        Writes the UST data to the given file path.

        Parameters
        ----------
        fpath : str or path-like
            The path to write the UST in.

        encoding : str
            The encoding used. Default is 'shiftjis'

        with_header : bool
            If the header is written or not. If self.is_ust is true, the header is always written. Default is false.
        """
        with open(fpath, 'w', encoding = encoding) as f:
            if with_header or self.is_ust:
                f.write('[#VERSION]\n')
                f.write(self.version + '\n')
                f.write('[#SETTING]\n')
                for k, v in self.settings.items():
                    f.write(f'{k}={v}\n')

            f.write(str(self))
