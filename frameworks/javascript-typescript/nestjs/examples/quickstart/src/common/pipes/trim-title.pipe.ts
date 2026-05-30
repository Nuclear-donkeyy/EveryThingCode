import { ArgumentMetadata, Injectable, PipeTransform } from "@nestjs/common";
import { CreateBookDto } from "../../books/dto/create-book.dto";

@Injectable()
export class TrimTitlePipe implements PipeTransform<CreateBookDto, CreateBookDto> {
  transform(value: CreateBookDto, _metadata: ArgumentMetadata): CreateBookDto {
    return {
      ...value,
      title: value.title.trim()
    };
  }
}
