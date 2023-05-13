from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from typing import Dict, Any

from schema import (
    GetGoogleDriveFilseAndFolderResponder,
    GetGoogleDriveFilesAndFoldersRequester,
    ErrorResponder,
)
from modules.google_drive_connector import get_file_and_folders
from modules.google_drive_connector import __init__ as google_drive_connector_init
from exception import SharedURLCantAccessException

app = FastAPI()
google_drive_connector_init()


@app.get(
    path="/files_and_folders",
    response_model=GetGoogleDriveFilseAndFolderResponder,
    responses={400: {"model": ErrorResponder}},
)
async def get_google_drive_files_and_folders(
    query_params: GetGoogleDriveFilesAndFoldersRequester = Depends(),
):
    try:
        structure_tree, file_nodes = get_file_and_folders(query_params.shared_url)
    except SharedURLCantAccessException as e:
        return JSONResponse(
            status_code=400,
            content={
                "error_code": "", # TODO: consider add error code if have multiple error to use
                "error_message": f"folder_id: {query_params.shared_url} cant access by server",
            },
        )

    response_dict = {"structure_tree": structure_tree, "file_nodes": file_nodes}
    return response_dict
