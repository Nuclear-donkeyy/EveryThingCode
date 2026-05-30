import { readFileSync } from "node:fs";

const app = readFileSync(new URL("../src/App.tsx", import.meta.url), "utf8");
const entry = readFileSync(new URL("../src/main.tsx", import.meta.url), "utf8");

const checks = [
  ["uses useState", app.includes("useState")],
  ["derives visible tasks", app.includes("visibleTasks")],
  ["passes props to TaskList", app.includes("<TaskList")],
  ["mounts with createRoot", entry.includes("createRoot")]
];

const failed = checks.filter(([, ok]) => !ok);
if (failed.length) {
  console.error(failed.map(([name]) => `Missing: ${name}`).join("\n"));
  process.exit(1);
}

console.log("React quickstart smoke passed");
