import rdflib as rdflib
from rdflib.namespace import Namespace
import logging
import time
import requests
from pip.utils import cached_property
from attrdict import AttrMap

logger = logging.getLogger(__name__)
SCHEMA_NS = Namespace('http://schema.org/')

# source: https://github.com/Princeton-CDH/viapy/blob/master/viapy/api.py
class ViafAPI(object):
    """Wrapper for VIAF API.
    https://platform.worldcat.org/api-explorer/apis/VIAF
    """

    #: base url for VIAF API methods
    api_base = "https://www.viaf.org/viaf"
    #: base url for VIAF URIs
    uri_base = "http://viaf.org/viaf"

    def search(self, query):
        """
        Query VIAF seach interface.  Returns a list of :class:`SRUItem`

        :param query: CQL query in viaf syntax (e.g., ``cql.any all "term"``)
        :type query: str

        """
        search_url = '%s/search' % self.api_base
        print('search_url="{}"'.format(search_url))
        params = {
            'query': query,
            'httpAccept': 'application/json',
            'maximumRecords': 5,  # TODO: configurable ?
            # sort by number of holdings (default sort on web search)
            # - so better known names show up first
            'sortKeys': 'holdingscount'
        }
        print('params="{}"'.format(params))

        response = requests.get(search_url, params=params)
        # logger.debug('search \'%s\': %s %s, %0.2f',
        #              params['query'], response.status_code, response.reason,
        #              response.elapsed.total_seconds())

        print('search \'{}\': {} {}, {:.2f} sec'.format(
            params['query'], response.status_code, response.reason, response.elapsed.total_seconds()))
        if response.status_code == requests.codes.ok:
            data = SRUResult(response.json())
            if data.total_results:
                return data.records

                # if response was not ok, raise the error


        response.raise_for_status()

    def _find_type(self, fltr, value):
        return self.search('%s all "%s"' % (fltr, value))

    def find_person(self, name):
        '''Search VIAF for local.personalNames'''
        return self._find_type('local.personalNames', name)

    def find_corporate(self, name):
        '''Search VIAF for local.corporateNames'''
        return self._find_type('local.corporateNames', name)

    def find_place(self, name):
        '''Search VIAF for local.geographicNames'''
        return self._find_type('local.geographicNames', name)


class ViafEntity(object):
    '''Object for working with a single VIAF entity.
    :param viaf_id: viaf identifier (either integer or uri)
    '''
    def __init__(self, viaf_id):
        try:
            int(viaf_id)
            self.uri = ViafAPI.uri_from_id(viaf_id)
        except ValueError:
            # NOTE: do we need to canonicalize the URI in any way to
            # ensure RDF queries work properly?
            self.uri = viaf_id

    @property
    def uriref(self):
        '''VIAF URI reference as instance of :class:`rdflib.URIRef`'''
        return rdflib.URIRef(self.uri)

    @cached_property
    def rdf(self):
        '''VIAF data for this entity as :class:`rdflib.Graph`'''
        start = time.time()
        graph = rdflib.Graph()
        graph.parse(self.uri)
        logger.debug('Loaded VIAF RDF %s: %0.2f sec',
                     self.uri, time.time() - start)
        return graph

    # person-specific properties

    @property
    def birthdate(self):
        '''schema birthdate as :class:`rdflib.Literal`'''
        return self.rdf.value(self.uriref, SCHEMA_NS.birthDate)

    @property
    def deathdate(self):
        '''schema deathdate as :class:`rdflib.Literal`'''
        return self.rdf.value(self.uriref, SCHEMA_NS.deathDate)

    @property
    def birthyear(self):
        '''birth year'''
        if self.birthdate:
            return self.year_from_isodate(str(self.birthdate))

    @property
    def deathyear(self):
        '''death year'''
        if self.deathdate:
            return self.year_from_isodate(str(self.deathdate))

    # utility method for date parsing
    @classmethod
    def year_from_isodate(cls, date):
        '''Return just the year portion of an ISO8601 date.  Expects
        a string, returns an integer'''
        return int(date.split('-')[0])


class SRUResult(object):
    '''SRU search result object, for use with :meth:`ViafAPI.search`.'''

    def __init__(self, data):
        self._data = data.get('searchRetrieveResponse', {})

    @cached_property
    def total_results(self):
        '''number of records matching the query'''
        return int(self._data.get('numberOfRecords', 0))

    @cached_property
    def records(self):
        '''list of results as :class:`SRUItem`.'''
        return [SRUItem(d['record']) for d in self._data.get('records', [])]


class SRUItem(AttrMap):
    '''Single item returned by a SRU search, for use with
    :meth:`ViafAPI.search` and :class:`SRUResult`.'''

    @property
    def uri(self):
        '''VIAF URI for this result'''
        return self.recordData.Document['@about']

    @property
    def viaf_id(self):
        '''VIAF numeric identifier'''
        return self.recordData.viafID


    @property
    def nametype(self):
        '''type of name (personal, corporate, title, etc)'''
        return self.recordData.nameType

    @property
    def label(self):
        '''first main heading for this item'''
        try:
            return self.recordData.mainHeadings.data[0].text
        except KeyError:
            return self.recordData.mainHeadings.data.text

