# Dark Stylesheet for QT5

the css and icons were inspired by https://github.com/ColinDuquesnoy/QDarkStyleSheet
which are Copyright (c) 2013-2018 Colin Duquesnoy

## Installation:

### From source:

    git clone https://gitlab.com/t-5/python3-qt5-t5darkstyle.git
    cd python3-qt5-t5darkstyle
    pip3 install .

### Debian Package:

I have a prebuilt debian package for this module.
Please refer to the page https://t-5.eu/hp/Software/Debian%20repository/ to setup the repo.
After the repo is setup you can install the package by issueing

    apt install python3-qt5-t5darkstyle

in a shell.


## Usage:

    from qt5_t5darkstyle import darkstyle_css
    widget.setstylesheet(darkstyle_css())

or set your own colors with:

    widget.setStylesheet(darkstyle_css(MY_COLORS_DICT))
