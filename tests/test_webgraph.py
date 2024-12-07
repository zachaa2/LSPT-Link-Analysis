import unittest
import asyncio
import os
import shutil
from webgraph import WebGraph

class TestWebGraph(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.test_file = "test_webgraph.pkl"
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        self.graph = WebGraph(graph_file=self.test_file)

    async def asyncTearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    async def test_add_and_get_node_metadata(self):
        await self.graph.add_node("NodeA", category="test")
        metadata = await self.graph.get_node_metadata("NodeA")
        self.assertIn("category", metadata)
        self.assertEqual(metadata["category"], "test")

    async def test_add_edge(self):
        await self.graph.add_node("NodeB", desc="source node")
        await self.graph.add_node("NodeC", desc="target node")
        await self.graph.add_edge("NodeB", "NodeC")

        edges = await self.graph.get_subgraph("NodeB", k=1)
        self.assertIn(("NodeB", "NodeC", {}), edges)

    async def test_remove_node(self):
        await self.graph.add_node("NodeD")
        await self.graph.remove_node("NodeD")
        with self.assertRaises(KeyError):
            await self.graph.get_node_metadata("NodeD")

    async def test_remove_edge(self):
        await self.graph.add_node("NodeE")
        await self.graph.add_node("NodeF")
        await self.graph.add_edge("NodeE", "NodeF")
        await self.graph.remove_edge("NodeE", "NodeF")

        edges = await self.graph.get_subgraph("NodeE", k=1)
        self.assertNotIn(("NodeE", "NodeF", {}), edges)

    async def test_update_node_metadata(self):
        await self.graph.add_node("NodeG", color="blue")
        await self.graph.update_node_metadata("NodeG", color="red", visited=True)
        metadata = await self.graph.get_node_metadata("NodeG")
        self.assertEqual(metadata["color"], "red")
        self.assertTrue(metadata["visited"])

    async def test_add_node_with_outlinks(self):
        await self.graph.add_node_with_outlinks("NodeH", ["NodeI", "NodeJ"], type="hub")
        metadata = await self.graph.get_node_metadata("NodeH")
        self.assertEqual(metadata["type"], "hub")

        edges = await self.graph.get_subgraph("NodeH", k=1)
        self.assertIn(("NodeH", "NodeI", {}), edges)
        self.assertIn(("NodeH", "NodeJ", {}), edges)

    async def test_pagerank_calculation(self):
        await self.graph.add_node_with_outlinks("NodeK", ["NodeL", "NodeM"])
        await self.graph.add_node_with_outlinks("NodeL", ["NodeM"])
        await self.graph.add_node("NodeM")

        await self.graph.calculate_pagerank()
        pagerank = self.graph.get_pagerank()
        self.assertIn("NodeK", pagerank)
        self.assertIn("NodeL", pagerank)
        self.assertIn("NodeM", pagerank)

        self.assertTrue(all(0 <= v <= 1 for v in pagerank.values()))
        self.assertAlmostEqual(sum(pagerank.values()), 1.0, places=5)

    async def test_initialization_no_file(self):
        if os.path.exists("non_existent_file.pkl"):
            os.remove("non_existent_file.pkl")
        temp_graph = WebGraph(graph_file="non_existent_file.pkl")
        await temp_graph.print_graph()

    async def test_get_node_metadata_nonexistent_node(self):
        with self.assertRaises(KeyError):
            await self.graph.get_node_metadata("NonExistentNode")

    async def test_get_subgraph_nonexistent_node(self):
        with self.assertRaises(KeyError):
            await self.graph.get_subgraph("NoSuchNode", 1)

    async def test_remove_nonexistent_node(self):
        result = await self.graph.remove_node("NoSuchNode")

    async def test_remove_nonexistent_edge(self):
        await self.graph.add_node("X")
        await self.graph.add_node("Y")
        await self.graph.remove_edge("X", "Y")

    async def test_get_pagerank_before_calculation(self):
        with self.assertRaises(KeyError):
            self.graph.get_pagerank("AnyNode")

    async def test_get_pagerank_for_nonexistent_node(self):
        await self.graph.add_node("A")
        await self.graph.calculate_pagerank()
        with self.assertRaises(KeyError):
            self.graph.get_pagerank("NoSuchNode")

if __name__ == "__main__":
    unittest.main()
