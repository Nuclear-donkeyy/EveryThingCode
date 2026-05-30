import { listTasks } from "$lib/tasks";

export function load() {
  return {
    tasks: listTasks()
  };
}
