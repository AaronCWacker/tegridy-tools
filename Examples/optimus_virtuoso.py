# -*- coding: utf-8 -*-
"""Optimus_VIRTUOSO.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1pNtJXB2ltVD3rCXHcL6Wh9nTVLXgETC9

# Optimus VIRTUOSO (ver. 1.0)

## "Music never allows falsehoods for even the deaf hear flat notes!" ---OV

***

Credit for char-based GPT2 implementation used in this colab goes out to Andrej Karpathy: https://github.com/karpathy/minGPT

***

WARNING: This complete implementation is a functioning model of the Artificial Intelligence. Please excercise great humility, care, and respect.

***

#### Project Los Angeles

#### Tegridy Code 2021

***

# Setup Environment, clone needed repos, and install all required dependencies
"""

#@title nvidia-smi gpu check
!nvidia-smi

#@title Install all dependencies (run only once per session)

!git clone https://github.com/asigalov61/tegridy-tools
!apt install fluidsynth #Pip does not work for some reason. Only apt works
!pip install midi2audio

#@title Import all needed modules

print('Loading needed modules. Please wait...')
import os

if not os.path.exists('/content/Dataset'):
    os.makedirs('/content/Dataset')

os.chdir('/content/tegridy-tools/tegridy-tools')
import TMIDI

os.chdir('/content/tegridy-tools/tegridy-tools')
from minGPT import *

from midi2audio import FluidSynth
from IPython.display import display, Javascript, HTML, Audio

from google.colab import output, drive

os.chdir('/content/')
print('Loading complete. Enjoy! :)')

"""# Download and process MIDI dataset"""

# Commented out IPython magic to ensure Python compatibility.
#@title Download special Tegridy Piano MIDI dataset

#@markdown Works best stand-alone/as-is for the optimal results
# %cd /content/Dataset/

!wget 'https://github.com/asigalov61/Tegridy-MIDI-Dataset/raw/master/Tegridy-Piano-CC-BY-NC-SA.zip'
!unzip -j '/content/Dataset/Tegridy-Piano-CC-BY-NC-SA.zip'
!rm '/content/Dataset/Tegridy-Piano-CC-BY-NC-SA.zip'

# %cd /content/

"""# If you are not sure where to start or what settings to select, please use original defaults"""

#@title Process MIDIs to special MIDI dataset with Tegridy MIDI Processor
#@markdown NOTES:

#@markdown 1) Dataset MIDI file names are used as song names. Feel free to change it to anything you like.

#@markdown 2) Best results are achieved with the single-track, single-channel, single-instrument MIDI 0 files with plain English names (avoid special or sys/foreign chars)

#@markdown 3) MIDI Channel = -1 means all MIDI channels. MIDI Channel = 16 means all channels will be processed. Otherwise, only single indicated MIDI channel will be processed.

file_name_to_output_dataset_to = "/content/Optimus-Virtuoso-Music-Dataset" #@param {type:"string"}
desired_MIDI_channel_to_process = 0 #@param {type:"slider", min:-1, max:15, step:1}
melody_notes_in_chords = True #@param {type:"boolean"}
chars_encoding_offset = 32000 #@param {type:"number"}

print('TMIDI Processor')
print('Starting up...')

###########

average_note_pitch = 0
min_note = 127
max_note = 0

files_count = 0

ev = 0

chords_list_f = []
melody_list_f = []

chords_list = []
chords_count = 0

melody_chords = []
melody_count = 0

TXT_String = 'DATASET=Optimus-Virtuoso-Music-Dataset' + chr(10)

TXT = ''
melody = []
chords = []

###########

print('Loading MIDI files...')
print('This may take a while on a large dataset in particular.')

dataset_addr = "/content/Dataset/"
os.chdir(dataset_addr)
filez = os.listdir(dataset_addr)

print('Processing MIDI files. Please wait...')
for f in tqdm.auto.tqdm(filez):
  try:

    files_count += 1
    TXT, melody, chords = TMIDI.Optimus_MIDI_TXT_Processor(f, chordify_TXT=True, output_MIDI_channels=False, char_offset=chars_encoding_offset)
    melody_list_f += melody
    chords_list_f += chords
    TXT_String += TXT
    
  
  except:
    print('Bad MIDI:', f)
    continue

print('Task complete :)')
print('==================================================')
print('Number of processed dataset MIDI files:', files_count)
print('Number of MIDI chords recorded:', len(chords_list_f))
print('First chord event:', chords_list_f[0], 'Last chord event:', chords_list_f[-1]) 
print('Number of recorded melody events:', len(melody_list_f))
print('First melody event:', melody_list_f[0], 'Last Melody event:', melody_list_f[-1])
print('Total number of MIDI events recorded:', len(chords_list_f) + len(melody_list_f))

# Writing dataset to TXT file
with open(file_name_to_output_dataset_to + '.txt', 'wb') as f:
  f.write(TXT_String.encode('utf-8', 'replace'))
  f.close

# Dataset
MusicDataset = [chords_list_f, melody_list_f]

# Writing dataset to pickle file
TMIDI.Tegridy_Pickle_File_Writer(MusicDataset, file_name_to_output_dataset_to)

"""# Setup and Intialize the Model

## YOU MUST RUN THE CELL/CODE IN THE SECTION BELOW to init the model. Does not matter if the model is empty or pre-trained.

## DO NOT EXECUTE TRAIN CELL/CODE UNLESS YOU INTEND TO TRAIN FROM SCRATCH
"""

#@title Create/prepare GPT2 model and load the dataset

full_path_to_training_text_file = "/content/Optimus-Virtuoso-Music-Dataset.txt" #@param {type:"string"}
model_attention_span_in_tokens = 256 #@param {type:"slider", min:0, max:1024, step:16}
model_embed_size = 256 #@param {type:"slider", min:0, max:1024, step:64}
number_of_heads = 16 #@param {type:"slider", min:1, max:16, step:1}
number_of_layers = 16 #@param {type:"slider", min:1, max:16, step:1}
number_of_training_epochs = 3 #@param {type:"slider", min:1, max:5, step:1}
training_batch_size = 32 #@param {type:"slider", min:0, max:160, step:4}
model_learning_rate = 6e-4 #@param {type:"number"}
checkpoint_full_path = "" #@param {type:"string"}

trainer, model, train_dataset = MainLoader(full_path_to_training_text_file,
                                          None,
                                          16,
                                          model_attention_span_in_tokens,
                                          model_embed_size,
                                          number_of_heads,
                                          number_of_layers,
                                          number_of_training_epochs,
                                          training_batch_size,
                                          model_learning_rate,
                                          )

"""# Train the model or Load/Re-load the existing pre-trained model checkpoint"""

# Commented out IPython magic to ensure Python compatibility.
#@title (OPTION 1) Train the model
# %cd /content/
trainer.train()

#@title Plot Positional Embeddings

# visualize some of the learned positional embeddings, maybe they contain structure
PlotPositionalEmbeddings(model, model_attention_span_in_tokens)

# Commented out IPython magic to ensure Python compatibility.
#@title Save/Re-Save the model from memory
#@markdown Standard PyTorch AI models file extension is PTH
full_path_to_save_model_to = "/content/Optimus-Virtuoso-Trained-Model.pth" #@param {type:"string"}
# %cd /content/
torch.save(model, full_path_to_save_model_to)
#torch.save(model.state_dict(), full_path_to_save_model_to)

#@title (OPTION 2) Load existing model/checkpoint
full_path_to_model_checkpoint = "/content/Optimus-Virtuoso-Trained-Model.pth" #@param {type:"string"}
model = torch.load(full_path_to_model_checkpoint)
model.eval()

"""# Generate, download, plot, and listen to the output"""

#@title Generate and download the composition as TXT file.
#@markdown PLEASE NOTE IMPORTANT POINTS: 

#@markdown 0) If you are not sure where to start/what settings to set, please use original defaults.

#@markdown 1) Model primes from the dataset !!!

#@markdown 2) Model's first output may be empty or garbled so please try several times before discarting the model

#@markdown 3) You can now communicate to the model desired length of the output composition by suffixing input_prompt with number of chords.

#@markdown I.e. SONG=Relax_with_900_Chords

#@markdown 3) Coherence of GPT2 Models is inversly proportional to the length of the generated composition, so the best resutls are achieved with shorter compositions and/or continuation routines use

print('Optimus VIRTUOSO Model Generator')
print('Starting up...')
number_of_tokens_to_generate = 8192 #@param {type:"slider", min:0, max:32768, step:128}
creativity_temperature = 0.8 #@param {type:"slider", min:0.05, max:4, step:0.05}
top_k_prob = 48 #@param {type:"slider", min:0, max:50, step:1}
input_prompt = "SONG=Deep" #@param {type:"string"}

os.chdir('/content/')

completion = Generate(model,
                      train_dataset,
                      trainer,
                      number_of_tokens_to_generate,
                      creativity_temperature,
                      top_k_prob,
                      input_prompt)

# Stuff for datetime stamp
filename = '/content/Optimus-VIRTUOSO-Composition-' + 'generated-on-' 
fname = TMIDI.Tegridy_File_Time_Stamp(filename)

print('Done!')
print('Saving to', str(fname + '.txt'))
with open(fname + '.txt', "w") as text_file:
    print(completion, file=text_file)

print('Downloading TXT file...')
from google.colab import files
files.download(fname + '.txt')

#@title Convert to MIDI from TXT (w/Tegridy MIDI-TXT Processor)

#@markdown Standard MIDI timings are 400/120(80)

'''For debug:

fname = '/content/Optimus-Virtuoso-Music-Dataset.txt'
with open(fname, 'r') as f:
  completion = f.read()[:1500]
  completion'''


number_of_ticks_per_quarter = 420 #@param {type:"slider", min:10, max:500, step:10}
encoding_has_MIDI_channels = False #@param {type:"boolean"}
simulate_velocity = True #@param {type:"boolean"}
chars_encoding_offset_used_for_dataset = 32000 #@param {type:"number"}

print('Converting TXT to MIDI. Please wait...')
print('Converting TXT to Song...')
output_list, song_name = TMIDI.Tegridy_Optimus_TXT_to_Notes_Converter(completion, 
                                                                has_MIDI_channels=encoding_has_MIDI_channels, 
                                                                simulate_velocity=simulate_velocity,
                                                                char_encoding_offset=chars_encoding_offset_used_for_dataset)

print('Converting Song to MIDI...')

output_signature = 'Optimus VIRTUOSO'

detailed_stats = TMIDI.Tegridy_SONG_to_MIDI_Converter(output_list,
                                                      output_signature = output_signature,  
                                                      output_file_name = fname, 
                                                      track_name=song_name, 
                                                      number_of_ticks_per_quarter=number_of_ticks_per_quarter)

print('Done!')

print('Downloading your composition now...')
from google.colab import files
files.download(fname + '.mid')

print('Detailed MIDI stats:')
detailed_stats

#@title Listen to the last generated composition
#@markdown NOTE: May be very slow with the long compositions
print('Synthesizing the last output MIDI. Please stand-by... ')
FluidSynth("/usr/share/sounds/sf2/FluidR3_GM.sf2", 16000).midi_to_audio(str(fname + '.mid'), str(fname + '.wav'))
Audio(str(fname + '.wav'), rate=16000)

"""## Congrats! :) You did it :)"""