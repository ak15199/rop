import inspect
from os import listdir
from os.path import isfile, join, abspath, dirname, sep
import logging


def moduleQualifies(dir, file, excludes, includes):
    return isfile(join(dir, file))                  \
         and file.endswith(".py")                   \
         and file not in excludes                   \
         and (file in includes or len(includes) == 0)


def getPluginList(plugindir, excludes, includes):
    basedir = dirname(abspath(inspect.getsourcefile(lambda _: None)))
    dir = basedir + sep + plugindir
    return [f[:-3]
            for f in listdir(dir)
            if moduleQualifies(dir, f, excludes, includes)]


def ImportPlugins(dir, excludes, includes, args):
    plugins = []
    excludes.append("__init__.py")

    for plugin in getPluginList(dir, excludes, includes):
        try:
            module = __import__(
                dir+'.'+plugin,
                globals(),
                locals(),
                ["Art"],
                -1)
            obj = module.Art(args)

            desc = getattr(obj, "description", None)
            if desc is not None:
                logging.info("%s: %s"%(plugin, desc))
            else:
                logging.info("%s: [None]"%(plugin))

            plugins.append(obj)
        except Exception as e:
            logging.error("%s: import failed: %s"%(plugin, str(e)))

    return plugins
