import re

#Envelope class. Largely based on how Delta stores Envelope data.
class Envelope:
    def __init__(self, envelope):
        self.p = []
        self.v = []
        self.set(*envelope.split(','))
    
    def set(self, *args):
        tmp = []
        self.p = []
        self.t = []
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

    def __str__(self):
        res = [f'{x:.3f}'.rstrip('0').rstrip('.') for x in [*self.p[:3], *self.v[:4]]]
        if len(self.p) >= 4:
            res.extend(['%', f'{self.p[3]:.3f}'.rstrip('0').rstrip('.')])
        if len(self.p) == 5:
            res.extend([f'{x:.3f}'.rstrip('0').rstrip('.') for x in [self.p[4], self.v[4]]])
        return ','.join(res)

    def get(self):
        return str(self)

#Mode1 Pitch Class. Honestly, I don't really like Mode1. I feel like someone's gonna need this tho so.
class Mode1Pitch:
    def __init__(self, PBStart = '', PitchBend = ''):
            self.start_time = None if PBStart == '' else float(PBStart)
            self.pitches = [float(x) if x != '' else 0 for x in PitchBend.split(',')]

    def set_pitches(self, *args):
        self.pitches = [float(x) if x != '' else 0 for x in args]

    def get_pitches(self):
        return ','.join([f'{x:.3f}'.rstrip('0').rstrip('.') for x in self.pitches])

    def set_start_time(self, PBStart):
        self.start_time = float(PBStart)

    def get_start_time(self):
        return f'{self.start_time:.3f}'.rstrip('0').rstrip('.') if self.start_time != None else ''

    def get(self):
        res = {}
        res['PitchBend'] = self.get_pitches()
        res['PBStart'] = self.get_start_time()
        return res

#Mode2 Pitch class. Returns a dictionary of string values for get
class Mode2Pitch:
    def __init__(self, PBS = '-25', PBW = '50', PBY = '0', PBM = ''):
        pbst = PBS.split(';')
        self.start_time = float(pbst[0])
        self.start_pitch = 0
        if len(pbst) == 2:
            self.start_pitch = 0 if pbst[1] == '' else float(pbst[1])
        self.pbw = [float(x) if x != '' else 0 for x in PBW.split(',')]
        self.pby = [float(x) if x != '' else 0 for x in PBY.split(',')]
        self.pbm = PBM.split(',')

    #TODO: Add append and extend for PBW, PBY, PBM maybe.

    def set_pbs(self, st, sp = 0):
        self.start_time = st
        self.start_pitch = sp

    def get_pbs(self):
        if self.start_pitch == 0:
            return f'{self.start_time:.3f}'.rstrip('0').rstrip('.')
        else:
            return f'{self.start_time:.3f}'.rstrip('0').rstrip('.') + f';{self.start_pitch:.3f}'.rstrip('0').rstrip('.')

    def set_pbw(self, *args):
        self.pbw = [float(x) if x != '' else 0 for x in args]

    def get_pbw(self):
        return ','.join([f'{x:.3f}'.rstrip('0').rstrip('.') for x in self.pbw])

    def set_pby(self, *args):
        self.pby = [float(x) if x != '' else 0 for x in args]

    def get_pby(self):
        return ','.join([f'{x:.3f}'.rstrip('0').rstrip('.') for x in self.pby])

    def set_pbm(self, *args):
        self.pbw = [str(x) for x in args]

    def get_pbm(self):
        return ','.join(self.pbm)

    def get(self):
        res = {}
        res['PBS'] = self.get_pbs()
        res['PBW'] = self.get_pbw()
        res['PBY'] = self.get_pby()
        res['PBM'] = self.get_pbm()

        return res
        
#Mode2 Vibrato class. This just deals with vibrato.
class Vibrato:
    def __init__(self, VBR):
        tmp = [float(x) for x in VBR.split(',')]
        if len(tmp) < 7:
            tmp.extend([65, 180, 35, 20, 20, 0, 0])
        self.length = tmp[0]
        self.cycle = tmp[1]
        self.depth = tmp[2]
        self.fade_in = tmp[3]
        self.fade_out = tmp[4]
        self.phase = tmp[5]
        self.offset = tmp[6]

    def set_all(self, length = None, cycle = None, depth = None, fade_in = None, fade_out = None, phase = None, offset = None):
        self.length = length if length else self.length
        self.cycle = cycle if cycle else self.cycle
        self.depth = depth if depth else self.depth
        self.fade_in = fade_in if fade_in else self.fade_in
        self.fade_out = fade_out if fade_out else self.fade_out
        self.phase = phase if phase else self.fade_out
        self.offset = offset if offset else self.offset
    
    def __str__(self):
        tmp = [self.length, self.cycle, self.depth, self.fade_in, self.fade_out, self.phase, self.offset]
        return ','.join([f'{x:.3f}'.rstrip('0').rstrip('.') for x in tmp]) + ',0'

    def get(self):
        return str(self)
    

#Note class. Biggest class of all. Stores note data with corresponding classes for "special" data.
class Note:
    def __init__(self, note_type):
        #I have no idea on how I'd deal with this. The easiest way is to just let it be a string...
        self.note_type = note_type
        #In case it's needed to bring back a delete note... I don't even know if anyone needs it at all.
        #Not writing a function just to set this back to False. Just keep in mind when you're reading this.
        self.isdeleted = False
        #Needed note data. Intensity and Modulation are just preferences.
        self.note_data = {
            'Length' : '480',
            'Lyric' : 'あ',
            'NoteNum' : '60',
            'PreUtterance' : None,
            'Intensity' : '100',
            'Modulation' : '0'
        }

    def delete_note(self):
        #Sets Note type to DELETE. This deletes the note... I hope I don't need to change note order for this.
        self.isdeleted = True

    def get_note_type(self):
        #Please use this, because it returns DELETE when the note is deleted
        if self.isdeleted:
            return 'DELETE'
        else:
            return self.note_type

    #For custom data. Must only be given data with __str__ or __repr__. Please kindly make your own data class.
    def set_custom_data(self, name, data):
        self.note_data[name] = str(data)

    #Also make the data class interpret its string representation...
    def get_custom_data(self, name):
        if name in self.note_data:
            return self.note_data[name]
        else:
            return None

    #For setting multiple data. Must only be given string data.
    def set_multiple_data(self, **kwargs):
        for k, v in kwargs.items():
            self.note_data[k] = v

    #For converting the Note class back to UTAU formatting
    def __str__(self):
        string = f'[#{self.note_type}]\n' if not self.isdeleted else '[#DELETE]\n'
        for k, v in self.note_data.items():
            if not k.startswith('@'):
                string += f'{k}='
                if v:
                    string += f'{v}\n'
                else:
                    string += '\n'

        return string

    def get(self):
        return str(self)

    #Setters and Getters. Converts data on the fly. Probably not a good idea.
    #The following setters and getters are for required note data.
    def set_length(self, length):
        self.note_data['Length'] = f'{length:d}'

    def get_length(self):
        return int(self.note_data['Length'])

    def set_lyric(self, lyric):
        self.note_data['Lyric'] = lyric

    def get_lyric(self):
        return self.note_data['Lyric']

    def init_lyric(self):
        #This sets the lyric to what it is with the prefix map applied.
        #Probably VCV as well for those who use AutoVCV in Shareware
        if '@alias' in self.note_data:
            self.note_data['Lyric'] = self.note_data['@alias']

    def set_note_num(self, note_num):
        self.note_data['NoteNum'] = f'{note_num:d}'
    
    def get_note_num(self):
        return int(self.note_data['NoteNum'])

    def set_preutterance(self, preutterance):
        #Some might prefer using decimals.
        #This isn't as elegant as {preutterance:.3g} but it switches to e when needed
        #I also know this truncates preutterance to 3 decimals but... Come on...
        self.note_data['PreUtterance'] = f'{preutterance:.3f}'.rstrip('0').rstrip('.')

    def get_preutterance(self):
        #The PreUtterance value can be blank, but is required.
        #The way I store this blank is by making it None.
        if self.note_data['PreUtterance']:
            return int(self.note_data['PreUtterance'])
        else:
            return None

    def init_preutterance(self):
        #UTAU sends in preutterance values, this initializes it on the PreUtterance data
        #Is obsolete for INSERT notes unless somehow you generate the read-only data
        #I mean I guess you can get this data through the oto...
        self.note_data['PreUtterance'] = self.note_data['@preuttr']

    #The following setters and getters are optional note data, and must be checked if present.
    def set_overlap(self, overlap):
        self.note_data['VoiceOverlap'] = f'{overlap:.3f}'.rstrip('0').rstrip('.')

    def get_overlap(self):
        #TODO: Get overlap from @overlap or just check VoiceOverlap?
        if 'VoiceOverlap' in self.note_data:
            return self.note_data['VoiceOverlap']
        else:
            return None

    def init_overlap(self):
        #Same for init_preutterance
        self.note_data['VoiceOverlap'] = self.note_data['@overlap']

    def set_intensity(self, intensity):
        self.note_data['Intensity'] = f'{intensity:.3f}'.rstrip('0').rstrip('.')

    def get_intensity(self):
        if 'Intensity' in self.note_data:
            return float(self.note_data['Intensity'])
        else:
            return None

    def set_modulation(self, modulation):
        self.note_data['Modulation'] = f'{modulation:.3f}'.rstrip('0').rstrip('.')

    def get_modulation(self):
        if 'Modulation' in self.note_data:
            return float(self.note_data['Modulation'])
        else:
            return None

    def set_start_point(self, start_point):
        self.note_data['StartPoint'] = f'{start_point:.3f}'.rstrip('0').rstrip('.')

    def get_start_point(self, start_point):
        #TODO: Same as get_overlap
        if 'StartPoint' in self.note_data:
            return float(self.note_data['StartPoint'])
        else:
            return None

    def init_start_point(self):
        self.note_data['StartPoint'] = self.note_data['@stpoint']

    def set_envelope(self, envelope):
        #Using str makes it able to accept both string envelopes and the Envelope class... I hope
        self.note_data['Envelope'] = str(envelope)

    def get_envelope(self):
        if 'Envelope' in self.note_data:
            return Envelope(self.note_data['Envelope'])
        else:
            return None

    def set_tempo(self, tempo):
        self.note_data['Tempo'] = f'{tempo:.3f}'.rstrip('0').rstrip('.')

    def get_tempo(self):
        if 'Tempo' in self.note_data:
            return float(self.note_data['Tempo'])
        else:
            return None

    def set_velocity(self, velocity):
        self.note_data['Velocity'] = f'{velocity:.3f}'.rstrip('0').rstrip('.')

    def get_velocity(self):
        if 'Velocity' in self.note_data:
            return float(self.note_data['Velocity'])
        else:
            return None

    def set_label(self, label):
        self.note_data['Label'] = label

    def get_label(self):
        if 'Label' in self.note_data:
            return float(self.note_data['Velocity'])
        else:
            return None

    def set_direct(self, direct):
        self.note_data['$direct'] = str(direct).lower()

    def get_direct(self):
        if '$direct' in self.note_data:
            return self.note_data['$direct'] == 'true'
        else:
            return None

    def set_mode2pitch(self, mode2pitch):
        if isinstance(mode2pitch, Mode2Pitch):
            self.set_multiple_data(**mode2pitch.get())
        else:
            self.set_multiple_data(**mode2pitch)

    def get_mode2pitch(self):
        if 'PBS' in self.note_data:
            res = Mode2Pitch(self.note_data['PBS'], self.note_data['PBW'], self.note_data['PBY'])
            if 'PBM' in self.note_data:
                res.set_pbm(*self.note_data['PBM'].split(','))
            return res
        else:
            return None

    def set_vibrato(self, vibrato):
        self.note_data['Vibrato'] = str(vibrato)

    def get_vibrato(self):
        if 'Vibrato' in self.note_data:
            return Vibrato(self.note_data['Vibrato'])
        else:
            return None

    def set_mode1pitch(self, mode1pitch):
        if isinstance(mode1pitch, Mode1Pitch):
            self.set_multiple_data(**mode1pitch.get())
        else:
            self.set_multiple_data(**mode1pitch)

    #Getters for read-only data. All of these start with @
    def get_at_preutterance(self):
        return self.note_data['@preuttr']

    def get_at_overlap(self):
        return self.note_data['@overlap']

    def get_at_start_point(self):
        return self.note_data['@stpoint']

    #These do not exist when the note is a rest note
    def get_sample_filename(self):
        if '@filename' in self.note_data:
            return self.note_data['@filename']

    def get_alias(self):
        if '@alias' in self.note_data:
            return self.note_data['@alias']

    #This also doesn't exists when there is no cache for the note
    def get_cache_location(self):
        if '@cache' in self.note_data:
            return self.note_data['@cache']
            
def createNote(lyric = 'あ', length = 480, note_num = 60, **kwargs):
    #Creates a new INSERT note.
    note = Note('INSERT')
    note.set_note_num(note_num)
    note.set_lyric(lyric)
    note.set_length(length)
    note.set_multiple_data(**kwargs)
    
#UtauPlugin class. Has data for everything UTAU sends in.
class UtauPlugin:
    def __init__(self, fpath):
        #Should I use codecs for this??? I just don't like dealing with \r\n at all.
        data_string = open(fpath, encoding = 'shiftjis').readlines()
        phase = 0
        self.settings = {}
        self.prev_note = None
        self.next_note = None
        self.notes = []
        sectionName = ''
        #I'm sorry if you're disgusted by this parsing.
        for line in data_string:
            sectionMatch = re.match('\[#(.+)\]', line)
            if sectionMatch:
                phase += 1
                sectionName = sectionMatch.group(1)
                continue
            
            if phase == 1:
                self.version = line[:-1]
            elif phase == 2:
                setStr = line.split('=')
                self.settings[setStr[0]] = setStr[1][:-1]
            else:
                if phase - 3 == len(self.notes):
                    self.notes.append(Note(sectionName))   
                setStr = line.split('=')
                self.notes[-1].set_custom_data(setStr[0], setStr[1][:-1])

        if self.notes[0].get_note_type() == 'PREV':
            self.prev_note = self.notes.pop(0)

        if self.notes[-1].get_note_type() == 'NEXT':
            self.next_note = self.notes.pop()
    
    def insert_note(self, idx, note):
        self.notes.insert(idx, note)

    def delete_note(self, idx):
        self.notes[idx].delete_note()

    def get_notes(self):
        #This function returns notes that are not deleted.
        notes = []
        for note in self.notes:
            if not note.isdeleted:
                notes.append(note)
        return notes

    def __str__(self):
        string = ''
        if self.prev_note:
            string += str(self.prev_note)

        for note in self.notes:
            string += str(note)

        if self.next_note:
            string += str(self.next_note)

        return string

    def write(self, f):
        f.write(str(self))