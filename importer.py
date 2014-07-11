import inspect
from os import listdir
from os.path import isfile, join, abspath, dirname, sep


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
        print plugin+":",
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
                print desc
            else:
                print "[done]"

            plugins.append(obj)
        except Exception as e:
            print "import failed:", str(e)

    return plugins
