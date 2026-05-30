import { inspect } from "node:util";

const language = "JavaScript";
const typedLayer = "TypeScript";
let runCount = 1;

const tasks = [
  {
    id: 101,
    title: "Sketch syntax guide",
    owner: "Ada",
    status: "done",
    estimateHours: 2,
    tags: ["docs", "syntax"],
  },
  {
    id: 102,
    title: "Build runnable tour",
    owner: "Grace",
    status: "active",
    estimateHours: 3,
    tags: ["node", "example"],
  },
  {
    id: 103,
    title: "Review async errors",
    owner: "Ada",
    status: "queued",
    estimateHours: null,
    tags: ["promise", "errors"],
  },
];

class TaskError extends Error {
  constructor(message, options = {}) {
    super(message, options);
    this.name = "TaskError";
    this.code = options.code ?? "TASK_ERROR";
  }
}

function describeRuntime(name = language) {
  return `${name} runs the program; ${typedLayer} checks many mistakes before it runs.`;
}

const formatTask = ({ id, title, owner, status, estimateHours }) => {
  const estimate = estimateHours == null ? "unestimated" : `${estimateHours}h`;
  return `#${id} ${title} (${owner}) - ${status}, ${estimate}`;
};

function statusLabel(status) {
  switch (status) {
    case "done":
      return "finished";
    case "active":
      return "in progress";
    case "queued":
      return "waiting";
    default:
      return `unknown:${status}`;
  }
}

function summarizeByOwner(taskList) {
  const counts = new Map();

  for (const task of taskList) {
    counts.set(task.owner, (counts.get(task.owner) ?? 0) + 1);
  }

  return counts;
}

function collectTags(taskList) {
  const tags = new Set();

  for (const task of taskList) {
    for (const tag of task.tags) {
      tags.add(tag);
    }
  }

  return [...tags].sort();
}

async function loadTaskById(taskList, id) {
  const task = await Promise.resolve(taskList.find((item) => item.id === id));

  if (!task) {
    throw new TaskError(`No task with id ${id}`, { code: "TASK_NOT_FOUND" });
  }

  return task;
}

export { TaskError, collectTags, formatTask, loadTaskById, summarizeByOwner };

console.log(`Run ${runCount}: ${describeRuntime()}`);
runCount += 1;

console.log("\nTasks");
for (const task of tasks) {
  if (task.status !== "done") {
    console.log(`- ${formatTask(task)} => ${statusLabel(task.status)}`);
  }
}

console.log("\nCollections");
console.log(`Owners: ${inspect([...summarizeByOwner(tasks)])}`);
console.log(`Tags: ${collectTags(tasks).join(", ")}`);

const activeTitles = tasks
  .filter((task) => task.status === "active")
  .map((task) => task.title.toUpperCase());

console.log(`Active titles: ${activeTitles.join(" | ")}`);

console.log("\nObjects are references");
const firstTask = tasks[0];
firstTask.status = "done";
console.log(`const binding stayed the same, object field is now: ${firstTask.status}`);

console.log("\nAsync and errors");
try {
  const [task] = await Promise.all([loadTaskById(tasks, 102)]);
  console.log(`Loaded: ${formatTask(task)}`);
  await loadTaskById(tasks, 999);
} catch (error) {
  if (error instanceof TaskError) {
    console.log(`Handled task error [${error.code}]: ${error.message}`);
  } else {
    throw error;
  }
} finally {
  console.log("Finished syntax tour.");
}
