import { Injectable, computed, signal } from "@angular/core";

export type Task = {
  id: number;
  title: string;
  done: boolean;
};

@Injectable({ providedIn: "root" })
export class TaskStore {
  private readonly _tasks = signal<Task[]>([
    { id: 1, title: "Bootstrap a standalone component", done: true },
    { id: 2, title: "Inject a service into the component", done: false },
    { id: 3, title: "Update the template through signals", done: false }
  ]);

  readonly tasks = this._tasks.asReadonly();
  readonly completedCount = computed(() => this._tasks().filter((task) => task.done).length);

  toggle(id: number) {
    this._tasks.update((tasks) =>
      tasks.map((task) => (task.id === id ? { ...task, done: !task.done } : task))
    );
  }
}
