Introduction
------------

This project is designed to generate a number of distinctive animations on a
grid of LEDs via OPC, to a FadeCandy board.

If you're not already familiar, go check out
https://github.com/scanlime/fadecandy for more background on this project.

Here's a test picture of the plasma art running on a physical array:

![example](http://i.imgur.com/KlEZBC8m.jpg)

Installation
------------

The code has been run on OSX with Python 2.7 and Python 3.6. There are a few
extras you'll need before you can start. Typically you'd run something like:

    # pip install -r requirements.txt

Or maybe - if you prefer - you'd install in a `virtualenv`. On the off-chance
that the installation gets a hiccup:

  - `numpy` is pretty well documented and you should be able to figure it out.
    Some distros have a natively installable package to use instead of the pip
    equivalent. If you do install but get poor performance, then it may be that
    there are some ancillary packages missing which `numpy` relies on for
    optimum performance. Again, the `numpy` docs are pretty good.

  - Either `Pillow` or it's predecessor `PIL` should work just fine, although
    the former is preferred.

Getting Started
---------------

To get started and display on your terminal, make sure that the terminal is at least 35x35 and simply run:

    % python art.py

You can also pick a specific subset to render by listing the particular modules
in the art directory, for example:

    % python art.py rain.py fortune.py

Be aware that the down-sampled image when displaying to the terminal is super
lossy, since it's reducing 24 bit color to a handful of ascii-art characters...
although if your tty has a 256 color mode, then things will look quite a bit
better than 16 colors. 

If you want higher quality output and can run against a physical LED display,
then update `config.py` to suit your display configuration, and start the OPC
service as appropriate.

The `config.py` file contains tunable parameters relating to the display, such
as geometry, as well as configuration options specific to the individual art
files.

Most textual logging is delivered to `art.log`. If something doesn't look
right, then check in this file for exceptions and other diagnostics.

It's also possible to limit number of cycles that `art.py` runs through, adjust
the duration that each art is displayed before moving on to the next, or to
switch on profiling. Run with `--help` for more information.

The directories are

    .                  application directory
    ./art              contains classes for each of the animations.
                       You'll notice a template.py file for the bare
                       bones
    ./art/utils        helper modules shared between animations
    ./art/baseclasses  base classes that animations may derive from
    ./assets           files that are used by the animations
    ./config.py        various configuration options
    ./opc              an extended interface for using OPC via python
    ./opc/utils        various utilities used by the framework

To help get up to speed on the library, you can use `pydoc`. For example:

  % pydoc opc.matrix

Check out the existing animations for use as examples, and please commit back
code that you create!

Running from the Web
--------------------

If you don't have a physical display, or a suitable terminal, then it's still
possible to see what's going on by looking at the animations as a web page. For
this, you'll need to run the bundled `Flask` app like this:

  % python webrop.py

You should then be able to go visit the web page at ``http://localhost:5000``

If course, this is using the bundled development web server that comes with
`Flask`. If you want to serve volumes of this stuff, then it'll be better to
run under a production web server.

Webrop is not generally maintained, so your mileage may vary.

Project Pictures
----------------

A random assortment of images documenting the development of the hardware can
be found on [Imgur](http://ak15199.imgur.com/all).

Other People's Work
-------------------

The opc code is taken from https://github.com/scanlime/fadecandy.

Hopefully attributions are correct. If you see one missing, then please let me
know and I'll fix.

Contributing
------------

There aren't any formal guidelines for contributing. If you'd like to submit
a pull request for review, or open an issue, though, then that's awesome.
