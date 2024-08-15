# How to generate the audio:

## Requeriments:
   - Python 3.x 
   - "numpy" and "scipy" modules:

     ```
     pip3 install numpy
     pip3 install scipy
     ```

## Before running the script

Modify the "Variables definition" section as you want:

- _add_parity_byte_

  - Set it to "True" if you want the audio hardware/emulator to print the solution when loaded.
  - Leave it "False" if you want to only allow the solution of memory exploration or waveform investigation.
- _clock_freq_ - Set the clock frequency, leave it at 3.5 Mhz if you want to mimic zx spectrum.
- _end_block_bytes_ - End of block bytes, leave it blank will cause out of memory in hardware/emulator.
- _flag_
  - The flag itself.
  - **Important** If you want to make the audio hardware/emulator compatible use max 10 characters.
- _sample_rate_ - Audio output sample rate
- _start_tone_freq_ - Start tone frequency in hz.

## Run the Script:

```
python3 audio_generator.py
```

Give it a nice presentation and enjoy!
