# EMPHarvest

A True Random Number Generator built with an RP2040 microcontroller, harvesting entropy from electromagnetic noise, photon detection, and timing jitter.

## How It Works

EMPHarvest combines multiple independent physical entropy sources:

### Electromagnetic Antennas (E)

Two copper wires (10-20cm) connected to ADC pins act as broadband antennas. They capture ambient electromagnetic radiation: WiFi signals at 2.4GHz, Bluetooth, cellular networks, the 50/60Hz hum from power lines, harmonics from switching power supplies, and thermal noise from nearby electronics.

The ADC samples voltage on these wires at 12-bit resolution. The high bits (8-11) reflect quasi-DC average voltage. The low bits (0-3) contain the noise — fluctuations too fast and small to be coherent signals. This is pure chaos: the sum of thousands of uncorrelated sources.

Each antenna captures a different slice of the electromagnetic environment. XORing two independent noisy sources reduces bias — if one is 60% ones, the other compensates.

### Microsecond Timer Jitter (M)

The internal microsecond timer appears deterministic but is not perfectly so. Hardware interrupts, DMA transfers, clock domain crossings, and oscillator instability add jitter at the microsecond level.

This is not high entropy by itself, but it is free and uncorrelated with the other sources. Every call to micros() returns a value influenced by the exact state of the system at that instant.

### Photon Detection via LED (P)

An LED is a P-N junction. When forward biased, it emits photons. But it works in reverse too — when photons strike the junction, they generate electron-hole pairs through the photoelectric effect.

We read the digital state of the LED pin — HIGH or LOW depends on how much light is hitting the junction at that microsecond. Ambient light fluctuations, reflections, imperceptible 50/60Hz flicker from artificial lighting — all contribute randomness.

### Mixing and Whitening

Raw entropy from all sources is XOR-mixed together. XOR of independent bits tends toward 50/50 distribution even if individual sources are biased.

The mixed entropy feeds into SHA-256 for whitening. SHA-256 is a cryptographic hash that diffuses every input bit across all output bits. A single bit change in input flips approximately 50% of output bits unpredictably.

We use a 4:1 ratio — 128 bytes of raw entropy produce 32 bytes of output. This ensures that even if raw entropy is only 2 bits per byte, the output has full entropy.

## Hardware Requirements

- Any RP2040-based board (Raspberry Pi Pico, Waveshare RP2040 Zero, etc.)
- Two pieces of wire (10-20cm copper wire or jumper wires)
- One LED (any color, transparent or red works best)
- USB cable

## Wiring
```
Antenna 1 (10-20cm wire) ──── GP26 (ADC0)
Antenna 2 (10-20cm wire) ──── GP27 (ADC1)

LED Anode (long leg)  ──── GP2
LED Cathode (short leg) ──── GP3
```

No resistors needed. Antenna pins must be floating (no pull-up/pull-down). LED is used as a sensor, not an emitter — it will not visibly light up.

## Software Setup

### Arduino IDE

1. Add RP2040 board support

   Go to File, Preferences, Additional Boards Manager URLs and add:
```
   https://github.com/earlephilhower/arduino-pico/releases/download/global/package_rp2040_index.json
```

2. Install the board package

   Go to Tools, Board, Boards Manager, search for "Raspberry Pi Pico/RP2040" by Earle F. Philhower III, and install it.

3. Install SHA256 library

   Go to Sketch, Include Library, Manage Libraries, search for "Crypto" by Rhys Weatherley, and install it.

4. Select your board

   Go to Tools, Board, Raspberry Pi RP2040 Boards and select your board.

5. Upload the firmware

   Hold the BOOT button on your board, connect USB, release BOOT, click Upload.

### Python Client
```bash
pip install pyserial
```

## Usage

### Finding Your Serial Port

The device will appear as a serial port:
- Linux: /dev/ttyACM0, /dev/ttyACM1, etc.
- macOS: /dev/cu.usbmodem*
- Windows: COM3, COM4, etc.

On Linux, you may need to add your user to the dialout group:
```bash
sudo usermod -aG dialout $USER
```

Log out and back in for this to take effect.

### Serial Port Configuration

On Linux, if you experience issues with data stopping, configure the port:
```bash
stty -F /dev/ttyACM0 115200 raw -echo -hupcl
```

### Command Line Interface
```bash
# Generate 32 random bytes (hex)
./trng.py random 32

# Generate raw bytes to file
./trng.py raw 1000000 > random.bin

# Generate a random integer (64-bit default)
./trng.py int

# Generate a 256-bit integer
./trng.py int 256

# Generate a float between 0 and 1
./trng.py float

# Generate a number in a range
./trng.py range 1 100

# Roll a dice
./trng.py dice 6
./trng.py dice 20

# Flip a coin
./trng.py coin

# Continuous stream
./trng.py stream
```

### Specifying the Port
```bash
./trng.py --port /dev/ttyACM1 random 32
./trng.py -p COM3 random 32
```

### Python Library
```python
from trng import TRNG

trng = TRNG("/dev/ttyACM0")

# Get random bytes
data = trng.read(32)

# Get hex string  
hex_string = trng.read_hex(32)

# Get random integer
number = trng.read_int(128)

# Get float [0, 1)
f = trng.read_float()

# Get number in range
n = trng.read_range(1, 100)

trng.close()
```

## Testing

### Prerequisites
```bash
# Debian/Ubuntu
sudo apt install rng-tools dieharder

# Fedora
sudo dnf install rng-tools dieharder
```

### Run Tests
```bash
cd scripts

# Default 5MB test
./run_tests.sh

# Custom size (in bytes)
./run_tests.sh 20000000
```

### Expected Results

FIPS 140-2: Should pass over 99% of tests.

Dieharder: Most tests pass. Some tests (operm5, rank_32x32) may show WEAK with small sample sizes. Larger samples (20MB+) improve results.

## Performance

- Throughput: approximately 18 KB/s
- Time to generate 1MB: approximately 57 seconds
- Time to generate 5MB: approximately 5 minutes

## Troubleshooting

### Serial Port Permission Denied
```bash
sudo chmod 666 /dev/ttyACM0
```

Or permanently:
```bash
sudo usermod -aG dialout $USER
```

### Device Stops Streaming

Reset the serial port configuration:
```bash
stty -F /dev/ttyACM0 115200 raw -echo -hupcl
```

Or kill any processes holding the port:
```bash
sudo fuser -k /dev/ttyACM0
```

### Board Not Detected

1. Try a different USB cable (some are power-only)
2. Try a different USB port (avoid hubs)
3. Hold BOOT, connect USB, release BOOT to enter bootloader mode

## The Physics

### Electromagnetic Noise

The antennas act as receivers for all electromagnetic radiation in their environment. Maxwell's equations describe how changing electric and magnetic fields propagate as waves. Every electronic device, power line, and radio transmitter contributes to the electromagnetic soup that the antennas sample.

The ADC converts this analog chaos into digital values. At 12-bit resolution, the least significant bits represent voltage changes of less than 1 millivolt — small enough that thermal noise in the ADC itself contributes randomness.

### Photon Detection

When a photon with sufficient energy strikes the LED's semiconductor junction, it can excite an electron from the valence band to the conduction band, creating an electron-hole pair. This is the photoelectric effect that Einstein explained in 1905.

The rate of photon arrival follows Poisson statistics — inherently random. Even in constant lighting, the exact number of photons hitting the junction in any microsecond interval varies unpredictably.

### Timing Jitter

The RP2040 runs at 125MHz from a crystal oscillator. But no oscillator is perfect — thermal noise causes tiny frequency variations. Additionally, the exact timing of when code executes depends on cache hits, bus arbitration, and interrupt servicing. These effects accumulate into microsecond-level unpredictability.

### Why SHA-256

Even after mixing multiple entropy sources, subtle correlations may remain — patterns too weak for humans to detect but visible to statistical tests. SHA-256 performs 64 rounds of bit mixing, with each round using different constants and rotation amounts.

The avalanche effect ensures that similar inputs produce completely different outputs. Two inputs differing by one bit will have outputs differing by approximately 50% of bits, with no predictable pattern.

## Security Considerations

EMPHarvest is suitable for:
- Cryptographic key generation
- Nonces and initialization vectors
- Monte Carlo simulations
- Gaming and gambling applications
- Seeding pseudorandom number generators

For high-security applications, consider:
- Running the full dieharder test suite
- NIST SP 800-90B entropy assessment
- Combining with other entropy sources

## License

MIT
