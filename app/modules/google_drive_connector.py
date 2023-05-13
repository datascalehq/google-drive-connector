import copy
from typing import Tuple, List
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.service_account import Credentials

from config import config
from schema import (
    GoogleDriveStructureTree,
    UnfilledContentGoogleDriveFileNode,
    FilledContentGoogleDriveFileNode,
)
from exception import SharedURLCantAccessException


SERVICE = None


def __init__() -> None:
    """Init googledrive service"""
    global SERVICE
    creds = Credentials.from_service_account_file(config.service_account_path)
    service = build("drive", "v3", credentials=creds)
    SERVICE = service


def get_file_and_folders(
    folder_id: str,
) -> Tuple[GoogleDriveStructureTree, FilledContentGoogleDriveFileNode]:
    """Get structure tree and file_nodes and fill content to file_nodes

    Args:
        folder_id (str):

    Returns:
        Tuple[GoogleDriveStructureTree, FilledContentGoogleDriveFileNode]:
    """
    structure_tree, file_nodes = _list_structure_tree_and_file_nodes(
        folder_id=folder_id
    )
    # TODO: consider to multithread for improve performance (if deployed machine have resouce)
    file_nodes = [
        _fill_content_to_file_node(file_node)
        if _should_read_content(file_node)
        else file_node
        for file_node in file_nodes
    ]

    return structure_tree, file_nodes

def _should_read_content(file_node: UnfilledContentGoogleDriveFileNode) -> bool:
    return  (file_node["mimeType"] in config.to_read_content_mime_types) and (int(file_node["size"]) <= config.to_read_content_size_threshold)

   
def _list_structure_tree_and_file_nodes(
    folder_id: str,
) -> Tuple[GoogleDriveStructureTree, List[UnfilledContentGoogleDriveFileNode]]:
    """Get structure_tree and unfilled_content_file_nodes under folder_id in recursive nested
    Note: This function modified from GPT4 output

    Args:
        folder_id (str):

    Returns:
        Tuple[GoogleDriveStructureTree, List[UnfilledContentGoogleDriveFileNode]]
    """
    # construct query and call google client api
    query = f"'{folder_id}' in parents and trashed=false and"
    query += _get_filter_mime_type_query(mime_types=config.to_list_file_mime_types)
    try:
        results = (
            SERVICE.files()
            .list(q=query, fields="nextPageToken, files(id, name, mimeType, size)")
            .execute()
        )
    except HttpError as e:
        if e.status_code == 404:
            raise SharedURLCantAccessException(f"{folder_id=}")
        else:
            raise e

    items = results.get("files", [])

    # recursive call folder vs add file node
    structure_nodes = []
    file_nodes = []
    for item in items:
        if item["mimeType"] == "application/vnd.google-apps.folder":
            # since it's folder then get children of this folder id
            childrens, child_file_nodes = _list_structure_tree_and_file_nodes(
                folder_id=item["id"]
            )
            # construct node
            node = item
            node["is_folder"] = True
            node["childrens"] = childrens
            # concat file_nodes on curr level with child level
            file_nodes = file_nodes + child_file_nodes

        else:
            # since it's file then just construct node
            node = item
            node["is_folder"] = False
            # concat file_node to curr level
            # use copy.deepcopy because dont want structure_tree and file_nodes reference to same object, it will effect when fill content
            file_nodes.append(copy.deepcopy(node))
            # file_nodes.append(node)
        structure_nodes.append(node)

    return structure_nodes, file_nodes


def _fill_content_to_file_node(
    file_node: UnfilledContentGoogleDriveFileNode,
) -> FilledContentGoogleDriveFileNode:
    """Fill content to file node

    Args:
        file_node (UnfilledContentGoogleDriveFileNode):

    Returns:
        FilledContentGoogleDriveFileNode:
    """
    file_node["content"] = _read_file_content(file_node["id"])
    return file_node


def _read_file_content(file_id: str) -> str:
    """Read string content from file_id
    Args:
        file_id (str):

    Returns:
        str:
    """
    response = SERVICE.files().get_media(fileId=file_id).execute()
    content_string = response.decode("utf-8")
    return content_string


def _get_filter_mime_type_query(mime_types: List[str]) -> str:
    """Generate query that use for filter interested mime types

    Args:
        mime_types (List[str]):

    Returns:
        str:
    """
    query = "("
    for i, mime_type in enumerate(mime_types):
        query += f" mimeType = '{mime_type}'"
        if i != len(mime_types) - 1:
            query += " or"
    query += " )"
    return query
