import { Body, Controller, Get, Post, UseGuards, UsePipes } from "@nestjs/common";
import { ApiKeyGuard } from "../common/guards/api-key.guard";
import { TrimTitlePipe } from "../common/pipes/trim-title.pipe";
import { BooksService } from "./books.service";
import { CreateBookDto } from "./dto/create-book.dto";

@Controller("books")
export class BooksController {
  constructor(private readonly booksService: BooksService) {}

  @Get()
  findAll() {
    return this.booksService.findAll();
  }

  @Post()
  @UseGuards(ApiKeyGuard)
  @UsePipes(TrimTitlePipe)
  create(@Body() input: CreateBookDto) {
    return this.booksService.create(input);
  }
}
