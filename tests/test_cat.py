import os
import unittest
from medcat.vocab import Vocab
from medcat.cdb import CDB
from medcat.cat import CAT


class CATTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.cdb = CDB.load(os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "examples", "cdb.dat"))
        cls.vocab = Vocab.load(os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "examples", "vocab.dat"))
        cls.cdb.config.general["spacy_model"] = "en_core_sci_sm"
        cls.cdb.config.ner['min_name_len'] = 2
        cls.cdb.config.ner['upper_case_limit_len'] = 3
        cls.cdb.config.general['spell_check'] = True
        cls.cdb.config.linking['train_count_threshold'] = 10
        cls.cdb.config.linking['similarity_threshold'] = 0.3
        cls.cdb.config.linking['train'] = True
        cls.cdb.config.linking['disamb_length_limit'] = 5
        cls.cdb.config.general['full_unlink'] = True
        cls.undertest = CAT(cdb=cls.cdb, config=cls.cdb.config, vocab=cls.vocab)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.undertest.destroy_pipe()

    def test_callable_with_single_text(self):
        text = "The dog is sitting outside the house."
        doc = self.undertest(text)
        self.assertEqual(text, doc.text)

    def test_callable_with_single_empty_text(self):
        self.assertIsNone(self.undertest(""))

    def test_callable_with_single_none_text(self):
        self.assertIsNone(self.undertest(None))

    def test_callable_with_multi_texts(self):
        texts = ["The dog is sitting outside the house.", "", None]
        docs = self.undertest(texts)
        self.assertEqual(3, len(docs))
        self.assertEqual(texts[0], docs[0].text)
        self.assertIsNone(docs[1])
        self.assertIsNone(docs[2])

    def test_callable_with_in_data(self):
        in_data = [
            (1, "The dog is sitting outside the house."),
            (2, "The dog is sitting outside the house.")
        ]
        docs = self.undertest(in_data)
        self.assertEqual(2, len(docs))
        self.assertEqual(in_data[0][1], docs[0].text)
        self.assertEqual(in_data[1][1], docs[1].text)

    @unittest.skip("WIP")
    def test_multiprocessing(self):
        in_data = [
            (1, "The dog is sitting outside the house."),
            (2, ""),
            (3, "The dog is sitting outside the house.")
        ]
        out = list(self.undertest.multiprocessing(in_data, nproc=1))
        self.assertEqual(3, len(out))
        self.assertEqual(1, out[0][0])
        self.assertEqual("The dog is sitting outside the house.", out[0][1]["text"])
        self.assertEqual(2, out[1][0])
        self.assertEqual("", out[1][1]["text"])
        self.assertEqual(3, out[2][0])
        self.assertEqual("The dog is sitting outside the house.", out[2][1]["text"])

    def test_multiprocessing_pipe(self):
        in_data = [
            (1, "The dog is sitting outside the house and second csv."),
            (2, "The dog is sitting outside the house."),
            (3, "The dog is sitting outside the house."),
        ]
        out = self.undertest.multiprocessing_pipe(in_data, nproc=2)
        self.assertTrue(type(out) == list)
        self.assertEqual(3, len(out))
        self.assertEqual(1, out[0][0])
        self.assertEqual('second csv', out[0][1]['entities'][0]['source_value'])
        self.assertEqual(2, out[1][0])
        self.assertEqual({'entities': {}, 'tokens': [], 'text': "The dog is sitting outside the house."}, out[1][1])
        self.assertEqual(3, out[2][0])
        self.assertEqual({'entities': {}, 'tokens': [], 'text': "The dog is sitting outside the house."}, out[2][1])

    def test_multiprocessing_pipe_with_malformed_texts(self):
        in_data = [
            (1, "The dog is sitting outside the house."),
            (2, ""),
            (3, None),
        ]
        out = self.undertest.multiprocessing_pipe(in_data, nproc=1, batch_size=1)
        self.assertTrue(type(out) == list)
        self.assertEqual(3, len(out))
        self.assertEqual(1, out[0][0])
        self.assertEqual({'entities': {}, 'tokens': [], 'text': "The dog is sitting outside the house."}, out[0][1])
        self.assertEqual(2, out[1][0])
        self.assertIsNone(out[1][1])
        self.assertEqual(3, out[2][0])
        self.assertIsNone(out[2][1])

    def test_multiprocessing_pipe_return_dict(self):
        in_data = [
            (1, "The dog is sitting outside the house."),
            (2, "The dog is sitting outside the house."),
            (3, "The dog is sitting outside the house.")
        ]
        out = self.undertest.multiprocessing_pipe(in_data, nproc=2, return_dict=True)
        self.assertTrue(type(out) == dict)
        self.assertEqual(3, len(out))
        self.assertEqual({'entities': {}, 'tokens': [], 'text': "The dog is sitting outside the house."}, out[1])
        self.assertEqual({'entities': {}, 'tokens': [], 'text': "The dog is sitting outside the house."}, out[2])
        self.assertEqual({'entities': {}, 'tokens': [], 'text': "The dog is sitting outside the house."}, out[3])

    def test_train(self):
        self.undertest.cdb.print_stats()
        self.undertest.train(["The dog is not a house", "The house is not a dog"])
        self.undertest.cdb.print_stats()

    def test_get_entities(self):
        text = "The dog is sitting outside the house."
        out = self.undertest.get_entities(text)
        self.assertEqual({}, out["entities"])
        self.assertEqual([], out["tokens"])

    def test_get_entities_from_in_data(self):
        in_data = [(1, "The dog is sitting outside the house."), (2, ""), (3, "The dog is sitting outside the house.")]
        out = self.undertest.get_entities(in_data, n_process=2)
        self.assertEqual(3, len(out))

    def test_train_supervised(self):
        fp, fn, tp, p, r, f1, cui_counts, examples = self.undertest.train_supervised(os.path.join(os.path.dirname(__file__), "resources", "medcat_trainer_export.json"), nepochs=1)
        self.assertEqual({}, fp)
        self.assertEqual({}, fn)
        self.assertEqual({}, tp)
        self.assertEqual({}, p)
        self.assertEqual({}, r)
        self.assertEqual({}, f1)
        self.assertEqual({}, cui_counts)
        self.assertEqual({}, examples)

    def test_no_error_handling_on_none_input(self):
        out = self.undertest.get_entities(None)
        self.assertEqual({}, out["entities"])
        self.assertEqual([], out["tokens"])

    def test_no_error_handling_on_empty_string_input(self):
        out = self.undertest.get_entities("")
        self.assertEqual({}, out["entities"])
        self.assertEqual([], out["tokens"])

    def test_no_raise_on_single_process_with_none(self):
        out = self.undertest.get_entities(["The dog is sitting outside the house.", None, "The dog is sitting outside the house."], n_process=1, batch_size=2)
        self.assertEqual(3, len(out))
        self.assertEqual({}, out[0]["entities"])
        self.assertEqual([], out[0]["tokens"])
        self.assertEqual({}, out[1]["entities"])
        self.assertEqual([], out[1]["tokens"])
        self.assertEqual({}, out[2]["entities"])
        self.assertEqual([], out[2]["tokens"])

    def test_no_raise_on_single_process_with_empty_string(self):
        out = self.undertest.get_entities(["The dog is sitting outside the house.", "", "The dog is sitting outside the house."], n_process=1, batch_size=2)
        self.assertEqual(3, len(out))
        self.assertEqual({}, out[0]["entities"])
        self.assertEqual([], out[0]["tokens"])
        self.assertEqual({}, out[1]["entities"])
        self.assertEqual([], out[1]["tokens"])
        self.assertEqual({}, out[2]["entities"])
        self.assertEqual([], out[2]["tokens"])

    def test_error_handling_multi_processes(self):
        out = self.undertest.get_entities([(1, "The dog is sitting outside the house."),
                                           (2, "The dog is sitting outside the house."),
                                           (3, "The dog is sitting outside the house."),
                                           (4, None),
                                           (5, None)], n_process=2, batch_size=2)
        self.assertEqual(5, len(out))
        self.assertEqual({}, out[0]["entities"])
        self.assertEqual([], out[0]["tokens"])
        self.assertEqual("The dog is sitting outside the house.", out[0]["text"])
        self.assertEqual({}, out[1]["entities"])
        self.assertEqual([], out[1]["tokens"])
        self.assertEqual("The dog is sitting outside the house.", out[1]["text"])
        self.assertEqual({}, out[2]["entities"])
        self.assertEqual([], out[2]["tokens"])
        self.assertEqual("The dog is sitting outside the house.", out[2]["text"])
        self.assertEqual({}, out[3]["entities"])
        self.assertEqual([], out[3]["tokens"])
        self.assertFalse(hasattr(out[2], "text"))
        self.assertEqual({}, out[4]["entities"])
        self.assertEqual([], out[4]["tokens"])
        self.assertFalse(hasattr(out[4], "text"))


if __name__ == '__main__':
    unittest.main()
