import uuid
import ollama
from dataclasses import dataclass
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams,Distance,PointStruct
from qdrant_client.http import models
from settings import settings



def embed(chunk):
    resulte=ollama.embeddings(model=settings.EMBEDDING_MODEL,prompt=chunk)
    return resulte['embedding']


@dataclass
class Chunk():
    """Represents a chunk in the vector database"""

    index:int
    title:str
    chuck:str


class VectorKnowledgeBase:
    """a class for management of QDrant vector database
    """

    def __init__(self,collection_name:str,vector_size:int=1024,local_client:bool=True):
        
        self.collection_name=collection_name
        self.vector_size=vector_size
        if local_client:
            self.client=QdrantClient(url="http://localhost:6333",check_compatibility=False)
        else:
            self.client=QdrantClient(url=settings.QDRANT_URL,api_key=settings.QDRANT_API_KEY)
  
    def collection_exist(self):
        collections=self.client.get_collections().collections
        return (any(col.name==self.collection_name for col in collections))
    
    def delete_collection(self):
        if self.collection_exist():
            self.client.delete_collection(collection_name=self.collection_name)

    def create_collection(self):
        if not(self.collection_exist()):
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=self.vector_size,
                    distance=Distance.COSINE
                )
            )
            return True
        else:
            return False

    def search_knowlegbase(self,query:str,num_item:int):
        

        embedding=embed(query)

        results=self.client.search(
            collection_name=self.collection_name,
            query_vector=embedding,
            limit=num_item
        )

        chunks= [
            Chunk(
                chuck=item.payload['chunk'],
                title=item.payload['title'],
                index=item.payload['index'],
            ) 
            for item in results
        ]

        sorted_chunks = sorted(chunks, key=lambda c: c.index)
        return sorted_chunks

    def store_chunks(self,chunk_list:list[str],title):    

        points=self.dict2point(
            chunk_list=chunk_list,
            title=title
        )

        sublist_number=len(points)//15
        reminder_points=len(points)%15

        i=0
        print('number of sub chunks:',sublist_number)
        for i in range(sublist_number):
            print(f"sub chunk number:{i}")
            self.client.upsert(
                    collection_name=self.collection_name,
                    points=points[15*i:(i+1)*15]
                )
        if reminder_points!=0:
            if i!=0:
                self.client.upsert(
                        collection_name=self.collection_name,
                        points=points[15*(i+1):]
                    )
            else:
                self.client.upsert(
                        collection_name=self.collection_name,
                        points=points
                    )
            
    def dict2point(self,chunk_list:list[str],title:str):
        
        list_of_points=[]
        for i,chunk in enumerate(chunk_list):
            vector=embed(chunk)
            point_verctor=PointStruct(
                id=str(uuid.uuid4()),
                vector=vector,
                payload={
                    "index":(i+1),
                    "title":title,
                    "chunk":chunk,
                }
            )
            list_of_points.append(point_verctor)
        
        return list_of_points
    
    def new_chunk_store(self,chunk_list:list[str],title):

        j=0
        list_of_points=[]
        for i,chunk in enumerate(chunk_list):
            vector=embed(chunk)
            point_vector=PointStruct(
                id=str(uuid.uuid4()),
                vector=vector,
                payload={
                    "index":(i+1),
                    "title":title,
                    "chunk":chunk
                }
            )
            if i!=0 and i%15==0:
                self.client.upsert(
                    collection_name=self.collection_name,
                    points=list_of_points
                )
                list_of_points=[]
                print(f'15 sub chunks{j} is uploaded')
                j+=1
            else:
                list_of_points.append(point_vector)
               
    def get_all_collections(self):

        collections=self.client.get_collections().collections
        return  collections

    def get_points_by_field(self,field_name,value):

        filter_condition=models.Filter(
            must=[
                models.FieldCondition(
                    key=field_name,
                    match=models.MatchValue(value=value)
                )
            ]
        )
        points,_=self.client.scroll(
            collection_name=self.collection_name,
            scroll_filter=filter_condition,
            limit=30,
            with_payload=True,
            with_vectors=False
        )
        return [
            Chunk(
                chuck=item.payload['chunk'],
                title=item.payload['title'],
                index=item.payload['index'],
            ) 
            for item in points
        ]
    
    def Delete(self,field_name,filed_type,value):
        
        field_map={"str":models.PayloadSchemaType.KEYWORD}

        self.client.create_payload_index(
            collection_name=self.collection_name,
            field_name=field_name,
            field_schema=field_map[filed_type],  
            wait=True
        )

        self.client.delete(
            collection_name=self.collection_name,
            points_selector=models.FilterSelector(
                filter=models.Filter(
                    must=[
                        models.FieldCondition(
                            key=filed_type,
                            match=models.MatchValue(value=value)
                        )
                    ]
                )
            ),
            wait=True 
        )
        

      

    