"""
Search functionality for the Gemini archive of observations.

For questions, contact ooberdorf@gemini.edu
"""

from datetime import date

from astropy import units
from astropy.table import Table, MaskedColumn

from astroquery.gemini.urlhelper import URLHelper
import numpy as np

from ..query import BaseQuery
from ..utils.class_or_instance import class_or_instance
from . import conf

__all__ = ['Observations', 'ObservationsClass']  # specifies what to import


__valid_instruments__ = [
    'GMOS',
    'GMOS-N',
    'GMOS-S',
    'GNIRS',
    'GRACES',
    'NIRI',
    'NIFS',
    'GSAOI',
    'F2',
    'GPI',
    'NICI',
    'MICHELLE',
    'TRECS',
    'BHROS',
    'HRWFS',
    'OSCIR',
    'FLAMINGOS',
    'HOKUPAA+QUIRC',
    'PHOENIX',
    'TEXES',
    'ABU',
    'CIRPASS'
]


__valid_observation_class__ = [
    'science',
    'acq',
    'progCal',
    'dayCal',
    'partnerCal',
    'acqCal',
]

__valid_observation_types__ = [
    'OBJECT',
    'BIAS',
    'DARK',
    'FLAT',
    'ARC',
    'PINHOLE',
    'RONCHI',
    'CAL',
    'FRINGE',
    'MASK'
]

__valid_modes__ = [
    'imaging',
    'spectroscopy',
    'LS',
    'MOS',
    'IFS'
]

__valid_adaptive_optics__ = [
    'NOTAO',
    'AO',
    'NGS',
    'LGS'
]

__valid_raw_reduced__ = [
    'RAW',
    'PREPARED',
    'PROCESSED_BIAS',
    'PROCESSED_FLAT',
    'PROCESSED_FRINGE',
    'PROCESSED_ARC'
]


class ObservationsClass(BaseQuery):

    server = conf.server
    url_helper = URLHelper(server)

    def __init__(self, *args):
        """
        Query class for observations in the Gemini archive.

        This class provides query capabilities against the gemini archive.  Queries
        can be done by cone search, by name, or by a set of criteria.
        """
        super().__init__()

    @class_or_instance
    def query_region(self, coordinates, radius=0.3*units.deg):
        """
        search for Gemini observations by target on the sky.

        Given a sky position and radius, returns a `~astropy.table.Table` of Gemini observations.

        Parameters
        ----------
        coordinates : str or `~astropy.coordinates` object
            The target around which to search. It may be specified as a
            string or as the appropriate `~astropy.coordinates` object.
        radius : str or `~astropy.units.Quantity` object, optional
            Default 0.3 degrees.
            The string must be parsable by `~astropy.coordinates.Angle`. The
            appropriate `~astropy.units.Quantity` object from
            `~astropy.units` may also be used. Defaults to 0.3 deg.

        Returns
        -------
        response : `~astropy.table.Table`
        """
        return self.query_criteria(coordinates=coordinates, radius=radius)

    @class_or_instance
    def query_object(self, objectname, radius=0.3*units.deg):
        """
        search for Gemini observations by target on the sky.

        Given an object name and optional radius, returns a `~astropy.table.Table` of Gemini observations.

        Parameters
        ----------
        objectname : str
            The name of an object to search for.  This attempts to resolve the object
            by name and do a search on that area of the sky.  This does not handle
            moving targets.
        radius : str or `~astropy.units.Quantity` object, optional
            Default 0.3 degrees.
            The string must be parsable by `~astropy.coordinates.Angle`. The
            appropriate `~astropy.units.Quantity` object from
            `~astropy.units` may also be used. Defaults to 0.3 deg.

        Returns
        -------
        response : `~astropy.table.Table`
        """
        return self.query_criteria(objectname=objectname, radius=radius)

    @class_or_instance
    def query_criteria(self, coordinates=None, radius=0.3*units.deg, pi_name=None, program_id=None, utc_date=None,
                       instrument=None, observation_class=None, observation_type=None, mode=None,
                       adaptive_optics=None, program_text=None, objectname=None, raw_reduced=None):
        """
        search a variety of known parameters against the Gemini observations.

        Given various criteria, search the Gemini archive for matching observations.

        Parameters
        ----------
        coordinates : str or `~astropy.coordinates` object
            The target around which to search. It may be specified as a
            string or as the appropriate `~astropy.coordinates` object.
        radius : str or `~astropy.units.Quantity` object, optional
            Default 0.3 degrees.
            The string must be parsable by `~astropy.coordinates.Angle`. The
            appropriate `~astropy.units.Quantity` object from
            `~astropy.units` may also be used. Defaults to 0.3 deg.
        pi_name : str, optional
            Default None.
            Can be used to search for data by the PI's name.
        program_id : str, optional
            Default None.
            Can be used to match on program ID
        utc_date : date or (date,date) tuple, optional
            Default None.
            Can be used to search for observations on a particular day or range of days (inclusive).
        instrument : str, optional
            Can be used to search for a particular instrument.  Valid values are:
                'GMOS',
                'GMOS-N',
                'GMOS-S',
                'GNIRS',
                'GRACES',
                'NIRI',
                'NIFS',
                'GSAOI',
                'F2',
                'GPI',
                'NICI',
                'MICHELLE',
                'TRECS',
                'BHROS',
                'HRWFS',
                'OSCIR',
                'FLAMINGOS',
                'HOKUPAA+QUIRC',
                'PHOENIX',
                'TEXES',
                'ABU',
                'CIRPASS'
        observation_class : str, optional
            Specifies the class of observations to search for.  Valid values are:
                'science',
                'acq',
                'progCal',
                'dayCal',
                'partnerCal',
                'acqCal'
        observation_type : str, optional
            Search for a particular type of observation.  Valid values are:
                'OBJECT',
                'BIAS',
                'DARK',
                'FLAT',
                'ARC',
                'PINHOLE',
                'RONCHI',
                'CAL',
                'FRINGE',
                'MASK'
        mode : str, optional
            The mode of the observation.  Valid values are:
                'imaging',
                'spectroscopy',
                'LS',
                'MOS',
                'IFS'
        adaptive_optics : str, optional
            Specify the presence of adaptive optics.  Valid values are:
                'NOTAO',
                'AO',
                'NGS',
                'LGS'
        program_text : str, optional
            Specify text in the information about the program.  This is free form text.
        objectname : str, optional
            Give the name of the target.
        raw_reduced : str, optional
            Indicate the raw or reduced status of the observations to search for.  Valid values are:
                'RAW',
                'PREPARED',
                'PROCESSED_BIAS',
                'PROCESSED_FLAT',
                'PROCESSED_FRINGE',
                'PROCESSED_ARC'

        Returns
        -------
        response : `~astropy.table.Table`
        """

        # Build parameters into raw query
        #
        # This consists of a set of unnamed arguments, args, and key/value pairs, kwargs
        args = list()
        kwargs = dict()

        if radius is not None:
            kwargs["radius"] = radius
        if coordinates is not None:
            kwargs["coordinates"] = coordinates
        if pi_name is not None:
            kwargs["PIname"] = pi_name
        if program_id is not None:
            kwargs["progid"] = program_id.upper()
        if utc_date is not None:
            if isinstance(utc_date, date):
                args.append(utc_date.strftime("YYYYMMdd"))
            elif isinstance(utc_date, tuple):
                if len(utc_date) != 2:
                    raise ValueError("utc_date tuple should have two values")
                if not isinstance(utc_date[0], date) or not isinstance(utc_date[1], date):
                    raise ValueError("utc_date tuple should have date values in it")
                args.append("%s-%s" % utc_date[0].strftime("YYYYMMdd"), utc_date[1].strftime("YYYYMMdd"))
        if instrument is not None:
            if instrument.upper() not in __valid_instruments__:
                raise ValueError("Unrecognized instrument: %s" % instrument)
            args.append(instrument)
        if observation_class is not None:
            if observation_class not in __valid_observation_class__:
                raise ValueError("Unrecognized observation class: %s" % observation_class)
            args.append(observation_class)
        if observation_type is not None:
            if observation_type not in __valid_observation_types__:
                raise ValueError("Unrecognized observation type: %s" % observation_type)
            args.append(observation_type)
        if mode is not None:
            if mode not in __valid_modes__:
                raise ValueError("Unrecognized mode: %s" % mode)
            args.append(mode)
        if adaptive_optics is not None:
            if adaptive_optics not in __valid_adaptive_optics__:
                raise ValueError("Unrecognized adaptive optics: %s" % adaptive_optics)
            args.append(adaptive_optics)
        if program_text is not None:
            kwargs["ProgramText"] = program_text
        if objectname is not None:
            kwargs["object"] = objectname
        if raw_reduced is not None:
            if raw_reduced not in __valid_raw_reduced__:
                raise ValueError("Unrecognized raw/reduced setting: %s" % raw_reduced)
            args.append(raw_reduced)

        return self.query_raw(*args, **kwargs)

    @class_or_instance
    def query_raw(self, *args, **kwargs):
        """
        perform flexible query against Gemini observations

        This is a more flexible query method.  This method will do special handling for
        coordinates and radius if present in kwargs.  However, for the remaining arguments
        it assumes all of args are useable as query path elements.  For kwargs, it assumes
        all of the elements can be passed as name=value within the query path to Gemini.

        This method does not do any validation checking or attempt to interperet the
        values being passed, aside from coordinates and radius.

        This method is most useful when the query_criteria and query_region do not
        meet your needs and you can build the appropriate search in the website.  When
        you see the URL that is generated by the archive, you can translate that into
        an equivalent python call with this method.  For example, if the URL in the
        website is:

        https://archive.gemini.edu/searchform/RAW/cols=CTOWEQ/notengineering/GMOS-N/PIname=Hirst/NotFail

        You can disregard NotFail, cols=x and notengineering.  You would run this query as

        query_raw('GMOS-N', PIname='Hirst')

        Parameters
        ----------
        args :
            The list of parameters to be passed via the query path to the webserver
        kwargs :
            The dictionary of parameters to be passed by name=value within the query
            path to the webserver

        Returns
        -------
        response : `~astropy.table.Table`
        """
        url = self.url_helper.build_url(*args, **kwargs)

        response = self._request(method="GET", url=url, data={}, timeout=180, cache=False)

        js = response.json()
        return _gemini_json_to_table(js)


def _gemini_json_to_table(json):
    """
    takes a JSON object as returned from the Gemini archive webserver and turns it into an `~astropy.table.Table`

    Parameters
    ----------
    json : dict
        A JSON object from the Gemini archive webserver

    Returns
    -------
    response : `~astropy.table.Table`
    """

    data_table = Table(masked=True)

    for key in __keys__:
        col_data = np.array([obj.get(key, None) for obj in json])

        atype = str

        col_mask = np.equal(col_data, None)
        data_table.add_column(MaskedColumn(col_data.astype(atype), name=key, mask=col_mask))

    return data_table


__keys__ = ["exposure_time",
        "detector_roi_setting",
        "detector_welldepth_setting",
        "telescope",
        "mdready",
        "requested_bg",
        "engineering",
        "cass_rotator_pa",
        "ut_datetime",
        "file_size",
        "types",
        "requested_wv",
        "detector_readspeed_setting",
        "size",
        "laser_guide_star",
        "observation_id",
        "science_verification",
        "raw_cc",
        "filename",
        "instrument",
        "reduction",
        "camera",
        "ra",
        "detector_binning",
        "lastmod",
        "wavelength_band",
        "data_size",
        "mode",
        "raw_iq",
        "airmass",
        "elevation",
        "data_label",
        "requested_iq",
        "object",
        "requested_cc",
        "program_id",
        "file_md5",
        "central_wavelength",
        "raw_wv",
        "compressed",
        "filter_name",
        "detector_gain_setting",
        "path",
        "observation_class",
        "qa_state",
        "observation_type",
        "calibration_program",
        "md5",
        "adaptive_optics",
        "name",
        "focal_plane_mask",
        "data_md5",
        "raw_bg",
        "disperser",
        "wavefront_sensor",
        "gcal_lamp",
        "detector_readmode_setting",
        "phot_standard",
        "local_time",
        "spectroscopy",
        "azimuth",
        "release",
        "dec"]

Observations = ObservationsClass()
