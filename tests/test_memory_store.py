import tempfile
import unittest
from pathlib import Path
from memory_store import MemoryStore

class MemoryStoreTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.store = MemoryStore(Path(self.tmp.name) / "test.db")
    def tearDown(self):
        self.tmp.cleanup()
    def test_add_and_search(self):
        self.store.add("research-rag", "decision", "Chunk size",
                       "Test 500 token chunks with 80 token overlap.", tags="chunking retrieval")
        hits = self.store.search("500 token overlap", project="research-rag")
        self.assertTrue(hits)
        self.assertEqual(hits[0]["title"], "Chunk size")
    def test_project_isolation(self):
        self.store.add("project-a", "note", "Secret", "Only for project A.")
        self.assertEqual(self.store.search("Secret", project="project-b"), [])
    def test_context_and_export(self):
        self.store.add("research-rag", "question", "Reranking",
                       "Should we add a cross-encoder reranker?")
        self.assertIn("Reranking", self.store.build_context("research-rag", "reranker"))
        self.assertIn("# Project Memory: research-rag",
                      self.store.export_markdown("research-rag"))

if __name__ == "__main__":
    unittest.main()
