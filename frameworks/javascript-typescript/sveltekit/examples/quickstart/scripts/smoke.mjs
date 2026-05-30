import { readFileSync } from "node:fs";

const page = readFileSync(new URL("../src/routes/+page.svelte", import.meta.url), "utf8");
const load = readFileSync(new URL("../src/routes/+page.ts", import.meta.url), "utf8");
const server = readFileSync(new URL("../src/routes/api/tasks/+server.ts", import.meta.url), "utf8");

const checks = [
  ["has load function", load.includes("export function load")],
  ["uses page data", page.includes("data.tasks")],
  ["uses svelte runes", page.includes("$state") && page.includes("$derived")],
  ["has server GET", server.includes("export function GET")],
  ["returns json", server.includes("json(")]
];

const failed = checks.filter(([, ok]) => !ok);
if (failed.length) {
  console.error(failed.map(([name]) => `Missing: ${name}`).join("\n"));
  process.exit(1);
}

console.log("SvelteKit quickstart smoke passed");
