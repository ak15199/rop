This project is designed to generate a number of distinctive animations on
a 16x16 grid of LEDs via OPC, to a FadeCandy board, although - with a
couple of exceptions - the code will mostly work with other grid sizes as
well

The code has been run on OSX with Python 2.7. Hopefully it works on other
platforms, but your mileage may vary slightly.

To get started, update dpyinfo.py to suit your configuration and connect
your OPC array. Then run:

    % python art.py

You can also pick a specific subset to render by listing the particular
modules in the art directory, for example:

    % python art.py rain.py fortune.py

If you don't have a display handy, then you don't need to make any
modifications to dpyinfo.py. The default output is to the controlling tty,
and so even if you're just running in software, or on the road, then you
can still get an idea of the animations. The default configuration assumes
that you have an ANSI compliant tty supporting basic color. However, if
that doesn't work, consider setting the line to read:

    ADDRESS='ansi-1'

in dpyinfo.py. This will eliminate the color control codes and may make the
image more legible. In both cases, the image is super lossy, since it's
reducing 24 bit color to ten distinct ascii-art characters.

The directories are:

    .               application directory
    ./art           contains classes for each of the animationso
                    You'll notice a template.py file for the bare
                    bones
    ./art/utils     helper modules shared between animations
    ./assets        files that are used by the animations
    ./opc           an extended interface for using OPC via python

Check out the existing animations for use as examples, and
please commit back code that you create!


OTHER PEOPLE'S WORK
=====

Hopefully attriibutions are correct, if you see one missing,
then please let me know and I'll fix.

One specific that is not covered elsewhere:

opc/opc.py is taken from https://github.com/scanlime/fadecandy
and should be unchanged from the original.
