import { Readable } from "node:stream";

const wait = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

async function* delayedEvents() {
  const events = [
    { kind: "view", user: "ada" },
    { kind: "click", user: "ada" },
    { kind: "view", user: "grace" },
    { kind: "purchase", user: "ada" },
  ];

  for (const event of events) {
    await wait(20);
    console.log("source ready", event);
    yield event;
  }
}

const stream = Readable.from(delayedEvents());
const counts = new Map();

for await (const event of stream) {
  console.log("consumer got", event);
  counts.set(event.kind, (counts.get(event.kind) ?? 0) + 1);
  console.log("counts snapshot", Object.fromEntries(counts));
}

console.log("final counts", Object.fromEntries(counts));
