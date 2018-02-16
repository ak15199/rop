import pkgutil
from os.path import dirname


def driver(address):
    here = dirname(__file__)
    driver = address.split(":")[0]
    drivers = {name: loader for loader, name, ispkg in
               pkgutil.iter_modules([here]) if
               not ispkg}

    try:
        module = drivers[driver].find_module(driver).load_module(driver)
        return module
    except KeyError:
        driverlist = "\n  ".join(drivers.keys())
        message = "Can't find driver '%s'. Available drivers are:\n  %s\n"
        raise Exception(message % (driver, driverlist))
