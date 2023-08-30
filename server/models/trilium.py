from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TriliumStatus(BaseModel):
    online: bool
    appVersion: Optional[str] = None
    dbVersion: Optional[int] = None
    syncVersion: Optional[int] = None
    buildDate: Optional[datetime] = None
    buildRevision: Optional[str] = None
    dataDirectory: Optional[str] = None
    clipperProtocolVersion: Optional[str] = None
    utcDateTime: Optional[datetime] = None