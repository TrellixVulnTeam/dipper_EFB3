from intermine.webservice import Service
from dipper.models.assoc.G2PAssoc import G2PAssoc
from dipper.sources.Source import Source
from dipper.models.Dataset import Dataset
import logging
import datetime

logger = logging.getLogger(__name__)


class MGISlim(Source):
    """
    slim mgi model only containing Gene to phenotype associations
    Uses mousemine: http://www.mousemine.org/mousemine/begin.do
    """

    def __init__(self):
        super().__init__('mgi_slim')
        self.dataset = Dataset(
            'mgi_slim', 'MGISlim', 'http://www.mousemine.org/mousemine/service')

    def parse(self, limit=None):
        self.load_bindings()

        count = 0
        for num in range(10, 100):
            fuzzy_gene = "MGI:{0}*".format(num)
            gene = "MGI:{0}".format(num)
            service = Service("http://www.mousemine.org/mousemine/service")
            logging.getLogger('Model').setLevel(logging.CRITICAL)
            logging.getLogger('JSONIterator').setLevel(logging.CRITICAL)
            query = service.new_query("OntologyAnnotation")
            query.add_constraint("subject", "SequenceFeature")
            query.add_constraint("ontologyTerm", "MPTerm")
            query.add_view(
                "subject.primaryIdentifier", "subject.symbol",
                "subject.sequenceOntologyTerm.name", "ontologyTerm.identifier",
                "ontologyTerm.name", "evidence.publications.pubMedId",
                "evidence.comments.type", "evidence.comments.description"
            )
            query.add_sort_order("OntologyAnnotation.ontologyTerm.name", "ASC")
            query.add_constraint("subject.organism.taxonId", "=", "10090", code="A")
            query.add_constraint("subject", "LOOKUP", fuzzy_gene, code="B")
            query.add_constraint("subject.primaryIdentifier", "CONTAINS", gene, code="C")
            query.outerjoin("evidence.comments")

            for row in query.rows():
                # To print raw data to stdout
                # print("{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}".format(
                #      row["subject.primaryIdentifier"], row["subject.symbol"],
                #      row["subject.sequenceOntologyTerm.name"], row["ontologyTerm.identifier"],
                #      row["ontologyTerm.name"], row["evidence.publications.pubMedId"],
                #      row["evidence.comments.type"], row["evidence.comments.description"]))

                mgi_curie = row["subject.primaryIdentifier"]
                mp_curie = row["ontologyTerm.identifier"]
                pub_curie = "PMID:{0}".format(row["evidence.publications.pubMedId"])
                assoc = G2PAssoc(self.name, mgi_curie, mp_curie)
                if row["evidence.publications.pubMedId"]:
                    assoc.add_source(pub_curie)
                    assoc.add_evidence('ECO:0000304')
                else:
                    assoc.add_evidence('ECO:0000059')

                assoc.add_association_to_graph(self.graph)

            if not count % 10 and count != 0:
                count_from = count - 10
                logger.info("{0} processed ids from MGI:{1}* to MGI:{2}*".format(
                    datetime.datetime.now(), count_from, count))

            count += 1
            if limit and count >= limit:
                break

        return

