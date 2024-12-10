from typing import Union
from fastapi import FastAPI, HTTPException
from webgraph import WebGraph
from pydantic import BaseModel
import asyncio
from typing import List, Optional
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--graph_name", type=str, required=True, help="name of the graph file. E.g., if name is \"graph\", then the file will be \"graph.pkl\"")
args = parser.parse_args()


app = FastAPI()
graph = WebGraph(graph_file=f"{args.graph_name}.pkl")

'''
    The following are the structures of the Request that gets recieved to this
    API endpoint. 
        ex. NodeRequest:
            {
                "url": "google.com"
                "metadata": {
                    "url": "google.com"
                    "num_clicks": 100
                    "{metadata type}": {value}
                }
            }    
'''
class NodeRequest(BaseModel):
    url: str
    metadata: Optional[dict] = None

class NodeWithOutlinksRequest(BaseModel):
    url: str
    metadata: Optional[dict] = None
    child_nodes: List[str]

class EdgeRequest(BaseModel):
    source: str
    target: str

class SubgraphRequest(BaseModel):
    url: str
    k: int


async def pagerank_task():
    while True:
        try:
            print("Calculating PageRank...")
            await graph.calculate_pagerank()
            print("PageRank calculation complete.")
        except Exception as e:
            print(f"Error in PageRank calculation: {e}")
        
        # Wait for 1 hour (3600 seconds)
        await asyncio.sleep(3600)

@app.on_event('startup')
async def app_startup():
    asyncio.create_task(pagerank_task())

@app.post("/add_node")
async def add_node(request: NodeRequest):
    await graph.add_node(request.url, **(request.metadata or {}))
    return {"message": f"Node '{request.url}' added successfully."}


@app.post("/add_edge")
async def add_edge(request: EdgeRequest):
    await graph.add_edge(request.source, request.target)
    return {"message": f"Edge from '{request.source}' to '{request.target}' added successfully."}



@app.delete("/remove_edge")
async def remove_edge(request: EdgeRequest):
    await graph.remove_edge(request.source, request.target)
    return {"message": f"Edge from '{request.source}' to '{request.target}' removed successfully."}



@app.post("/get_subgraph")
async def get_subgraph(request: SubgraphRequest):
    try:
        subgraph = await graph.get_subgraph(request.url, request.k)
        return {"subgraph": subgraph}
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.get("/print_graph")
async def print_graph():
    await graph.print_graph()
    return {"message": "Graph printed to the console."}




#-------------------------------------------------------------------------------------
#                   Endpoints other teams will call
#-------------------------------------------------------------------------------------


#crawling
@app.post("/crawling/add_nodes")
async def add_node_with_outlinks(request: NodeWithOutlinksRequest):
    await graph.add_node_with_outlinks(
        request.url,
        request.child_nodes,
        **(request.metadata or {})
    )
    return {"message": f"Node '{request.url}' with outlinks added successfully."}

@app.delete("/crawling/remove_node/{url}")
async def remove_node(url: str):
    await graph.remove_node(url)
    return {"message": f"Node '{url}' removed successfully."}


#evaluation 
@app.post("/evaluation/update_metadata")
async def  update_node_metadata(request: NodeRequest):
    await graph.update_node_metadata(request.url, **(request.metadata or {}))
    return {"message": f"Node '{request.url}' updated successfully."}

@app.get("/evaluation/get_node_metadata/{node}")
async def get_node_metadata(node: str):
    try:
        metadata = await graph.get_node_metadata(node)
        return metadata
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))


#ranking status okay
@app.get("/ranking/get_pagerank")
async def get_all_pageranks():
    pagerank = graph.get_pagerank()
    return pagerank

@app.get("/ranking/{url}")
async def get_pagerank(url: str):
    try:
        pagerank = graph.get_pagerank(url)
        return {"url": url, "pagerank": pagerank}
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))


#uiux ugly but status okay
@app.post("/uiux/graph")
async def get_subgraph(request: SubgraphRequest):
    try:
        subgraph = await graph.get_subgraph(request.url, request.k)
        nodes = set()
        result = dict()
        result["nodes"]=[]
        result["edges"]=[]
        nodeID = dict()
        idCounter = 0
        for edges in subgraph:
            if edges[0] not in nodes:
                nodeDict = dict()
                nodeDict["id"]=idCounter
                nodeID[edges[0]]=idCounter
                nodeDict["url"]=edges[0]
                nodeDict["page_rank"] = graph.get_pagerank(edges[0])
                idCounter+=1
                result["nodes"].append(nodeDict)
                nodes.add(edges[0])
            if edges[1] not in nodes:
                nodeDict = dict()
                nodeDict["id"]=idCounter
                nodeID[edges[1]]=idCounter
                nodeDict["url"]=edges[1]
                nodeDict["page_rank"] = graph.get_pagerank(edges[1])
                idCounter+=1
                result["nodes"].append(nodeDict)
                nodes.add(edges[1])

            edgeDict = dict()
            edgeDict["source"] = nodeID[edges[0]]
            edgeDict["target"] = nodeID[edges[1]]
            result["edges"].append(edgeDict)
        return result
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))