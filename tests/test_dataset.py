import datetime
import unittest
import logging
from datetime import datetime
from rdflib import XSD
from rdflib import URIRef, Literal, Graph

from dipper.graph.RDFGraph import RDFGraph
from dipper.models.Dataset import Dataset
from dipper import curie_map as curiemap

logging.basicConfig(level=logging.WARNING)
LOGGER = logging.getLogger(__name__)


class DatasetTestCase(unittest.TestCase):
    """
    For testing metadata emitted by Dataset class

    Dataset creates a graph describing the metadata associated with the dataset in
    question, which should follow the HCLS specification for dataset descriptions
    https://www.w3.org/TR/2015/NOTE-hcls-dataset-20150514/
    """

    @classmethod
    def setUpClass(cls):
        cls.curie_map = curiemap.get()

        # parameters passed to code, to be returned in graph
        cls.monarch_data_curie_prefix = "MonarchArchive"
        cls.identifier = "fakeingest"
        cls.ingest_description = "some ingest description"
        cls.ingest_url = "http://fakeingest.com"
        cls.ingest_title = "this ingest title"
        cls.ingest_logo_url = "http://fakeingest.com/logo.png"
        cls.license_url = "https://choosealicense.com/licenses/mit/"
        cls.license_url_default = "https://project-open-data.cio.gov/unknown-license/"
        cls.data_rights = "https://www.gnu.org/licenses/gpl-3.0.html"

        # parse test graph once, to test triples counts/statistics below
        cls.test_ttl = "tests/resources/fakeingest/test_graph_simple.ttl"
        cls.test_graph = RDFGraph()
        cls.test_graph.parse(cls.test_ttl, format="turtle")

        # expected things:
        cls.expected_curie_prefix = "MonarchArchive"
        cls.timestamp_date = datetime.today().strftime("%Y%m%d")

        cls.base_cito = 'http://purl.org/spar/cito/'
        cls.base_dc = 'http://purl.org/dc/elements/1.1/'
        cls.base_dcat = 'http://www.w3.org/ns/dcat#'
        cls.base_dcterms = 'http://purl.org/dc/terms/'
        cls.base_dctypes = 'http://purl.org/dc/dcmitype/'
        cls.base_pav = 'http://purl.org/pav/'
        cls.base_rdf = 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'
        cls.base_rdfs = 'http://www.w3.org/2000/01/rdf-schema#'
        cls.base_schemaorg = 'http://schema.org/'
        cls.base_void = 'http://rdfs.org/ns/void#'

        # expected summary level IRI
        cls.summary_level_IRI = URIRef(cls.curie_map.get(cls.expected_curie_prefix)
                                       + cls.identifier)
        # expected version level IRI
        cls.version_level_IRI = URIRef(cls.summary_level_IRI + cls.timestamp_date)

        # expected distribution level IRI (for ttl resource)
        cls.distribution_level_IRI_ttl = URIRef(cls.version_level_IRI + ".ttl")

        # set expected IRIs for predicates and other things
        cls.iri_rdf_type = URIRef(cls.base_rdf + "type")
        cls.iri_title = URIRef(cls.base_dcterms + "title")
        cls.iri_dataset = URIRef(cls.base_dctypes + "Dataset")
        cls.iri_description = URIRef(cls.base_dc + "description")
        cls.iri_publisher = URIRef(cls.base_dcterms + "Publisher")
        cls.iri_source = URIRef(cls.base_dcterms + "source")
        cls.iri_logo = URIRef(cls.base_schemaorg + "logo")
        cls.iri_mi_org = URIRef("https://monarchinitiative.org/")
        cls.iri_created = URIRef(cls.base_dcterms + "created")
        cls.iri_version = URIRef(cls.base_pav + "version")
        cls.iri_retrieved_on = URIRef(cls.base_pav + "retrievedOn")
        cls.iri_creator = URIRef(cls.base_dcterms + "creator")
        cls.iri_is_version_of = URIRef(cls.base_dcterms + "isVersionOf")
        cls.iri_distribution = URIRef(cls.base_dcat + "Distribution")
        cls.iri_created_with = URIRef(cls.base_pav + "createdWith")
        cls.iri_format = URIRef(cls.base_dcterms + "format")
        cls.iri_download_url = URIRef(cls.base_dcterms + "downloadURL")
        cls.iri_license = URIRef(cls.base_dcterms + "license")
        cls.iri_data_rights = URIRef(cls.base_dcterms + "rights")
        cls.iri_cites_as_authority = URIRef(cls.base_cito + "citesAsAuthority")
        cls.iri_triples_count = URIRef(cls.base_void + "triples")
        cls.iri_entities_count = URIRef(cls.base_void + "entities")
        cls.iri_distinct_subjects = URIRef(cls.base_void + "distinctSubjects")
        cls.iri_distinct_objects = URIRef(cls.base_void + "distinctObjects")
        cls.iri_distinct_properties = URIRef(cls.base_void + "properties")
        cls.iri_void_class = URIRef(cls.base_void + "class")
        cls.iri_rdfs_class = URIRef(cls.base_rdfs + "Class")
        cls.iri_rdfs_label = URIRef(cls.base_rdfs + "label")
        cls.iri_void_class_partition = URIRef(cls.base_void + "classPartition")

        cls.iri_dipper = URIRef("https://github.com/monarch-initiative/dipper")
        cls.iri_ttl_spec = URIRef("https://www.w3.org/TR/turtle/")

        cls.iri_biolink_category = URIRef("http://w3id.org/biolink/vocab/category")
        cls.iri_biolink_case = URIRef("http://w3id.org/biolink/vocab/case")
        cls.iri_biolink_info_content = \
            URIRef("http://w3id.org/biolink/vocab/InformationContentEntity")

        cls.iri_distinct_class_count_blank_node = URIRef(
            RDFGraph.curie_util.get_uri(Dataset.make_id("distinct_class_count")))

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.dataset = Dataset(
            identifier=self.monarch_data_curie_prefix + ":" + self.identifier,
            ingest_title=self.ingest_title,
            ingest_url=self.ingest_url,
            ingest_logo=self.ingest_logo_url,
            ingest_description=self.ingest_description,
            license_url=self.license_url,
            data_rights=self.data_rights
        )

        # put all triples in a list for debugging below
        self.all_triples = list(self.dataset.graph.triples((None, None, None)))

    def tearDown(self):
        pass

    def test_dataset_has_graph(self):
        self.assertIsInstance(self.dataset.graph, Graph,
                              "dataset doesn't contain an RDF graph")

    def test_get_graph(self):
        self.assertIsInstance(
            self.dataset.get_graph(), RDFGraph,
            "get_graph() didn't return an RDF graph")

    def test_get_license(self):
        gpl2_iri = "https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html"
        self.dataset.license_url = gpl2_iri
        self.assertEqual(self.dataset.get_license(),
                         gpl2_iri, "set_license didn't set license_url correctly")

    def test_set_citation(self):
        citation_iri =\
            "http://purl.obolibrary.org/obo/uberon/releases/2016-01-26/uberon.owl"
        self.dataset.set_citation(citation_iri)
        self.assertTrue(self.dataset.citation.issuperset([citation_iri]))
        triples = list(self.dataset.graph.triples(
            (self.version_level_IRI,
             URIRef(self.iri_cites_as_authority),
             URIRef(citation_iri))))
        self.assertTrue(len(triples) == 1, "missing citation triple")

    def test_set_ingest_source_file_version_num(self):
        this_version = "version1234"
        file_iri = "http://somefilesource.org/file.txt"
        self.dataset.set_ingest_source_file_version_num(file_iri, this_version)
        triples = list(self.dataset.graph.triples(
            (URIRef(file_iri), self.iri_version, Literal(this_version))))
        self.assertTrue(len(triples) == 1, "ingest source file version not set")

    def test_set_ingest_source_file_version_date(self):
        this_version = "1970-01-01"
        file_iri = "http://somefilesource.org/file.txt"
        self.dataset.set_ingest_source_file_version_date(file_iri, this_version)

        triples = list(self.dataset.graph.triples(
            (URIRef(file_iri),
             self.iri_version,
             Literal(this_version, datatype=XSD.date))))
        self.assertTrue(len(triples) == 1,
                        "ingest source file version not set with literal type of date")

    #
    # Test summary level triples:
    #
    def test_summary_level_type(self):
        triples = list(self.dataset.graph.triples(
            (self.summary_level_IRI, self.iri_rdf_type, self.iri_dataset)))
        self.assertTrue(len(triples) == 1, "missing summary level type triple")

    def test_summary_level_title(self):
        triples = list(self.dataset.graph.triples(
            (self.summary_level_IRI, self.iri_title, Literal(self.ingest_title))))
        self.assertTrue(len(triples) == 1, "missing summary level title triple")

    def test_summary_level_description(self):
        # by default, description is the class's docstring
        triples = list(self.dataset.graph.triples(
            (self.summary_level_IRI, self.iri_description,
             Literal(self.ingest_description))))
        self.assertTrue(len(triples) == 1, "missing summary level description triple")

    def test_summary_level_publisher(self):
        triples = list(self.dataset.graph.triples(
            (self.summary_level_IRI, self.iri_publisher, self.iri_mi_org)))
        self.assertTrue(len(triples) == 1, "missing summary level publisher triple")

    def test_summary_level_source_web_page(self):
        triples = list(self.dataset.graph.triples(
            (self.summary_level_IRI, self.iri_source, URIRef(self.ingest_url))))
        self.assertTrue(len(triples) == 1, "missing summary level source page triple")

    def test_summary_level_source_logo(self):
        triples = list(self.dataset.graph.triples(
            (self.summary_level_IRI, self.iri_logo, URIRef(self.ingest_logo_url))))
        self.assertTrue(len(triples) == 1, "missing summary level source logo triple")

    #
    # Test version level resource triples:
    #
    def test_version_level_type(self):
        triples = list(self.dataset.graph.triples(
            (self.version_level_IRI, self.iri_rdf_type, self.iri_dataset)))
        self.assertTrue(len(triples) == 1, "missing version level type triple")

    def test_version_level_title(self):
        triples = list(self.dataset.graph.triples(
            (self.version_level_IRI, self.iri_title, Literal(self.ingest_title))))
        self.assertTrue(len(triples) == 1, "missing version level title triple")

    def test_version_level_description(self):
        triples = list(self.dataset.graph.triples(
            (self.version_level_IRI, self.iri_description,
             Literal(self.ingest_description))))
        self.assertTrue(len(triples) == 1, "missing version level description triple")

    def test_version_level_created(self):
        triples = list(self.dataset.graph.triples(
            (self.version_level_IRI, self.iri_created, None)))
        self.assertTrue(len(triples) == 1,
                        "didn't get exactly 1 version level created triple")
        self.assertEqual(triples[0][2],
                         Literal(self.timestamp_date, datatype=XSD.date),
                         "version level created triple has the wrong timestamp")

    def test_version_level_version(self):
        triples = list(self.dataset.graph.triples(
            (self.version_level_IRI, self.iri_version, None)))
        self.assertTrue(len(triples) == 1,
                        "didn't get exactly one version level version triple")
        self.assertEqual(triples[0][2],
                         Literal(self.timestamp_date, datatype=XSD.date),
                         "version level version triple has the wrong timestamp")

    def test_version_level_creator(self):
        triples = list(self.dataset.graph.triples(
            (self.version_level_IRI, self.iri_creator, self.iri_mi_org)))
        self.assertTrue(len(triples) == 1, "missing version level creator triple")

    def test_version_level_publisher(self):
        triples = list(self.dataset.graph.triples(
            (self.version_level_IRI, self.iri_publisher, self.iri_mi_org)))
        self.assertTrue(len(triples) == 1, "missing version level publisher triple")

    def test_version_level_isVersionOf(self):
        triples = list(self.dataset.graph.triples(
            (self.version_level_IRI, self.iri_is_version_of, self.summary_level_IRI)))
        self.assertTrue(len(triples) == 1, "missing version level isVersionOf triple")

    #
    # test distribution level triples
    #
    def test_distribution_level_dataset_type(self):
        triples = list(self.dataset.graph.triples(
            (self.distribution_level_IRI_ttl, self.iri_rdf_type, self.iri_dataset)))
        self.assertTrue(len(triples) == 1, "missing version level type dataset triple")

    def test_distribution_level_distribution_type(self):
        triples = list(self.dataset.graph.triples(
            (self.distribution_level_IRI_ttl,
             self.iri_rdf_type,
             self.iri_distribution)))
        self.assertTrue(len(triples) == 1,
                        "missing version level type distribution triple")

    def test_distribution_level_title(self):
        triples = list(self.dataset.graph.triples(
            (self.distribution_level_IRI_ttl, self.iri_title,
             Literal(self.ingest_title))))
        self.assertTrue(len(triples) == 1, "missing version level type title triple")

    def test_distribution_level_description(self):
        triples = list(self.dataset.graph.triples(
            (self.distribution_level_IRI_ttl, self.iri_description,
             Literal(self.ingest_description))))
        self.assertTrue(len(triples) == 1,
                        "missing version level type description triple")

    def test_distribution_level_created(self):
        triples = list(self.dataset.graph.triples(
            (self.distribution_level_IRI_ttl, self.iri_created, None)))
        self.assertTrue(len(triples) == 1,
                        "didn't get exactly 1 version level type created triple")
        self.assertEqual(triples[0][2], Literal(self.timestamp_date, datatype=XSD.date))

    def test_distribution_level_version(self):
        triples = list(self.dataset.graph.triples(
            (self.distribution_level_IRI_ttl, self.iri_version, None)))
        self.assertTrue(len(triples) == 1,
                        "didn't get exactly 1 version level type version triple")
        self.assertEqual(triples[0][2], Literal(self.timestamp_date, datatype=XSD.date))

    def test_distribution_level_creator(self):
        triples = list(self.dataset.graph.triples(
            (self.distribution_level_IRI_ttl, self.iri_creator, self.iri_mi_org)))
        self.assertTrue(len(triples) == 1,
                        "missing distribution level creator triple")

    def test_distribution_level_publisher(self):
        triples = list(self.dataset.graph.triples(
            (self.distribution_level_IRI_ttl, self.iri_publisher, self.iri_mi_org)))
        self.assertTrue(len(triples) == 1,
                        "missing distribution level publisher triple")

    def test_distribution_level_created_with(self):
        triples = list(self.dataset.graph.triples(
            (self.distribution_level_IRI_ttl,
             self.iri_created_with,
             self.iri_dipper)))
        self.assertTrue(len(triples) == 1,
                        "missing distribution level createdWith triple")

    def test_distribution_level_format(self):
        triples = list(self.dataset.graph.triples(
            (self.distribution_level_IRI_ttl,
             self.iri_format,
             self.iri_ttl_spec)))
        self.assertTrue(len(triples) == 1,
                        "missing distribution level format triple")

    def test_distribution_level_download_url(self):
        triples = list(self.dataset.graph.triples(
            (self.distribution_level_IRI_ttl,
             self.iri_download_url,
             self.distribution_level_IRI_ttl)))
        self.assertTrue(len(triples) == 1,
                        "missing distribution level downloadUrl triple")

    def test_distribution_level_license_url(self):
        triples = list(self.dataset.graph.triples(
            (self.distribution_level_IRI_ttl,
             self.iri_license,
             URIRef(self.license_url))))
        self.assertTrue(len(triples) == 1,
                        "missing distribution level license triple")

    def test_distribution_level_data_rights(self):
        triples = list(self.dataset.graph.triples(
            (self.distribution_level_IRI_ttl,
             self.iri_data_rights,
             URIRef(self.data_rights))))
        self.assertTrue(len(triples) == 1,
                        "missing distribution level data rights triple")

    def test_distribution_level_no_license_url_default_value(self):
        self.dataset = Dataset(
            identifier=self.monarch_data_curie_prefix + ":" + self.identifier,
            ingest_title=self.ingest_title,
            ingest_url=self.ingest_url,
            ingest_logo=self.ingest_logo_url,
            ingest_description=self.ingest_description,
            license_url=None,
            data_rights=self.data_rights
        )
        triples = list(self.dataset.graph.triples(
            (self.distribution_level_IRI_ttl,
             self.iri_license,
             URIRef(self.license_url_default))))
        self.assertTrue(len(triples) == 1,
                        "distribution level default license triple not set")


if __name__ == '__main__':
    unittest.main()
