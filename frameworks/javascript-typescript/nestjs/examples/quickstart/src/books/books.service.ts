import { Injectable } from "@nestjs/common";
import { CreateBookDto } from "./dto/create-book.dto";

export type Book = {
  id: number;
  title: string;
  author: string;
};

@Injectable()
export class BooksService {
  private readonly books: Book[] = [
    { id: 1, title: "Learning NestJS Modules", author: "EveryThingCode" },
    { id: 2, title: "Dependency Injection in Practice", author: "EveryThingCode" }
  ];

  findAll(): Book[] {
    return this.books;
  }

  create(input: CreateBookDto): Book {
    const book: Book = {
      id: this.books.length + 1,
      title: input.title,
      author: input.author
    };

    this.books.push(book);
    return book;
  }
}
