<?php

use App\Services\TaskRepository;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;

Route::get('/tasks', function (TaskRepository $tasks) {
    return response()->json($tasks->all());
});

Route::post('/tasks', function (Request $request, TaskRepository $tasks) {
    $validated = validator($request->all(), [
        'title' => ['required', 'string', 'max:120'],
        'done' => ['sometimes', 'boolean'],
    ])->validate();

    $task = $tasks->create(
        title: $validated['title'],
        done: (bool) ($validated['done'] ?? false),
    );

    return response()->json($task, 201);
});

Route::get('/tasks/{id}', function (int $id, TaskRepository $tasks) {
    $task = $tasks->find($id);

    if ($task === null) {
        return response()->json(['message' => 'Task not found'], 404);
    }

    return response()->json($task);
})->whereNumber('id');
