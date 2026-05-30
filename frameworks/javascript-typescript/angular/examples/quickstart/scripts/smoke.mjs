import { readFileSync } from "node:fs";

const main = readFileSync(new URL("../src/main.ts", import.meta.url), "utf8");
const component = readFileSync(new URL("../src/app/app.component.ts", import.meta.url), "utf8");
const store = readFileSync(new URL("../src/app/task.store.ts", import.meta.url), "utf8");

const checks = [
  ["bootstraps standalone app", main.includes("bootstrapApplication")],
  ["uses injectable store", store.includes("@Injectable")],
  ["uses signals", store.includes("signal<") && store.includes("computed(")],
  ["injects store", component.includes("inject(TaskStore)")],
  ["uses control flow", component.includes("@for")]
];

const failed = checks.filter(([, ok]) => !ok);
if (failed.length) {
  console.error(failed.map(([name]) => `Missing: ${name}`).join("\n"));
  process.exit(1);
}

console.log("Angular quickstart smoke passed");
