from __future__ import annotations

from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query, status
from pydantic import BaseModel, Field


class BookCreate(BaseModel):
    title: str = Field(min_length=1, examples=["FastAPI type driven APIs"])
    author: str = Field(min_length=1, examples=["EveryThingCode"])


class BookRead(BookCreate):
    id: int


class BookRepository:
    def __init__(self) -> None:
        self._books: dict[int, BookRead] = {
            1: BookRead(id=1, title="FastAPI type driven APIs", author="EveryThingCode")
        }
        self._next_id = 2

    def reset(self) -> None:
        self.__init__()

    def list(self, q: str | None = None) -> list[BookRead]:
        books = list(self._books.values())
        if q is None:
            return books
        keyword = q.casefold()
        return [
            book
            for book in books
            if keyword in book.title.casefold() or keyword in book.author.casefold()
        ]

    def create(self, data: BookCreate) -> BookRead:
        book = BookRead(id=self._next_id, **data.model_dump())
        self._books[book.id] = book
        self._next_id += 1
        return book

    def get(self, book_id: int) -> BookRead | None:
        return self._books.get(book_id)


repository = BookRepository()


def get_repository() -> BookRepository:
    return repository


app = FastAPI(
    title="EveryThingCode FastAPI Quickstart",
    summary="A tiny type-driven books API for learning FastAPI.",
)


@app.get("/books", response_model=list[BookRead])
def list_books(
    repository: Annotated[BookRepository, Depends(get_repository)],
    q: Annotated[str | None, Query(description="Filter by title or author")] = None,
) -> list[BookRead]:
    return repository.list(q)


@app.post("/books", response_model=BookRead, status_code=status.HTTP_201_CREATED)
def create_book(
    book: BookCreate,
    repository: Annotated[BookRepository, Depends(get_repository)],
) -> BookRead:
    return repository.create(book)


@app.get("/books/{book_id}", response_model=BookRead)
def read_book(
    book_id: int,
    repository: Annotated[BookRepository, Depends(get_repository)],
) -> BookRead:
    book = repository.get(book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="book not found")
    return book
