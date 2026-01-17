import wave
import math
import struct
import random
import os

def generate_beep(filename, frequency=440.0, duration=0.1, volume=0.5):
    sample_rate = 44100
    n_samples = int(sample_rate * duration)
    
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        
        for i in range(n_samples):
            t = float(i) / sample_rate
            # Simple Sine Wave
            value = int(volume * 32767.0 * math.sin(2.0 * math.pi * frequency * t))
            wav_file.writeframes(struct.pack('<h', value))

def generate_noise(filename, duration=0.3, volume=0.5):
    sample_rate = 44100
    n_samples = int(sample_rate * duration)
    
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        
        for i in range(n_samples):
            value = int(random.uniform(-1, 1) * volume * 32767.0)
            wav_file.writeframes(struct.pack('<h', value))

def generate_powerup(filename):
    sample_rate = 44100
    duration = 0.2
    n_samples = int(sample_rate * duration)
    
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        
        for i in range(n_samples):
            t = float(i) / sample_rate
            # Frequency slide up
            freq = 400.0 + (i / n_samples) * 600.0 
            value = int(0.5 * 32767.0 * math.sin(2.0 * math.pi * freq * t))
            wav_file.writeframes(struct.pack('<h', value))

# Ensure directory exists
if not os.path.exists('assets'):
    os.makedirs('assets')

generate_powerup('assets/coin.wav') # Good sound
generate_noise('assets/explosion.wav', duration=0.5) # Bad sound
generate_beep('assets/select.wav', frequency=660, duration=0.1) # Menu select

print("Sound assets generated in ./assets folder.")
