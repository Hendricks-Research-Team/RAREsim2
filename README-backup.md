# Raresim

[![PyPI version](https://badge.fury.io/py/raresim.svg)](https://badge.fury.io/py/raresim)
[![Python Version](https://img.shields.io/pypi/pyversions/raresim.svg)](https://pypi.org/project/raresim/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Python Interface for Scalable rare-variant simulations.

## Table Of Contents
- [Installation Steps](#to-install)
- [Usage](#usage)
  - [Convert haplotype files to a sparse matrix](#convert-haplotype-files-to-a-sparse-matrix)
  - [Extract haplotype subset](#extract-haplotype-subset)
  - [Simulate new allele frequencies](#simulate-new-allele-frequencies)
  - [Simulations that consider variant affect](#simulations-that-consider-variant-affect-functionalsynonymous)
  - [Prune only one type of variant](#prune-only-one-type-of-variant)
  - [Prune by given probabilities](#prune-by-given-probabilities)
  - [Prune with protected variants](#prune-with-protected-variants)
- [Running C Code](#running-c-code)
  - [Build](#build)
  - [Run](#run)
- [Running converted RAREsim python scripts](#running-converted-raresim-python-scripts)
  - [afs](#afs)
  - [nvariants](#nvariants)
  - [Expected variants](#expected-variants)

## Installation

### From PyPI
```bash
pip install raresim
```

### From TestPyPI (for testing pre-releases)
```bash
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ raresim
```

### From Source
```bash
git clone https://github.com/yourusername/raresim.git
cd raresim
pip install -e .  # Install in development mode
```

## Usage

### Command Line Interface

RareSim provides a command-line interface with several subcommands. Get help with:

```bash
raresim --help
```

### Convert haplotype files to a sparse matrix

```bash
raresim convert \
    -i path/to/input.haps.gz \
    -o output.sm
```

Options:
- `-i, --input-file`: Input haplotype file path (required)
- `-o, --output-file`: Output sparse matrix path (required)

### Extract haplotype subset

```bash
raresim extract \
    -i input.haps \
    -o output_subset.haps \
    -n 20 \
    --seed 123
```

Options:
- `-i, --input-file`: Input haplotype file path (required)
- `-o, --output-file`: Output haplotype subset file path (required)
- `-n, --num`: Number of haplotypes to extract (required)
- `--seed`: Random seed for reproducibility (optional)

### Simulate new allele frequencies

```bash
raresim sim \
    -m input_matrix.sm \
    -b expected_bins.txt \
    -l input.legend \
    -L output.legend \
    -H output.hap.gz
```

Options:
- `-m, --sparse-matrix`: Input sparse matrix path (required)
- `-b, --exp-bins`: Input expected bin sizes (required)
- `-l, --input-legend`: Input variant site legend (required)
- `-L, --output-legend`: Output variant site legend (required)
- `-H, --output-hap`: Output compressed hap file (required)
- `-z, --remove-zeros`: Remove rows of zeros and pruned rows
- `--prob`: Prune rows allele by allele with probability of removal
- `--small-sample`: Allow simulation of small sample sizes
- `--keep-protected`: Keep variants marked as protected in the legend
- `--stop-threshold`: Pruning stop threshold (default: 20)
- `--activation-threshold`: Pruning activation threshold (default: 10)
- `--verbose`: Enable verbose output

Input allele frequency distribution:
(1, 1, 20.0) 9
(2, 2, 10.0) 5
(3, 5, 5.0) 6
(6, 10, 5.0) 7
(11, 20, 1.0) 11
(21, 1000, 0.0) 48

New allele frequency distribution:
(1, 1, 20.0) 15
(2, 2, 10.0) 11
(3, 5, 5.0) 6
(6, 10, 5.0) 3
(11, 20, 1.0) 1
(21, 1000, 0.0) 0

Writing new variant legend

Writing new haplotype file............

### Variant-aware simulations (functional/synonymous)

For simulations that consider variant impact:
1. The legend file must contain a column labeled 'fun' where:
   - Functional variants are marked as 'fun'
   - Synonymous variants are marked as 'syn'
2. Provide separate expected bin size files for functional and synonymous variants

```bash
# First convert the haplotype file
raresim convert \
    -i input_stratified.haps.gz \
    -o output_stratified.sm

# Then run the simulation with both functional and synonymous bins
raresim sim \
    -m output_stratified.sm \
    --functional-bins expected_functional.txt \
    --synonymous-bins expected_synonymous.txt \
    -l input.legend \
    -L output.legend \
    -H output.hap.gz
```

Additional options for variant-aware simulations:
- `--f-only`: Process only functional variants
- `--s-only`: Process only synonymous variants

Input allele frequency distribution:
Functional
[1,1]   610.213692400324    686
[2,2]   199.745137641156    351
[3,5]   185.434393821117    598
[6,10]  73.1664075520905    472
[11,20] 37.132127271035 432
[21,220]    34.4401706091422    768
[221,440]   1.98761248740743    10
[441, ]     30

Synonymous
[1,1]   215.389082675548    276
[2,2]   73.1166493377018    140
[3,5]   73.6972836211026    240
[6,10]  33.4315406970657    181
[11,20] 19.1432926816897    181
[21,220]    20.2848171294807    331
[221,440]   1.38678884898772    11
[441, ]     20

New allele frequency distribution:
Functional
[1,1]   610.213692400324    607
[2,2]   199.745137641156    217
[3,5]   185.434393821117    178
[6,10]  73.1664075520905    82
[11,20] 37.132127271035 40
[21,220]    34.4401706091422    41
[221,440]   1.98761248740743    1
[441, ]     30

Synonymous
[1,1]   215.389082675548    220
[2,2]   73.1166493377018    66
[3,5]   73.6972836211026    63
[6,10]  33.4315406970657    31
[11,20] 19.1432926816897    20
[21,220]    20.2848171294807    20
[221,440]   1.38678884898772    1
[441, ]     20

Writing new variant legend

Writing new haplotype file...........
```

### Prune only one type of variant

To process only functional variants:
```bash
raresim sim \
    -m input_stratified.sm \
    --f-only expected_functional.txt \
    -l input.legend \
    -L output.legend \
    -H output.hap.gz
```

To process only synonymous variants:
```bash
raresim sim \
    -m input_stratified.sm \
    --s-only expected_synonymous.txt \
    -l input.legend \
    -L output.legend \
    -H output.hap.gz
```

### Prune by given probabilities

Rows can be pruned allele by allele using probabilities specified in the legend file:

```bash
raresim sim \
    -m input_matrix.sm \
    -H output.hap.gz \
    -l input_with_probs.legend \
    --prob
```

**Note:** The legend file must include a column with pruning probabilities.

## Python API Example

```python
from raresim.common.sparse import SparseMatrix, SparseMatrixReader

def main():
    # Load a sparse matrix from a file
    reader = SparseMatrixReader()
    sparse_matrix = reader.loadSparseMatrix("input.haps.gz")
    
    # Get matrix dimensions
    print(f"Matrix dimensions: {sparse_matrix.num_rows()} rows x {sparse_matrix.num_cols()} columns")
    
    # Access matrix data
    for row in range(sparse_matrix.num_rows()):
        alts = [sparse_matrix.get(row, i) for i in range(sparse_matrix.row_num(row))]
        print(f"Row {row}: {alts}")
    
    # Write to a new file
    writer = SparseMatrixWriter()
    writer.writeToHapsFile(sparse_matrix, "output.haps")

if __name__ == "__main__":
    main()
```

### Prune with protected variants

To protect specific variants from pruning:
1. Add a column called "protected" to your legend file
2. Mark rows with 1 to protect them (0 means they can be pruned)

```bash
raresim sim \
    -m input_matrix.sm \
    -H output.hap.gz \
    -l protected.legend \
    --keep-protected \
    -b expected_bins.txt \
    --small-sample \
    -L output.legend
```

**Note:** Protected variants are still counted in the allele frequency distribution but won't be pruned.
## Advanced Usage

### Running the C Implementation

For maximum performance, you can use the C implementation:

1. **Build the C code**:
   ```bash
   cd lib/raresim/src/
   make
   ```

2. **Run the C implementation**:
   ```bash
   # Decompress input file if needed
   gunzip -k input.haps.gz
   
   # Run the C program
   ./read \
       -i input.haps \
       -o output.haps.dat
   ```

**Note:** The Python package provides a more user-friendly interface and is recommended for most use cases.
## RAREsim Python Module

The package includes Python implementations of RAREsim's core functionality:

### Available Population Codes
- `EAS`: East Asian
- `AFR`: African
- `NFE`: Non-Finnish European
- `SAS`: South Asian

### Calculate Allele Frequency Spectrum (AFS)

```bash
raresim calc \
    --pop EAS \
    --mac mac_bins.csv \
    -o output_afs.txt
```

Or with custom parameters:
```bash
raresim calc \
    --alpha 1.5 \
    --beta -0.25 \
    -b 0.25 \
    --mac mac_bins.csv \
    -o output_afs.txt
```

### Calculate Expected Number of Variants

```bash
raresim calc \
    --pop AFR \
    -N 15000
```

With custom parameters:
```bash
raresim calc \
    --omega 0.15 \
    --phi 0.65 \
    -N 15000
```

### Calculate Expected Variants per Bin

```bash
raresim calc \
    -N 10000 \
    --props afs_output.txt \
    -o expected_variants.txt
```

## Contributing

Contributions are welcome! Please see our [Contributing Guidelines](CONTRIBUTING.md) for more information.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.