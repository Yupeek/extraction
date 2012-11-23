import unittest
import extraction
from extraction.tests.data import *
from extraction.examples.new_return_type import AddressExtractor

class TestSequenceFunctions(unittest.TestCase):
    def setUp(self):
        self.extractor = extraction.Extractor()

    def test_rewriting_relative_urls(self):
        "Test rewriting relative URLs as absolute URLs if source_url is specified."
        self.extractor.techniques = ["extraction.examples.custom_technique.LethainComTechnique"]

        # without source_url, stays as a relative URL
        extracted = self.extractor.extract(LETHAIN_COM_HTML)
        self.assertEqual(extracted.image, "/static/blog/digg_v4/initial_org.png")

        # with source_url, should rewrite as an absolute path
        extracted = self.extractor.extract(LETHAIN_COM_HTML, source_url="http://lethain.com/digg-v4-architecture-process/")
        # rewrites /static/blog/digg_v4/initial_org.png
        self.assertEqual(extracted.images[0], "http://lethain.com/static/blog/digg_v4/initial_org.png")
        # rewrites ../digg_v4/initial_org.png
        self.assertEqual(extracted.images[1], "http://lethain.com/digg_v4/initial_org.png")

    def test_parse_facebook(self):
        # make sure the shuffled sequence does not lose any elements
        self.extractor.techniques = ["extraction.techniques.FacebookOpengraphTags"]
        extracted = self.extractor.extract(FACEBOOK_HTML)
        self.assertEqual(extracted.title, "The Rock")
        self.assertEqual(extracted.titles, ["The Rock"])
        self.assertEqual(extracted.url, "http://www.imdb.com/title/tt0117500/")
        self.assertEqual(extracted.image, "http://ia.media-imdb.com/rock.jpg")
        self.assertEqual(extracted.images, ["http://ia.media-imdb.com/rock.jpg"])
        self.assertTrue(extracted.description, "A group of U.S. Marines, under command of a renegade general, take over Alcatraz and threaten San Francisco Bay with biological weapons.")
        self.assertEqual(len(extracted.descriptions), 1)

    def test_example_lethain_com_technique(self):
        "Test extracting data from lethain.com with a custom technique in extraction.examples."
        self.extractor.techniques = ["extraction.examples.custom_technique.LethainComTechnique"]
        extracted = self.extractor.extract(LETHAIN_COM_HTML)
        self.assertEqual(extracted.title, "Digg v4's Architecture and Development Processes")
        self.assertEqual(extracted.url, None)
        self.assertEqual(extracted._unexpected_values['tags'], [u'architecture', u'digg'])
        self.assertEqual(extracted._unexpected_values['dates'], [u'08/19/2012'])
        self.assertEqual(extracted.image, "/static/blog/digg_v4/initial_org.png")
        self.assertEqual(len(extracted.images), 2)
        self.assertEquals(extracted.description.split(), "A month ago history reset with the second launch of Digg v1 , and memories are starting to fade since much of the Digg team joined SocialCode four months ago, so it seemed like a good time to describe the system and team architecture which ran and developed Digg.com from May 2010 until May 2012.".split())

    def test_example_new_return_type(self):
        "Test returning a non-standard datatype, in this case addresses."
        self.extractor = AddressExtractor()
        self.extractor.techniques = ["extraction.examples.new_return_type.AddressTechnique"]
        extracted = self.extractor.extract(WILLARSON_COM_HTML)
        self.assertEqual(extracted.address, "Cole Valley San Francisco, CA USA")
        self.assertEqual(extracted.url, None)
        self.assertEqual(extracted.title, None)
        self.assertEqual(extracted.description, None)
        self.assertEqual(extracted.image, None)


if __name__ == '__main__':
    unittest.main()