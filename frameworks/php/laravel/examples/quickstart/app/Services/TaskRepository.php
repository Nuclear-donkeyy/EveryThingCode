<?php

namespace App\Services;

use JsonException;

final class TaskRepository
{
    private string $file;

    public function __construct()
    {
        $this->file = dirname(__DIR__, 2) . '/storage/app/tasks.json';
    }

    /**
     * @return list<array{id:int,title:string,done:bool}>
     */
    public function all(): array
    {
        return $this->read();
    }

    /**
     * @return array{id:int,title:string,done:bool}|null
     */
    public function find(int $id): ?array
    {
        foreach ($this->read() as $task) {
            if ($task['id'] === $id) {
                return $task;
            }
        }

        return null;
    }

    /**
     * @return array{id:int,title:string,done:bool}
     */
    public function create(string $title, bool $done): array
    {
        $tasks = $this->read();
        $nextId = empty($tasks) ? 1 : max(array_column($tasks, 'id')) + 1;

        $task = [
            'id' => $nextId,
            'title' => $title,
            'done' => $done,
        ];

        $tasks[] = $task;
        $this->write($tasks);

        return $task;
    }

    /**
     * @return list<array{id:int,title:string,done:bool}>
     */
    private function read(): array
    {
        $this->ensureStore();

        try {
            $decoded = json_decode((string) file_get_contents($this->file), true, 512, JSON_THROW_ON_ERROR);
        } catch (JsonException) {
            $decoded = $this->seed();
            $this->write($decoded);
        }

        return is_array($decoded) ? array_values($decoded) : $this->seed();
    }

    /**
     * @param list<array{id:int,title:string,done:bool}> $tasks
     */
    private function write(array $tasks): void
    {
        $directory = dirname($this->file);

        if (! is_dir($directory)) {
            mkdir($directory, 0775, true);
        }

        file_put_contents($this->file, json_encode($tasks, JSON_PRETTY_PRINT | JSON_THROW_ON_ERROR));
    }

    private function ensureStore(): void
    {
        if (! file_exists($this->file)) {
            $this->write($this->seed());
        }
    }

    /**
     * @return list<array{id:int,title:string,done:bool}>
     */
    private function seed(): array
    {
        return [
            ['id' => 1, 'title' => 'Read Laravel routing', 'done' => false],
            ['id' => 2, 'title' => 'Trace service container injection', 'done' => true],
        ];
    }
}
