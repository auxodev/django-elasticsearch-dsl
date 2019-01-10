from copy import deepcopy

from django.utils.encoding import python_2_unicode_compatible
from elasticsearch_dsl import Index as DSLIndex

from .apps import DEDConfig
from .registries import registry


@python_2_unicode_compatible
class Index(DSLIndex):

    def __init__(self, name, using='default'):
        super(Index, self).__init__(name, using)
        self._settings = deepcopy(DEDConfig.default_index_settings())

    def document(self, document, *args, **kwargs):
        """
        Extend to register the doc_type in the global document registry
        """
        document = super(Index, self).document(document, *args, **kwargs)
        registry.register(self, document)
        return document

    # available for backwards compatibility
    # TODO: remove in ES 7.0.0
    doc_type = document

    def __str__(self):
        return self._name
