import { json } from "@sveltejs/kit";
import { listTasks } from "$lib/tasks";

export function GET() {
  return json({ items: listTasks() });
}
