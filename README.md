Introduction
------------

This project is designed to generate a number of distinctive animations on
a grid of LEDs via OPC, to a FadeCandy board.

If you're not already familiar, go check out
https://github.com/scanlime/fadecandy for more background on this project.

Installation
------------

The code has been run on OSX with Python 2.7, and there are a few extras
you'll need before you can start. Typically you'd run something like:

    # pip install -r requirements.txt

as the super user to install. Or maybe - if you prefer - you'd install in
a virtualenv. On the off-chance that the installation gets a hiccup:

  - numpy is pretty well documented and you should be able to figure
    it out. Some distros have a natively installable package to use instead
    of the pip equivalent. If you ido install bug get crappy performance,
    then it may be that there are some ancillary packages missing which numpy
    relies on for optimum performance. Again, the numpy docs are pretty good.

  - Either Pillow or it's predecessor PIL should work just fine, just
    make sure that you have one or the other installed. Probably not both
    though.

Getting Started
---------------

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
24 bit color to a handful of ascii-art characters... although if your
tty has a 256 color mode, then things will look quite a bit better.
Also, don't be too adventurous in trying to render to areas larger than the
tty, as curses will choke. In this case, you'll see a message saying that
the terminal is too small. *The terminal needs to be three lines taller
than the matrix in order to work*.

Most textual logging is delivered to art.log. If something doesn't
look right, then check in this file for exceptions and other diagnostics.

It's also possible to limit number of cycles that art.py runs through,
adjust the duration that each art is displayed before moving on to the next,
or to switch on profiling. Run with `--help` for more information.

The directories are

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
 
Running from the Web
--------------------

If you don't have a physical display, or a suitable terminal, then it's
still possbile to see what's going on by looking at the animations as
a web page. For this, you'll need to run the bundled Flask app like this:

  % python webrop.py

You should then be able to go visit the web page at ``http://localhost:5000``

If course, this is using the bundled development web server that comes
with Flask. If you want to serve volumes of this stuff, then it'll be
better to run under a production web server.

Project Pictures
----------------

A random assortment of images documenting the development of the hardware
can be found on [Imgur](http://ak15199.imgur.com/all).

Other People's Work
-------------------

The opc code is taken from https://github.com/scanlime/fadecandy.

Hopefully attriibutions are correct, if you see one missing,
then please let me know and I'll fix.
