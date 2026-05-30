<?php

namespace App\Controller;

use App\Service\TaskRepository;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\Routing\Attribute\Route;

final class TaskController extends AbstractController
{
    #[Route('/tasks', methods: ['GET'])]
    public function list(TaskRepository $tasks): JsonResponse
    {
        return $this->json($tasks->all());
    }

    #[Route('/tasks', methods: ['POST'])]
    public function create(Request $request, TaskRepository $tasks): JsonResponse
    {
        $payload = json_decode($request->getContent() ?: '{}', true);

        if (! is_array($payload)) {
            return $this->json(['message' => 'Request body must be a JSON object'], 400);
        }

        $title = trim((string) ($payload['title'] ?? ''));

        if ($title === '') {
            return $this->json(['message' => 'title is required'], 422);
        }

        $task = $tasks->create($title, (bool) ($payload['done'] ?? false));

        return $this->json($task, 201);
    }

    #[Route('/tasks/{id<\d+>}', methods: ['GET'])]
    public function show(int $id, TaskRepository $tasks): JsonResponse
    {
        $task = $tasks->find($id);

        if ($task === null) {
            return $this->json(['message' => 'Task not found'], 404);
        }

        return $this->json($task);
    }
}
