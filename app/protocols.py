from typing import Protocol,runtime_checkable
import sqlite3
from typing import Any,Optional,Dict,Tuple,List
from flask import Response


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

    def validate_file(self,file:Any)->Dict[str,Any]:
        ...
    def _allowed_file(self,filename:str)->bool:
        ...
    def generate_unique_filename(self,file:Any)->Tuple[str,str]:
        ...
    def process_file(self,file:Any)->Dict[str,Any]:
        ...
    
@runtime_checkable
class FileServiceProtocol(Protocol):
    file_helper:FileHelperProtocol
    model:FileModelProtocol

    def upload_file(self,file:Any)->Dict[str,Any]:
        ...
    def generate_report(self,file:Any)->Dict[str,Any]:
        ...
    def download_report(self)->bytes:
        ...
    def delete_file(self)->Optional[None]:
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
    def generate_report(self,file:Any)->Dict[str,Any]:
        ...
    def download_report(self)->Response:
        ...
    
    
