export type Task = {
  id: number;
  title: string;
  done: boolean;
};

export const tasks: Task[] = [
  { id: 1, title: "Load data in +page.ts", done: true },
  { id: 2, title: "Render data in +page.svelte", done: false },
  { id: 3, title: "Expose JSON in +server.ts", done: false }
];

export function listTasks() {
  return tasks;
}
