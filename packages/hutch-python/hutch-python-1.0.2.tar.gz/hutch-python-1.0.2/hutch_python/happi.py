import logging

import happi
import lightpath
from lightpath.config import beamlines
from happi.loader import load_devices

logger = logging.getLogger(__name__)


def get_happi_objs(db, hutch):
    """
    Get the relevant devices for ``hutch`` from ``db``.

    This depends on a JSON ``happi`` database stored somewhere in the file
    system and handles setting up the ``happi.Client`` and querying the data
    base for devices.

    Parameters
    ----------
    db: ``str``
        Path to database

    hutch: ``str``
        Name of hutch

    Returns
    -------
    objs: ``dict``
        A mapping from device name to device
    """
    # Load the happi Client
    client = happi.Client(path=db)
    containers = list()
    # Find upstream devices based on lightpath configuration
    beamline_conf = beamlines.get(hutch.upper())
    # Something strange is happening if there are no upstream devices
    if not beamline_conf:
        logger.warning("Unable to find lightpath for %s",
                       hutch.upper())
        beamline_conf = {}
    # Add the complete hutch beamline
    beamline_conf[hutch.upper()] = {}
    # Base beamline
    for beamline, conf in beamline_conf.items():
        # Assume we want hutch devices that are active and in the bounds
        # determined by the beamline configuration
        reqs = dict(beamline=beamline, active=True,
                    start=conf.get('start', 0),
                    end=conf.get('end', None))
        blc = client.search(**reqs)
        # Add the beamline containers to the complete list
        if blc:
            containers.extend(blc)
        else:
            logger.warning("No devices found in database for %s",
                           beamline.upper())
    # Instantiate the devices needed
    dev_namespace = load_devices(*containers, pprint=False)
    return dev_namespace.__dict__


def get_lightpath(db, hutch):
    """
    Create a lightpath from relevant ``happi`` objects.

    Parameters
    ----------
    db: ``str``
        Path to database

    hutch: ``str``
        Name of hutch

    Returns
    -------
    path: ``lightpath.BeamPath``
        Object that provides a convenient way to visualize all the devices
        that may block the beam on the way to the interaction point.
    """
    # Load the happi Client
    client = happi.Client(path=db)
    # Allow the lightpath module to create a path
    lc = lightpath.LightController(client, endstations=[hutch.upper()])
    # Return the BeamPath object created by the LightController
    return lc.beamlines[hutch.upper()]
