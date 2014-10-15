# Layouter

A simple library, using gdspy, to automate the generation of many similar designs with different parameters.

## Usage

Make sure you have git and gdspy installed. Then from bash do, for example,

    mkdir new_layout && cd new_layout
    git clone https://github.com/cdoolin/layouter.git
    cp layouter/example/make_chip.py .
    python make_chip.py

And to save the layout to `mylayout.gds`,

    python make_chip.py mylayout
