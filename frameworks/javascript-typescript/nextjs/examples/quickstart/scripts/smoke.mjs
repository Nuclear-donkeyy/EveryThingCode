import { readFile } from "node:fs/promises";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");

const requiredFiles = [
  "package.json",
  "tsconfig.json",
  "next.config.ts",
  "src/app/layout.tsx",
  "src/app/page.tsx",
  "src/app/api/posts/route.ts",
  "src/lib/posts.ts"
];

const contents = new Map();

for (const file of requiredFiles) {
  contents.set(file, await readFile(resolve(root, file), "utf8"));
}

const checks = [
  ["package.json", '"dev": "next dev"'],
  ["src/app/page.tsx", "getPosts"],
  ["src/app/api/posts/route.ts", "export async function GET"],
  ["src/lib/posts.ts", "export async function getPosts"]
];

for (const [file, expected] of checks) {
  if (!contents.get(file).includes(expected)) {
    throw new Error(`${file} does not contain ${expected}`);
  }
}

console.log("OK: Next.js quickstart structure looks ready");
