This project is designed to generate a number of distinctive animations on
a grid of LEDs via OPC, to a FadeCandy board.

If you're not already familiar, go check out
https://github.com/scanlime/fadecandy for more background on this project.

The code has been run on OSX with Python 2.7, and the only extra you'll need
is numpy to support fastopc and array math. Typically you'd run something
like:

    # pip install -r requirements.txt

as the super user to install. On the off-chance that the installation gets
a hiccup, numpy is pretty well documented and you should be able to figure
it out.

To get started, update dpyinfo.py to suit your display configuration, start
the OPC service and connect your array. Then run:

    % python art.py

You can also pick a specific subset to render by listing the particular
modules in the art directory, for example:

    % python art.py rain.py fortune.py

If you don't have a display handy, then that's okay. The default output is
to the controlling tty, so even if you're just checking this stuff out
or on the road, then you can still get an idea of the animations. The code
will auto-detect whether the terminal supports color and use it if it can.

Be aware that the down-sampled image is super lossy, since it's reducing
24 bit color to a handful of ascii-art characters... or - even better - if
your tty has a 256 color mode, then things will look quite a bit better.
Also, don't be too adventurous in trying to render to areas larger than the
tty, as curses will choke. In this case, you'll see a message saying that
the terminal is too small. *The terminal needs to be three lines taller
than the matrix in order to work*.

Most textual logging is now delivered to art.log. If something doesn't
look right, then check in here for exceptions and other diagnostics.

The directories are:

    .               application directory
    ./art           contains classes for each of the animations.
                    You'll notice a template.py file for the bare
                    bones
    ./art/utils     helper modules shared between animations
    ./art/basecls   base classes that animations may derive from
    ./assets        files that are used by the animations
    ./opc           an extended interface for using OPC via python
    ./opc/utils     various utilities used by the framework

Check out the existing animations for use as examples, and please commit
back code that you create!


### Project Pictures

A random assortment of images documenting the development of the hardware
can be found on [Imgur](http://ak15199.imgur.com/all).

### Other People's Work

The opc code is taken from https://github.com/scanlime/fadecandy.

Hopefully attriibutions are correct, if you see one missing,
then please let me know and I'll fix.
