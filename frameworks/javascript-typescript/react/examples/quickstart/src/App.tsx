import { useMemo, useState } from "react";

type Task = {
  id: number;
  title: string;
  done: boolean;
};

const initialTasks: Task[] = [
  { id: 1, title: "Break UI into components", done: true },
  { id: 2, title: "Keep source state in one owner", done: false },
  { id: 3, title: "Derive visible tasks while rendering", done: false }
];

export function App() {
  const [tasks, setTasks] = useState(initialTasks);
  const [filter, setFilter] = useState("");

  const visibleTasks = useMemo(() => {
    const keyword = filter.trim().toLowerCase();
    return keyword ? tasks.filter((task) => task.title.toLowerCase().includes(keyword)) : tasks;
  }, [filter, tasks]);

  const completed = tasks.filter((task) => task.done).length;

  function toggleTask(id: number) {
    setTasks((current) =>
      current.map((task) => (task.id === id ? { ...task, done: !task.done } : task))
    );
  }

  return (
    <main className="app-shell">
      <header>
        <p className="eyebrow">React state as UI source</p>
        <h1>任务看板</h1>
        <p>
          已完成 {completed} / {tasks.length}。改变 state，界面会随之重新计算。
        </p>
      </header>

      <label className="search">
        <span>筛选任务</span>
        <input value={filter} onChange={(event) => setFilter(event.target.value)} />
      </label>

      <TaskList tasks={visibleTasks} onToggle={toggleTask} />
    </main>
  );
}

function TaskList({ tasks, onToggle }: { tasks: Task[]; onToggle: (id: number) => void }) {
  if (tasks.length === 0) {
    return <p className="empty">没有匹配的任务。</p>;
  }

  return (
    <ul className="task-list">
      {tasks.map((task) => (
        <TaskItem key={task.id} task={task} onToggle={onToggle} />
      ))}
    </ul>
  );
}

function TaskItem({ task, onToggle }: { task: Task; onToggle: (id: number) => void }) {
  return (
    <li className={task.done ? "task done" : "task"}>
      <span>{task.title}</span>
      <button type="button" onClick={() => onToggle(task.id)}>
        {task.done ? "重开" : "完成"}
      </button>
    </li>
  );
}
