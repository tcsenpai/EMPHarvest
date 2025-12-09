#!/usr/bin/env python3
"""
TRNG - True Random Number Generator
RP2040 + Antenna hardware entropy source
"""

import serial
import argparse
import sys
import atexit


class TRNG:
    def __init__(self, port: str = "/dev/ttyACM0", baud: int = 115200):
        self.port = port
        self.baud = baud

        import subprocess
        subprocess.run(
            ["stty", "-F", port, str(baud), "raw", "-echo", "-hupcl"],
            capture_output=True
        )

        self.ser = serial.Serial(port, baud, timeout=None)
        self.ser.reset_input_buffer()
        atexit.register(self.cleanup)
    
    def read(self, nbytes: int) -> bytes:
        """Legge n byte di entropia"""
        return self.ser.read(nbytes)
    
    def read_hex(self, nbytes: int) -> str:
        """Legge n byte e ritorna hex"""
        return self.read(nbytes).hex()
    
    def read_int(self, nbits: int = 64) -> int:
        """Legge un intero random di n bit"""
        nbytes = (nbits + 7) // 8
        data = self.read(nbytes)
        return int.from_bytes(data, 'big') & ((1 << nbits) - 1)
    
    def read_float(self) -> float:
        """Ritorna float random tra 0 e 1"""
        return self.read_int(53) / (2**53)
    
    def read_range(self, min_val: int, max_val: int) -> int:
        """Ritorna intero random nell'intervallo [min, max]"""
        range_size = max_val - min_val + 1
        bits_needed = range_size.bit_length()
        while True:
            val = self.read_int(bits_needed)
            if val < range_size:
                return min_val + val
    
    def cleanup(self):
        if self.ser and self.ser.is_open:
            self.ser.reset_input_buffer()
            self.ser.reset_output_buffer()
            self.ser.close()
            try:
                import subprocess
                subprocess.run(
                    ["stty", "-F", self.port, str(self.baud), "raw", "-echo"],
                    capture_output=True
                )
            except:
                pass
    
    def close(self):
        self.cleanup()


def main():
    parser = argparse.ArgumentParser(
        description="TRNG - Hardware Random Number Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Esempi:
  trng random 32              # 32 byte hex
  trng raw 1000 > file.bin    # 1000 byte binari
  trng int 128                # intero a 128 bit
  trng float                  # float [0,1)
  trng range 1 100            # dado 1-100
  trng dice 6                 # dado D6
  trng coin                   # testa o croce
  trng stream                 # stream continuo (ctrl+c per fermare)
        """
    )
    parser.add_argument("--port", "-p", default="/dev/ttyACM0", help="Porta seriale")
    parser.add_argument("--baud", "-b", type=int, default=115200, help="Baud rate")
    
    sub = parser.add_subparsers(dest="cmd", required=True)
    
    p = sub.add_parser("random", help="Byte random in hex")
    p.add_argument("bytes", type=int, default=32, nargs="?", help="Numero byte")
    
    p = sub.add_parser("raw", help="Byte random binari (per file/pipe)")
    p.add_argument("bytes", type=int, help="Numero byte")
    
    p = sub.add_parser("int", help="Intero random")
    p.add_argument("bits", type=int, default=64, nargs="?", help="Numero bit")
    
    sub.add_parser("float", help="Float random [0,1)")
    
    p = sub.add_parser("range", help="Intero in range [min,max]")
    p.add_argument("min", type=int)
    p.add_argument("max", type=int)
    
    p = sub.add_parser("dice", help="Tira un dado")
    p.add_argument("sides", type=int, default=6, nargs="?", help="Facce")
    
    sub.add_parser("coin", help="Testa o croce")
    
    p = sub.add_parser("stream", help="Stream continuo hex")
    p.add_argument("--chunk", type=int, default=32, help="Byte per riga")
    
    args = parser.parse_args()
    
    try:
        trng = TRNG(args.port, args.baud)
    except serial.SerialException as e:
        print(f"Errore: {e}", file=sys.stderr)
        sys.exit(1)
    
    try:
        if args.cmd == "random":
            print(trng.read_hex(args.bytes))
        
        elif args.cmd == "raw":
            sys.stdout.buffer.write(trng.read(args.bytes))
        
        elif args.cmd == "int":
            print(trng.read_int(args.bits))
        
        elif args.cmd == "float":
            print(trng.read_float())
        
        elif args.cmd == "range":
            print(trng.read_range(args.min, args.max))
        
        elif args.cmd == "dice":
            print(trng.read_range(1, args.sides))
        
        elif args.cmd == "coin":
            print("Testa" if trng.read_int(1) else "Croce")
        
        elif args.cmd == "stream":
            while True:
                print(trng.read_hex(args.chunk))
    
    except KeyboardInterrupt:
        pass
    finally:
        trng.close()


if __name__ == "__main__":
    main()
