<script lang="ts">
  import type { Task } from "$lib/tasks";

  type PageData = {
    tasks: Task[];
  };

  let { data }: { data: PageData } = $props();
  let keyword = $state("");

  const visibleTasks = $derived(
    keyword.trim()
      ? data.tasks.filter((task) => task.title.toLowerCase().includes(keyword.trim().toLowerCase()))
      : data.tasks
  );
  const completedCount = $derived(data.tasks.filter((task) => task.done).length);
</script>

<main class="shell">
  <p class="eyebrow">SvelteKit file routes</p>
  <h1>任务页面</h1>
  <p>已完成 {completedCount} / {data.tasks.length}</p>

  <label>
    <span>筛选任务</span>
    <input bind:value={keyword} />
  </label>

  <ul>
    {#each visibleTasks as task (task.id)}
      <li class:done={task.done}>{task.title}</li>
    {/each}
  </ul>
</main>

<style>
  .shell {
    max-width: 720px;
    margin: 48px auto;
    padding: 28px;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    font-family: Inter, system-ui, sans-serif;
  }
  .eyebrow {
    color: #7c3aed;
    font-weight: 700;
  }
  label {
    display: grid;
    gap: 8px;
    margin: 24px 0;
  }
  .done {
    color: #6b7280;
    text-decoration: line-through;
  }
</style>
