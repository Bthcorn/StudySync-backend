from fastapi import APIRouter, Depends, HTTPException
import uuid
from typing import List
from models.FolderModel import FolderCreate, FolderResponse
from services.FolderService import FolderService


router = APIRouter(prefix="/folder", tags=["folder"])


@router.post("/", response_model=FolderResponse)
def create_folder(
    user_id: uuid.UUID,
    folder_create: FolderCreate,
    folder_service: FolderService = Depends(),
):
    try:
        return folder_service.create_folder(user_id, folder_create)
    except HTTPException as e:
        raise e


@router.get("/", response_model=List[FolderResponse])
def index(
    pageSize: int = 10,
    startIndex: int = 0,
    folder_service: FolderService = Depends(),
):
    try:
        return folder_service.list_folders(pageSize, startIndex)
    except HTTPException as e:
        raise e


@router.get("/{folder_id}", response_model=FolderResponse)
def get_folder(
    folder_id: uuid.UUID,
    folder_service: FolderService = Depends(),
):
    try:
        return folder_service.get_folder(folder_id)
    except HTTPException as e:
        raise e


@router.get("/user/{user_id}", response_model=List[FolderResponse])
def get_user_folders(
    user_id: uuid.UUID,
    folder_service: FolderService = Depends(),
):
    try:
        return folder_service.get_user_folders(user_id)
    except HTTPException as e:
        raise e


@router.patch("/{folder_id}", response_model=FolderResponse)
def update_folder(
    folder_id: uuid.UUID,
    folder_create: FolderCreate,
    folder_service: FolderService = Depends(),
):
    try:
        return folder_service.update_folder(folder_id, folder_create)
    except HTTPException as e:
        raise e


@router.delete("/{folder_id}")
def delete_folder(
    folder_id: uuid.UUID,
    folder_service: FolderService = Depends(),
):
    try:
        return folder_service.delete_folder(folder_id)
    except HTTPException as e:
        raise e
