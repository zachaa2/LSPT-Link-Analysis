from typing import Union
from fastapi import FastAPI, HTTPException
from webgraph import WebGraph
from pydantic import BaseModel
import asyncio
from typing import List, Optional

app = FastAPI()
graph = WebGraph()

'''
    The following are the structures of the Request that gets recieved to this
    API endpoint. 
        ex. NodeRequest:
            {
                "node": "node1"
                "metadata": {
                    "url": "google.com"
                    "num_clicks": 100
                    "{metadata type}": {value}
                }
            }    
'''
class NodeRequest(BaseModel):
    node: str
    metadata: Optional[dict] = None

class NodeWithOutlinksRequest(BaseModel):
    node: str
    metadata: Optional[dict] = None
    outlinks: List[str]

class EdgeRequest(BaseModel):
    source: str
    target: str

class SubgraphRequest(BaseModel):
    node: str
    k: int


@app.on_event("startup")
async def startup_event():
    # Perform any startup tasks if needed
    await graph.calculate_pagerank()


@app.post("/add_node")
async def add_node(request: NodeRequest):
    await graph.add_node(request.node, **(request.metadata or {}))
    return {"message": f"Node '{request.node}' added successfully."}


@app.post("/add_edge")
async def add_edge(request: EdgeRequest):
    await graph.add_edge(request.source, request.target)
    return {"message": f"Edge from '{request.source}' to '{request.target}' added successfully."}


@app.delete("/remove_node/{node}")
async def remove_node(node: str):
    await graph.remove_node(node)
    return {"message": f"Node '{node}' removed successfully."}


@app.delete("/remove_edge")
async def remove_edge(request: EdgeRequest):
    await graph.remove_edge(request.source, request.target)
    return {"message": f"Edge from '{request.source}' to '{request.target}' removed successfully."}


@app.post("/add_node_with_outlinks")
async def add_node_with_outlinks(request: NodeWithOutlinksRequest):
    await graph.add_node_with_outlinks(
        request.node,
        request.outlinks,
        **(request.metadata or {})
    )
    return {"message": f"Node '{request.node}' with outlinks added successfully."}


@app.get("/get_pagerank")
async def get_all_pageranks():
    graph.calculate_pagerank()
    pagerank = graph.get_pagerank()
    return pagerank


@app.get("/get_pagerank/{node}")
async def get_pagerank(node: str):
    try:
        graph.calculate_pagerank()
        pagerank = graph.get_pagerank(node)
        return {"node": node, "pagerank": pagerank}
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.post("/get_subgraph")
async def get_subgraph(request: SubgraphRequest):
    try:
        subgraph = await graph.get_subgraph(request.node, request.k)
        return {"subgraph": subgraph}
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.get("/print_graph")
async def print_graph():
    await graph.print_graph()
    return {"message": "Graph printed to the console."}


@app.get("/get_node_metadata/{node}")
async def get_node_metadata(node: str):
    try:
        metadata = await graph.get_node_metadata(node)
        return metadata
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
