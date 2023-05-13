from __future__ import annotations
from pydantic import BaseModel, validator
from typing import List, Optional
from urllib.parse import urlparse


class GetGoogleDriveFilesAndFoldersRequester(BaseModel):
    shared_url: str
    
    # TODO: consider handle missing value or wrong value and raise exception follow ErrorResponder
    @validator("shared_url")
    def validate_and_transform_shared_url(cls, v):
        try:
            path = urlparse(v).path
            folder_id = path.split("/")[-1]
        except Exception as e:
            raise e
        return folder_id


class GetGoogleDriveFilseAndFolderResponder(BaseModel):
    structure_tree: GoogleDriveStructureTree
    file_nodes: List[FilledContentGoogleDriveFileNode]


class GoogleDriveStructureTree(BaseModel):
    __root__: List[GoogleDriveStructureTreeNode]


class GoogleDriveStructureTreeNode(BaseModel):
    name: str
    id: str
    is_folder: bool
    mimeType: Optional[str]
    childrens: Optional[List[GoogleDriveStructureTreeNode]]


class UnfilledContentGoogleDriveFileNode(BaseModel):
    name: str
    id: str
    mimeType: str
    size: str


class FilledContentGoogleDriveFileNode(UnfilledContentGoogleDriveFileNode):
    content: Optional[str]


class ErrorResponder(BaseModel):
    error_code: str
    error_message: str


GetGoogleDriveFilseAndFolderResponder.update_forward_refs()
GoogleDriveStructureTree.update_forward_refs()
GoogleDriveStructureTreeNode.update_forward_refs()
