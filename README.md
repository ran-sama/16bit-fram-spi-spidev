# 16bit-fram-spi-spidev
  Write to and read from a 16bit FRAM or EEPROM with Python spidev over the SPI bus. 

Tested on FM25W256 with 256 Kibibit (aka 32 KiB or 32768 Byte):

http://www.cypress.com/file/41696/download

## Requirements

https://pypi.org/project/spidev/

```
pip install spidev
```
If pip gives you troubles you can put sudo -H in front of it, if you know what you are doing.


## Usage

Make sure to chmod +x your files, usage is trivial:

```
./fram256.py w < onefill32
./fram256.py r > empty_output.txt
./fram256.py w < mlems_eeprom.jpg
./fram256.py r > mlems_output.jpg
```
Currently only reading and writing exact 32768 Byte files is supported.
If you want to implement offset reading and writing you can copy code from me here:

https://github.com/ran-sama/16bit-eeprom-i2c-smbus2

## Benchmarks

```
ran@raspberrypi:~ $ time python3 fram3.py w <  mlems_fram.jpg

real    0m0.334s
user    0m0.137s
sys     0m0.187s
ran@raspberrypi:~ $ time python3 fram3.py r > fast_out.txt

real    0m0.852s
user    0m0.450s
sys     0m0.401s
ran@raspberrypi:~ $
```

Writing at 20MHz SPI speeds is even faster than with my dedicated CH341a programmer which takes about 600ms on my desktop. The poor reading performance might be caused by inefficient coding on my end in Python 3 itself. As long as it is below 1 second I see no reason to improve it yet.

This FRAM module (FM25W256) provides longer retention (151 years), more cycles (10^14) and unnoticeable (~90ns) write delays. Despite its name ferroelectric RAM is actually non-volatile. It will outlive any EEPROM and NAND based storage, the latter you'd find in SSDs or USB flash storage.


## Benefits

Due to usage of spidev this is insanely fast compared to i2c.

Writing and reading in 32 byte blocks is the key to make best use of the SPI bus.

## License

Licensed under the WTFPL license.
