import { readFile } from "node:fs/promises";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");

const requiredFiles = [
  "package.json",
  "tsconfig.json",
  "src/main.ts",
  "src/app.module.ts",
  "src/books/books.module.ts",
  "src/books/books.controller.ts",
  "src/books/books.service.ts",
  "src/books/dto/create-book.dto.ts",
  "src/common/guards/api-key.guard.ts",
  "src/common/pipes/trim-title.pipe.ts"
];

const contents = new Map();

for (const file of requiredFiles) {
  contents.set(file, await readFile(resolve(root, file), "utf8"));
}

const checks = [
  ["src/app.module.ts", "@Module"],
  ["src/books/books.controller.ts", "@Controller(\"books\")"],
  ["src/books/books.service.ts", "@Injectable"],
  ["src/common/guards/api-key.guard.ts", "CanActivate"],
  ["src/common/pipes/trim-title.pipe.ts", "PipeTransform"]
];

for (const [file, expected] of checks) {
  if (!contents.get(file).includes(expected)) {
    throw new Error(`${file} does not contain ${expected}`);
  }
}

console.log("OK: NestJS quickstart structure looks ready");
