# CVPal-Config

# CVPal Manual
https://pichenettes.github.io/mutable-instruments-diy-archive/cvpal/manual/

# List USB Devices
system_profiler SPUSBDataType

# Web Sites for Various useful snippets
https://spotlightkid.github.io/python-rtmidi/index.html
https://courses.ideate.cmu.edu/16-375/f2021/text/code/midi-examples.html
https://pypi.org/project/pyscpi/

# GIT Commands
 git add -A *
 git commit -m "various changes"
 git push

# install Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# install libusb
brew install libusb

# put libusb into path
export DYLD_LIBRARY_PATH="/opt/homebrew/lib:$DYLD_LIBRARY_PATH"

ln -s /opt/homebrew/lib ~/lib

python3 -m pip install --upgrade pyscpi

python3 -m pip install python-rtmidi

python3 -m pip install pyusb

python3 -m pip install --upgrade pyserial
