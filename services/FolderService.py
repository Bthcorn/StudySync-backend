from repositories.FolderRepository import FolderRepository
from repositories.UserRepository import UserRepository
from fastapi import Depends, HTTPException, status
from models.FolderModel import FolderCreate, FolderResponse
from typing import List


class FolderService:
    folder_repository: FolderRepository
    user_repository: UserRepository

    def __init__(
        self,
        folder_repository: FolderRepository = Depends(),
        user_repository: UserRepository = Depends(),
    ):
        self.folder_repository = folder_repository
        self.user_repository = user_repository

    def create_folder(
        self, user_id: str, folder_create: FolderCreate
    ) -> FolderResponse:
        user = self.user_repository.find_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        return self.folder_repository.create(user_id, folder_create)

    def get_user_folders(self, user_id: str) -> List[FolderResponse]:
        user = self.user_repository.find_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        return self.folder_repository.find_by_user_id(user_id)

    def list_folders(self, pageSize: int, startIndex: int) -> List[FolderResponse]:
        return self.folder_repository.list(pageSize, startIndex)

    def get_folder(self, folder_id: str) -> FolderResponse:
        folder = self.folder_repository.find_by_id(folder_id)
        if not folder:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Folder not found"
            )

        return folder

    def update_folder(
        self, folder_id: str, folder_create: FolderCreate
    ) -> FolderResponse:
        folder = self.folder_repository.find_by_id(folder_id)
        if not folder:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Folder not found"
            )

        return self.folder_repository.update(folder, folder_create)

    def delete_folder(self, folder_id: str) -> None:
        folder = self.folder_repository.find_by_id(folder_id)
        if not folder:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Folder not found"
            )

        return self.folder_repository.delete(folder_id, folder)
