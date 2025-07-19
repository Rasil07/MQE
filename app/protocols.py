from typing import Protocol,runtime_checkable
import sqlite3
from typing import Any,Optional,Dict,Tuple,List


@runtime_checkable
class DatabaseProtocol(Protocol):
    def initialize_tables(self,db_schema:str)->None:
        ...
    def connect(self)->sqlite3.Connection:
        ...
    def run(self,query:str,args:tuple=(),commit:bool=False,fetch_one:bool=False,fetch_all:bool=False,lastrowid:bool=False)->Optional[Any]:
        ...


@runtime_checkable
class FileModelProtocol(Protocol):
    def __init__(self,db_connection:DatabaseProtocol):
        ...
    def create(self,payload:Dict[str,Any])->int:
        ...
    def getById(self,upload_id:int)->Optional[Dict[str,Any]]:
        ...
    def getAll(self)->List[Dict[str,Any]]:
        ...

@runtime_checkable
class FileHelperProtocol(Protocol):
    allowed_extensions: set[str]
    max_file_size: int

    def pre_upload_check(self,file:Any)->Dict[str,Any]:
        ...
    def post_upload_check(self,file_name:str)->Dict[str,Any]:
        ...
    def save_file(self,file:Any)->Tuple[str,str]:
        ...
    def _allowed_file(self,filename:str)->bool:
        ...
    
    
@runtime_checkable
class FileServiceProtocol(Protocol):
    file_helper:FileHelperProtocol
    model:FileModelProtocol

    def upload_file(self,file:Any)->Dict[str,Any]:
        ...


@runtime_checkable
class FileControllerProtocol(Protocol):
    file_service:FileServiceProtocol

    def index(self)->str:
        ...
    def list_files(self)->str:
        ...
    def upload(self,file:Any)->Dict[str,Any]:
        ...
    
    
    
