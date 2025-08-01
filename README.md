## External Dependencies

This project requires the following command-line tools to be installed and accessible in your `PATH`:

- **[HMMER3](http://hmmer.org/)** – for sequence alignment and homology searches.  
- **[MAFFT](https://mafft.cbrc.jp/alignment/software/)** – for multiple sequence alignment.  
- **[mTAlign](https://github.com/biocompibens/mTAlign)** – for structural alignment of protein domains.

### Installation

#### Debian/Ubuntu:

```bash
sudo apt install hmmer mafft
# mTAlign is not in apt – install it manually:
git clone https://github.com/biocompibens/mTAlign.git
cd mTAlign
make
export PATH=$PWD:$PATH
```

#### Conda:

```bash
conda env create -f environment.yml
conda activate hmms-build
```
