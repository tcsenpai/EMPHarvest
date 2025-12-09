#!/bin/bash

SIZE=${1:-5000000}

echo "Collecting $SIZE bytes..."
python3 ../trng.py raw $SIZE > /tmp/trng_test.bin

echo "File size:"
ls -lh /tmp/trng_test.bin

echo ""
echo "FIPS 140-2..."
rngtest < /tmp/trng_test.bin || true

echo ""
echo "Dieharder birthdays..."
dieharder -d 0 -g 201 -f /tmp/trng_test.bin || echo "dieharder failed"

echo ""
echo "Dieharder operm5..."
dieharder -d 1 -g 201 -f /tmp/trng_test.bin || echo "dieharder failed"

echo ""
echo "Dieharder rank..."
dieharder -d 2 -g 201 -f /tmp/trng_test.bin || echo "dieharder failed"

echo ""
echo "Done."
