❯ ./run_tests.sh 
Collecting 5000000 bytes...
File size:
-rw-r--r--. 1 tcsenpai tcsenpai 4.8M Dec  9 22:20 /tmp/trng_test.bin

FIPS 140-2...
rngtest 6.17
Copyright (c) 2004 by Henrique de Moraes Holschuh
This is free software; see the source for copying conditions.  There is NO warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

rngtest: starting FIPS tests...
rngtest: entropy source drained
rngtest: bits received from input: 40000000
rngtest: FIPS 140-2 successes: 1998
rngtest: FIPS 140-2 failures: 1
rngtest: FIPS 140-2(2001-10-10) Monobit: 0
rngtest: FIPS 140-2(2001-10-10) Poker: 0
rngtest: FIPS 140-2(2001-10-10) Runs: 1
rngtest: FIPS 140-2(2001-10-10) Long run: 0
rngtest: FIPS 140-2(2001-10-10) Continuous run: 0
rngtest: input channel speed: (min=1.552; avg=32.834; max=18.626)Gibits/s
rngtest: FIPS tests speed: (min=84.396; avg=270.453; max=298.023)Mibits/s
rngtest: Program run time: 142274 microseconds

Dieharder birthdays...
#=============================================================================#
#            dieharder version 3.31.1 Copyright 2003 Robert G. Brown          #
#=============================================================================#
   rng_name    |           filename             |rands/second|
 file_input_raw|              /tmp/trng_test.bin|  1.21e+08  |
#=============================================================================#
        test_name   |ntup| tsamples |psamples|  p-value |Assessment
#=============================================================================#
# The file file_input_raw was rewound 11 times
   diehard_birthdays|   0|       100|     100|0.15149076|  PASSED  

Dieharder operm5...
#=============================================================================#
#            dieharder version 3.31.1 Copyright 2003 Robert G. Brown          #
#=============================================================================#
   rng_name    |           filename             |rands/second|
 file_input_raw|              /tmp/trng_test.bin|  1.46e+08  |
#=============================================================================#
        test_name   |ntup| tsamples |psamples|  p-value |Assessment
#=============================================================================#
# The file file_input_raw was rewound 88 times
      diehard_operm5|   0|   1000000|     100|0.00024856|   WEAK   

Dieharder rank...
#=============================================================================#
#            dieharder version 3.31.1 Copyright 2003 Robert G. Brown          #
#=============================================================================#
   rng_name    |           filename             |rands/second|
 file_input_raw|              /tmp/trng_test.bin|  1.28e+08  |
#=============================================================================#
        test_name   |ntup| tsamples |psamples|  p-value |Assessment
#=============================================================================#
# The file file_input_raw was rewound 110 times
  diehard_rank_32x32|   0|     40000|     100|0.02561921|  PASSED  

Done.


