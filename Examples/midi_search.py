# -*- coding: utf-8 -*-
"""MIDI_Search.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1q_PuqEBGEZKMeb975WEPKH-Vrv30Tc_N

# MIDI Search (Ver 1.0)

***

## MIDI Search/Plagiarizm checker

***

#### Project Los Angeles

#### Tegridy Code 2021

***

# Setup Environment, clone needed repos, and install all required dependencies
"""

#@title Install all dependencies (run only once per session)
!git clone https://github.com/asigalov61/tegridy-tools
!apt install fluidsynth #Pip does not work for some reason. Only apt works
!pip install midi2audio

#@title Import all needed modules

print('Loading needed modules. Please wait...')
import os

import pickle

os.chdir('/content/tegridy-tools/tegridy-tools')
import TMIDI
import MIDI

from midi2audio import FluidSynth
from IPython.display import display, Javascript, HTML, Audio

from google.colab import output, drive

chords_list_f = []
melody_list_f = []

os.chdir('/content/')
print('Loading complete. Enjoy! :)')

"""# Download and process desired MIDI datasets

## PLEASE NOTE: You need to have at least 16GB free RAM to load large datasets
"""

# Commented out IPython magic to ensure Python compatibility.
#@title Download partial (small) pre-processed MIDI datasets
# %cd /content/

# POP909 dataset (Channel 0)
# https://github.com/music-x-lab/POP909-Dataset
!wget --no-check-certificate -O POP.zip "https://onedrive.live.com/download?cid=8A0D502FC99C608F&resid=8A0D502FC99C608F%2118359&authkey=AAYhmJhE0o8AM4g"
!unzip POP.zip

# groove2groove dataset (Channel 2)
# https://github.com/cifkao/groove2groove
# https://doi.org/10.5281/zenodo.3957999
!wget --no-check-certificate -O groove2groove.zip "https://onedrive.live.com/download?cid=8A0D502FC99C608F&resid=8A0D502FC99C608F%2118367&authkey=AHJ48GG8uGoOb5Y"
!unzip groove2groove.zip

# Reddit 130000 MIDIs dataset (aka Melody Kit 1.0 by Melody Man)
# Channel 0 only
!wget --no-check-certificate -O 130000.zip "https://onedrive.live.com/download?cid=8A0D502FC99C608F&resid=8A0D502FC99C608F%2118363&authkey=AITWpblsg68d9VI"
!unzip 130000.zip

# Reddit 30000 MIDIs subset (aka Melody Kit 1.0 by Melody Man)
# All channels except the drums
!wget --no-check-certificate -O 30000.zip "https://onedrive.live.com/download?cid=8A0D502FC99C608F&resid=8A0D502FC99C608F%2118371&authkey=AKqo-iUgbU4Z6Y8"
!unzip 30000.zip

# %cd /content/

# Commented out IPython magic to ensure Python compatibility.
#@title Download complete (large) pre-processed MIDI datasets
# %cd /content/

# POP909 dataset (Complete)
# https://github.com/music-x-lab/POP909-Dataset
!wget --no-check-certificate -O POP.zip "https://onedrive.live.com/download?cid=8A0D502FC99C608F&resid=8A0D502FC99C608F%2118362&authkey=AD3_7eDWpgUhcaw"
!unzip POP.zip

# groove2groove dataset (Complete)
# https://github.com/cifkao/groove2groove
# https://doi.org/10.5281/zenodo.3957999
!wget --no-check-certificate -O groove2groove.zip "https://onedrive.live.com/download?cid=8A0D502FC99C608F&resid=8A0D502FC99C608F%2118365&authkey=AHr0I_2k_AZ110E"
!unzip groove2groove.zip

# Clean MIDI subset (Complete)
# https://colinraffel.com/projects/lmd/
# https://github.com/craffel/midi-dataset
!wget --no-check-certificate -O clean_midi.zip "https://onedrive.live.com/download?cid=8A0D502FC99C608F&resid=8A0D502FC99C608F%2118368&authkey=AAFEzC5YBABk7rA"
!unzip clean_midi.zip

# Google Magenta Piano Transformer dataset (Complete)
# https://github.com/asigalov61/Google-Magenta-Piano-Transformer-Colab
!wget --no-check-certificate -O piano_transformer.zip "https://onedrive.live.com/download?cid=8A0D502FC99C608F&resid=8A0D502FC99C608F%2118369&authkey=AATJ2n_642HLGFI"
!unzip piano_transformer.zip

# Google MAESTRO Piano dataset (Complete)
# https://magenta.tensorflow.org/datasets/maestro
!wget --no-check-certificate -O MAESTRO.zip "https://onedrive.live.com/download?cid=8A0D502FC99C608F&resid=8A0D502FC99C608F%2118370&authkey=ABxzaWHKIeN1e3A"
!unzip MAESTRO.zip

# %cd /content/

#@title Load/Merge and parse the dataset

full_path_to_the_dataset = "/content/clean_midi.npy" #@param {type:"string"}
merge_several_datasets = False #@param {type:"boolean"}

print('Loading the dataset...Please wait...')
with open(full_path_to_the_dataset, 'rb') as filehandle:
  MusicDataset = pickle.load(filehandle)

if merge_several_datasets:
  print('Merging datasets...Please wait...')
  chords_list_f.extend(MusicDataset[0])
  melody_list_f.extend(MusicDataset[1])

else:
  chords_list_f = MusicDataset[0]
  melody_list_f = MusicDataset[1]

print('Parsing the dataset...Please wait...')
chords_notes_list = []
melody_notes_list = []

for chord in chords_list_f:
  chords_notes_list.append(chord[0][4])

for note in melody_list_f:
  melody_notes_list.append(note[4])

print('Done!')

print('Number of chords recorded:', len(chords_list_f))
print('The longest chord:', len(max(chords_list_f, key=len)), 'notes') 
print(max(chords_list_f, key=len))
print('Number of recorded melody events:', len(melody_list_f))
print('First melody event:', melody_list_f[0], 'Last Melody event:', melody_list_f[-1])
print('Total number of MIDI events recorded:', len(chords_list_f)+len(melody_list_f))
print('Dataset is loaded! Enjoy :)')

"""# If you are not sure where to start or what settings to select, please use original defaults"""

#@title Specify input MIDI file to search for
full_path_to_input_MIDI_file = "/content/tegridy-tools/tegridy-tools/seed.mid" #@param {type:"string"}
print('Loading the MIDI file...')
chords, melody = TMIDI.Tegridy_MIDI_Processor(full_path_to_input_MIDI_file, 
                                              -1, 
                                              1,
                                              )
print('MIDI file loaded. Enjoy :)')

#@title Initial Search
number_of_notes_to_match = 5 #@param {type:"slider", min:2, max:10, step:1}

output_song = []
pattern = []

print('Initial pattern search...')
print('Loading input notes...')

print('Input number of notes is', len(melody))
output_song.extend(melody)

for note in output_song[len(output_song)-number_of_notes_to_match:]:
  pattern.append(note[4])

#pattern = [69, 65, 66, 62, 63]

print('Starting search...')
print('Looking for pitches pattern', pattern)
pattern_start_index = [i for i in range(0,len(melody_notes_list)) if list(melody_notes_list[i:i+len(pattern)])==pattern]

if pattern_start_index == []:
  print('Nothing found')
else:
  print('Found matching notes at index', pattern_start_index[0])

#@title Re-Search

output_song = []
pattern = []

print('Pattern re-search...')

pidx = pattern_start_index[0]+number_of_notes_to_match

print('Loading input notes...')

print('Input number of notes is', len(melody))
output_song.extend(melody)

for note in output_song[len(output_song)-number_of_notes_to_match:]:
  pattern.append(note[4])

#pattern = [69, 65, 66, 62, 63]

print('Starting re-search...')
print('Looking for pitches pattern', pattern)
pattern_start_index = [i for i in range(pidx,len(melody_notes_list)) if list(melody_notes_list[i:i+len(pattern)])==pattern]

if pattern_start_index == []:
  print('Nothing found')
else:
  print('Found matching notes at index', pattern_start_index[0])

"""# Generate, download, and listen to the output"""

#@title Convert to MIDI
import MIDI

#@markdown Standard MIDI timings are 400/120(80)

number_of_ticks_per_quarter = 424 #@param {type:"slider", min:8, max:1000, step:8}
number_of_notes_to_play = 100 #@param {type:"slider", min:1, max:200, step:1}
simulate_velocity = True #@param {type:"boolean"}

output_song = []

for n in melody:
  n[5] = n[4]
  output_song.append(n)

output_s = melody_list_f[pattern_start_index[0]+number_of_notes_to_match:pattern_start_index[0]+number_of_notes_to_play]
time = output_song[-1][1]

for note in output_s:
  n = note
  n[1] = time
  if simulate_velocity:
    n[5] = note[4]
  output_song.append(n)
  time += note[2]

output_signature = 'MIDI Search'

output_header = [number_of_ticks_per_quarter, [['track_name', 0, bytes(output_signature, 'utf-8')]]] 

list_of_MIDI_patches = [0, 24, 32, 40, 42, 46, 56, 71, 73, 0, 0, 0, 0, 0, 0, 0]                                                  

patch_list = [['patch_change', 0, 0, list_of_MIDI_patches[0]], 
                ['patch_change', 0, 1, list_of_MIDI_patches[1]],
                ['patch_change', 0, 2, list_of_MIDI_patches[2]],
                ['patch_change', 0, 3, list_of_MIDI_patches[3]],
                ['patch_change', 0, 4, list_of_MIDI_patches[4]],
                ['patch_change', 0, 5, list_of_MIDI_patches[5]],
                ['patch_change', 0, 6, list_of_MIDI_patches[6]],
                ['patch_change', 0, 7, list_of_MIDI_patches[7]],
                ['patch_change', 0, 8, list_of_MIDI_patches[8]],
                ['patch_change', 0, 9, list_of_MIDI_patches[9]],
                ['patch_change', 0, 10, list_of_MIDI_patches[10]],
                ['patch_change', 0, 11, list_of_MIDI_patches[11]],
                ['patch_change', 0, 12, list_of_MIDI_patches[12]],
                ['patch_change', 0, 13, list_of_MIDI_patches[13]],
                ['patch_change', 0, 14, list_of_MIDI_patches[14]],
                ['patch_change', 0, 15, list_of_MIDI_patches[15]],
                ['track_name', 0, bytes('Composition Track', 'utf-8')]]


output = output_header + [patch_list + output_song]

midi_data = MIDI.score2midi(output)
detailed_MIDI_stats = MIDI.score2stats(output)

with open('MIDI_Search' + '.mid', 'wb') as midi_file:
    midi_file.write(midi_data)
    midi_file.close()
print('Done!')

from google.colab import files
files.download('MIDI_Search' + '.mid')
print('Detailed MIDI stats:')
detailed_MIDI_stats

#@title Listen to the last generated composition
#@markdown NOTE: May be very slow with the long compositions
print('Synthesizing the last output MIDI. Please stand-by... ')
FluidSynth("/usr/share/sounds/sf2/FluidR3_GM.sf2", 16000).midi_to_audio(str('MIDI_Search' + '.mid'), str('MIDI_Search' + '.wav'))
Audio(str('MIDI_Search' + '.wav'), rate=16000)

"""## Congrats! :) You did it :)"""