import networkx as nx
import os
import pickle as pkl
import asyncio
import aiofiles

class WebGraph:
    def __init__(self, graph_file="webgraph.pkl"):
        """
        initialize WebGraph module
        """
        self.graph_file = graph_file
        self.graph_lock = asyncio.Lock() # control in memory graph access
        self.file_lock = asyncio.Lock() # control graph io access
        self.graph = self._load_graph()

    def _load_graph(self):
        """
        Load the networkx graph from the file. If the file does not exist, loads default empty DiGraph into memory.
        """
        if os.path.exists(self.graph_file):
            with open(self.graph_file,"rb") as f:
                return pkl.load(f)
        else:
            return nx.DiGraph()

    async def _save_graph(self):
        """
        Safely save the in-memory DiGraph to the file in self.graph_file. 
        """
        async with self.file_lock:
            async with aiofiles.open(self.graph_file, "wb") as f:
                await f.write(pkl.dumps(self.graph))
    
    async def add_node(self, node, **metadata):
        """
        Add a node to graph asynchronously.

        Parameters:
            node (str): Node to remove from the graph.
            metadata (dict): Dict of metadata to add.
        """
        async with self.graph_lock:
            self.graph.add_node(node, **metadata)

        await self._save_graph()
    
    async def add_edge(self, source, target):
        """
        Add an edge to the graph asynchronously.

        Parameters:
            source (str): source node for the directed edge.
            target (str): target node for the directed edge.
        """
        async with self.graph_lock:
            self.graph.add_edge(source, target)
        
        await self._save_graph()
    
    async def remove_node(self, node):
        """
        Remove a node from the graph asynchronously.

        Parameters:
            node (str): Node to remove from the graph.
        """
        async with self.graph_lock:
            if node in self.graph:
                self.graph.remove_node(node)
        
        await self._save_graph()
    
    async def remove_edge(self, source, target):
        """
        Remove an edge from the graph asynchronously. 

        Parameters:
            source (str): source node for the directed edge.
            target (str): target node for the directed edge.
        """
        async with self.graph_lock:
            if self.graph.has_edge(source, target):
                self.graph.remove_edge(source, target)
        
        await self._save_graph()
    
    async def update_node_metadata(self, node, **metadata):
        """
        Update node metadata asynchronously.

        Parameters:
            node (str): The node to update
            metadata (dict): Dict of metadata to update
        """
        async with self.graph_lock:
            if node in self.graph:
                self.graph.nodes[node].update(metadata)
        
        await self._save_graph()
    
    async def print_graph(self):
        """
        Print basic stats on the graph (via networkx)
        """
        async with self.graph_lock:
            print(self.graph)
    
    async def get_node_metadata(self, node):
        """
        Retrieve metadata for a given specific node.

        Parameters:
            node (str): The node to be added
        """
        async with self.graph_lock:
            if node in self.graph:
                return self.graph.nodes[node]
            else:
                raise KeyError(f"Node {node} not found in the graph")
    
    async def add_node_with_outlinks(self, node, outlinks, **metadata):
        """
        Add a node with metadata and its outlinks to the graph asynchronously. 
        Writes to the graph in memory and the graph file specified by self.graph_file.

        Parameters:
            node (str): The node to be added.
            outlinks (list): A list of nodes to which the given node will have edges.
            metadata (dict): Metadata to associate with the node.
        """
        async with self.graph_lock:
            self.graph.add_node(node, **metadata)

            for target in outlinks:
                if target not in self.graph:
                    self.graph.add_node(target)
                self.graph.add_edge(node, target)
        
        await self._save_graph() # async write to file



# usage example
async def main():
    graph = WebGraph()
    
    await graph.add_node("A", metadata={"HomePage": "www.googel.com"})
    await graph.add_node("B", metadata="AboutPage")
    await graph.add_edge("A", "B")
    
    try:
        metadata = await graph.get_node_metadata("A")
        print(metadata)
        metadata = await graph.get_node_metadata("B")
        print(metadata)
    except Exception as e:
        print(f"Exception caught: {e}")
    
    await graph.print_graph()

    await graph.remove_node("B")

    await graph.print_graph()

if __name__ == "__main__":
    asyncio.run(main())
