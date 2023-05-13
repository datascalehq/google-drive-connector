from typing import List
from pydantic import BaseSettings


class Config(BaseSettings):
    service_account_path: str = "../credentials/service_account.json"
    to_list_file_mime_types: List[str] = ["text/plain", "text/x-sql", "text/markdown", "text/csv"] + ["application/vnd.google-apps.folder"] # Note: not supported yet because this filter will exclude folder too
    to_read_content_mime_types: List[str] = ["text/plain", "text/x-sql", "text/markdown", "text/csv"]
    to_read_content_size_threshold: int = 100000 # byte


config = Config()
