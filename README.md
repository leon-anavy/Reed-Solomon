# Reed-Solomon

This repo contains all code required for the encoding and decoding of the composite DNA based storage.
[doi of the manuscript on BioRxiv]

### General libaraies
Implementation for the necesarry Finite Fields, Polynomial arithmetics, and Reed-Solomon codecs.
This is adapted from the work of Andrew Brown <brownan@cs.duke.edu, brownan@gmail.com>

### Encoding and decoding pipelines

### General
#### composite_RS.py
A library containing the required combinations of the appropriate RS encoder and decoder for each of the composite alphabets used.

### Encoding
#### composite_encode.py
An encoding script that takes as an input the composite sequences (output of the fountain code) and the alphabet size (4,5 or 6) and returns the set of RS coded composite sequences.
#### generate_oligo_set.py
A script that takes as an input the RS-encoded seuqeunces and the number of desired output sequences and generate a final set of sequences randomly selected from the input set.

### Decoding
#### composite_decode.py
An decoding script that takes as an input the inffered sequences (generated from NGS reads) and the alphabet size (4,5 or 6) and returns the set of decoded composite sequences (that can serve as input to the fountain decoder)
## Authors

* **Leon Anavy** - *Initial work* - [leon-anavy](https://github.com/leon-anavy)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments
*  Andrew Brown <brownan@cs.duke.edu, brownan@gmail.com>
