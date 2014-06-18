This project is designed to generate a number of distinctive
animations on a 16x16 grid of LEDs via OPC, to a FadeCandy
board, although the code should mostly work with other grid
sizes too.

The code has been run on OSX with Python 2.7. Hopefully it
works on other platforms, but your mileage may vary slightly.

To get started, connect your OPC array, and run:

    % python art.py

You can also pick a specific subset to render by listing the 
particular modules in the art directory, for example:

    % python art.py rain.py fortune.py

If the display looks a bit wonky, you may need to modify
dpyinfo.py to suit your configuration.

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
----

Hopefully attriibutions are correct, if you see one missing,
then please let me know and I'll fix.

One specific that is not covered elsewhere:

opc/opc.py is taken from https://github.com/scanlime/fadecandy
and should be unchanged from the original.
