import midi          #Requires python midi module - available here - https://github.com/vishnubob/python-midi
import numpy as np

#Initialises MIDI track
pattern = midi.Pattern(resolution = 1000)
track = midi.Track()

pattern.append(track)

###Put your sequence here
protein = "MESKWYW" ###Sequence as a string here
protein.upper()

barTimer = 0 #Times the bar to 400 ticks
offBeat = 0 #offbeat counter

def Protein_to_note(AAnote):
    global barTimer
    global offBeat

    ###Notes assigned to amino acids - change these to your liking

    if AAnote == "G": #Glycine
        note = midi.C_5
    elif AAnote == "E": #Glutamic acid
        note = midi.E_5
    elif AAnote == "Q": #Glutamine
        note = midi.G_5
    elif AAnote == "S": #Serine
        note = midi.B_5
    elif AAnote == "A": #Alanine
        note = midi.C_6 
    elif AAnote == "R": #Asparagine
        note = midi.D_6
    elif AAnote == "D": #Aspartic acid
        note = midi.E_6
    elif AAnote == "L": #Leucine
        note = midi.Gb_6
    elif AAnote == "T": #Threeonine
        note = midi.G_6
    elif AAnote == "V": #Valine
        note = midi.A_6
    elif AAnote == "R": #Arginine
        note = midi.B_6
    elif AAnote == "I": #Isoleucine
        note = midi.C_4
    elif AAnote == "F": #Phenylanaline
        note = midi.E_4
    elif AAnote == "Y": #Tyrosine
        note = midi.G_4
    elif AAnote == "P": #Proline
        note = midi.B_4 
    elif AAnote == "K": #Lysine
        note = midi.C_7
    elif AAnote == "H": #Histidine
        note = midi.D_7
    elif AAnote == "M": #Methionine
        note = midi.Gb_7
    elif AAnote == "C": #Cysteine
        note = midi.A_7
    elif AAnote == "W": #Tryptophan
        note = midi.D_5
    else:
        return
    
    randTick = np.random.normal(0.5, 0.3, 1)[0] #random normal distribution help determines the note length/tick value

    if (100 *  randTick ) < 25 :
        tickValue = 25 #Think of 25 as 16th note
    elif ((100 * randTick) < 50) & (400 - (50 + barTimer) >-0.1):
        tickValue = 50 #Think of 50 as an 8th note
    elif ((100 *  randTick ) < 75) & (barTimer < 330):
        tickValue = 75  #Think of 75 as a dotted 8th note
    elif (barTimer < 305) :
        tickValue = 100 #Think of 100 as a quarter note
    else :
        tickValue = 25

    if (barTimer / 50).is_integer is False:
        offBeat += 1 #This counts the number of consecutive off beat notes 
        if offBeat > 2:         ###Change this value to allow for more or less consecutive off beat notes (ie "offBeat > 4:" would be more offbeat than "offBeat > 1")
            if tickValue == 50:
                tickValue = 25
            elif tickValue == 100:
                tickValue = 75


    on = midi.NoteOnEvent(tick = 0, velocity=20, pitch=note)
    track.append(on)
    off = midi.NoteOffEvent(tick= tickValue * 10, pitch=note)
    track.append(off)
    print(AAnote + "Done!")

    barTimer += tickValue
    if barTimer > 390 :
        barTimer = 0

    return
    

for AA in protein:
    Protein_to_note(AA)


#Ends and writes the track
eot = midi.EndOfTrackEvent(tick=1)
track.append(eot)
midi.write_midifile("exampleProtein.mid", pattern)