This project is designed to generate a number of distinctive animations on
a 16x16 grid of LEDs via OPC, to a FadeCandy board, and with just a few
exceptions the code will mostly work with other grid sizes as well

If you're not already familiar, go check out
https://github.com/scanlime/fadecandy for more background on this project.

The code has been run on OSX with Python 2.7 with just the standard
modules. Hopefully it works on other platforms, but your mileage may vary.

To get started, update dpyinfo.py to suit your configuration, start the OPC
service and connect your array. Then run:

    % python art.py

You can also pick a specific subset to render by listing the particular
modules in the art directory, for example:

    % python art.py rain.py fortune.py

If you don't have a display handy, then that's okay and you don't need to
make any modifications to dpyinfo.py. The default output is to the
controlling tty, so even if you're just checking this stuff out or on the
road, then you can still get an idea of the animations. The code will
auto-detect whether the terminal supports color and use it if it can.

Be aware that the down-sampled image is super lossy, since it's reducing
24 bit color to a handful of ascii-art characters. Also, don't be too
adventurous in trying to render to areas larger than the tty, as you'll
see curses choke.

Most textual output is now delivered to art.log. If something doesn't look
right, then check in here for exceptions and other diagnostics.

The directories are:

    .               application directory
    ./art           contains classes for each of the animationso
                    You'll notice a template.py file for the bare
                    bones
    ./art/utils     helper modules shared between animations
    ./assets        files that are used by the animations
    ./opc           an extended interface for using OPC via python

Check out the existing animations for use as examples, and please commit
back code that you create!

OTHER PEOPLE'S WORK
=====

Hopefully attriibutions are correct, if you see one missing,
then please let me know and I'll fix.

One specific that is not covered elsewhere:

opc/opc.py is taken from https://github.com/scanlime/fadecandy
and should be unchanged from the original.
