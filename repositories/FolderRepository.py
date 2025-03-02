from sqlmodel import Session, select
from fastapi import Depends
from config.db import get_db_session
from models.FolderModel import FolderCreate, Folder
from typing import List


class FolderRepository:
    session: Session

    def __init__(self, session: Session = Depends(get_db_session)):
        self.session = session

    def create(self, user_id: str, folder: FolderCreate) -> Folder:
        db_obj = Folder.model_validate(
            folder,
            update={"user_id": user_id},
        )

        self.session.add(db_obj)
        self.session.commit()
        self.session.refresh(db_obj)
        return db_obj

    def find_by_id(self, id: str) -> Folder:
        folder = self.session.get(Folder, id)
        return folder

    def find_by_user_id(self, user_id: str) -> List[Folder]:
        folders = self.session.exec(
            select(Folder).where(Folder.user_id == user_id)
        ).all()
        return folders

    def list(self, limit: int, start: int) -> Folder:
        folders = self.session.exec(select(Folder).offset(start).limit(limit)).all()
        return folders

    def update(self, folder: Folder, folder_update: FolderCreate) -> Folder:
        folder_data = folder_update.model_dump(exclude_unset=True)
        folder = Folder.sqlmodel_update(folder, obj=folder_data)
        self.session.add(folder)
        self.session.commit()
        self.session.refresh(folder)
        return folder

    def delete(self, id: str, folder: Folder) -> None:
        folder = self.session.get(Folder, id)
        self.session.delete(folder)
        self.session.commit()
        self.session.flush()
        return None
