import { Component, inject } from "@angular/core";
import { TaskStore } from "./task.store";

@Component({
  selector: "app-root",
  standalone: true,
  template: `
    <main class="shell">
      <p class="eyebrow">Angular platform thinking</p>
      <h1>任务工作台</h1>
      <p>已完成 {{ store.completedCount() }} / {{ store.tasks().length }}</p>

      <ul>
        @for (task of store.tasks(); track task.id) {
          <li [class.done]="task.done">
            <span>{{ task.title }}</span>
            <button type="button" (click)="toggle(task.id)">
              {{ task.done ? "重开" : "完成" }}
            </button>
          </li>
        }
      </ul>
    </main>
  `,
  styles: [
    `
      .shell {
        max-width: 760px;
        margin: 48px auto;
        padding: 28px;
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        font-family: Inter, system-ui, sans-serif;
      }
      .eyebrow {
        color: #b45309;
        font-weight: 700;
      }
      li {
        display: flex;
        justify-content: space-between;
        padding: 10px 0;
      }
      .done span {
        color: #6b7280;
        text-decoration: line-through;
      }
    `
  ]
})
export class AppComponent {
  protected readonly store = inject(TaskStore);

  protected toggle(id: number) {
    this.store.toggle(id);
  }
}
