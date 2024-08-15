import numpy as np
from scipy import signal
import scipy.io.wavfile

# **************************************
# Variables definition:
# **************************************

add_parity_byte = True                  # Set to True if you want the audio to be compatible with hardware/emulator
clock_freq = 3500000                    # 3.5 Mhz to mimic zx spectrum
end_block_bytes = "01111110 00000000"   # End of block bytes, leave it blank will cause out of memory in hardware/emulator
flag = "<<flag>>"                       # Important, max 10 characters
sample_rate = 44100                     # Audio output sample rate
start_tone_freq = 807                   # In hz

# **************************************
# Create signals to use:
# **************************************

# Start tone - 807 Hz:
vector_time = np.linspace(0,1/start_tone_freq,int(sample_rate*1/start_tone_freq),endpoint=False)
start_tone = -1*signal.square(2 * np.pi * start_tone_freq * vector_time)

# Bit 0 - 855 t-states:
freq = 1/(1/clock_freq*2*855)
vector_time = np.linspace(0,1/freq,int(sample_rate*1/freq),endpoint=False)
bit_0 = -1*signal.square(2 * np.pi * freq * vector_time)

# Bit 1 - 1710 t-states:
freq = 1/(1/clock_freq*2*1710)
vector_time = np.linspace(0,1/freq,int(sample_rate*1/freq),endpoint=False)
bit_1 = -1*signal.square(2 * np.pi * freq * vector_time)

# **************************************
# Create audio
# **************************************

# Add start tone for 2 seconds, it needs to be more than 1 second:
output_audio = start_tone
for x in range(start_tone_freq*2):
    output_audio = np.append(output_audio,start_tone)

# Add sync signal:
output_audio = np.append(output_audio,bit_0)

# Add headers:
for x in range(16):
    output_audio = np.append(output_audio,bit_0)

# Add program name, in this case, the flag:
binary_flag = "".join(f"{ord(i):08b}" for i in flag)
for i in binary_flag:
    if i == "0":
        output_audio = np.append(output_audio,bit_0)
    else:
        output_audio = np.append(output_audio,bit_1)

# Add rest of program name, in case not 10 characters used in flag:
extra_characters = ""
blank_characters = 10 - len(flag)
while blank_characters > 0:
    blank_characters = blank_characters - 1
    extra_characters = extra_characters + "00100000"

for i in extra_characters:
    if i == "0":
        output_audio = np.append(output_audio,bit_0)
    elif i == "1":
        output_audio = np.append(output_audio,bit_1)

# Add end of block data:
for i in end_block_bytes:
    if i == "0":
        output_audio = np.append(output_audio,bit_0)
    elif i == "1":
        output_audio = np.append(output_audio,bit_1)

# Add parity byte - 8 bit XOR:
if add_parity_byte:
    all_binary_data = binary_flag+extra_characters+end_block_bytes.replace(" ", "")
    parity_byte = ""

    for i in range(8):
        parity_bit = "0"
        for j in range(int(len(all_binary_data)/8)):
            next_bit_to_compare = all_binary_data[j*8+i]
            parity_bit = str(int(parity_bit) ^ int(next_bit_to_compare))  # XOR operation
        parity_byte = parity_byte + parity_bit

    for i in parity_byte:
        if i == "0":
            output_audio = np.append(output_audio,bit_0)
        elif i == "1":
            output_audio = np.append(output_audio,bit_1)

# Create audio file:
archivo_audio = scipy.io.wavfile.write("zxsound.wav", sample_rate, output_audio.astype(np.float32))
