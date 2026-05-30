import { readFileSync } from "node:fs";

const app = readFileSync(new URL("../src/App.vue", import.meta.url), "utf8");
const entry = readFileSync(new URL("../src/main.ts", import.meta.url), "utf8");

const checks = [
  ["uses createApp", entry.includes("createApp")],
  ["uses ref", app.includes("ref(")],
  ["uses computed", app.includes("computed(")],
  ["uses v-model", app.includes("v-model")],
  ["uses v-for", app.includes("v-for")]
];

const failed = checks.filter(([, ok]) => !ok);
if (failed.length) {
  console.error(failed.map(([name]) => `Missing: ${name}`).join("\n"));
  process.exit(1);
}

console.log("Vue quickstart smoke passed");
