<script setup lang="ts">
import { computed, ref } from "vue";

type Task = {
  id: number;
  title: string;
  done: boolean;
};

const keyword = ref("");
const tasks = ref<Task[]>([
  { id: 1, title: "Read Vue SFC structure", done: true },
  { id: 2, title: "Use ref for source state", done: false },
  { id: 3, title: "Use computed for derived lists", done: false }
]);

const visibleTasks = computed(() => {
  const value = keyword.value.trim().toLowerCase();
  return value ? tasks.value.filter((task) => task.title.toLowerCase().includes(value)) : tasks.value;
});

const doneCount = computed(() => tasks.value.filter((task) => task.done).length);

function toggleTask(id: number) {
  const task = tasks.value.find((item) => item.id === id);
  if (task) {
    task.done = !task.done;
  }
}
</script>

<template>
  <main class="shell">
    <p class="eyebrow">Vue reactivity</p>
    <h1>响应式任务面板</h1>
    <p>已完成 {{ doneCount }} / {{ tasks.length }}</p>

    <label>
      <span>筛选任务</span>
      <input v-model="keyword" />
    </label>

    <ul>
      <li v-for="task in visibleTasks" :key="task.id" :class="{ done: task.done }">
        <span>{{ task.title }}</span>
        <button type="button" @click="toggleTask(task.id)">
          {{ task.done ? "重开" : "完成" }}
        </button>
      </li>
    </ul>
  </main>
</template>

<style scoped>
.shell {
  max-width: 720px;
  margin: 48px auto;
  padding: 28px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  font-family: Inter, system-ui, sans-serif;
}

.eyebrow {
  color: #047857;
  font-weight: 700;
}

label {
  display: grid;
  gap: 8px;
  margin: 24px 0;
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
</style>
