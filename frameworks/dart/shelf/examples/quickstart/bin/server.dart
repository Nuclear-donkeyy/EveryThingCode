import 'dart:convert';
import 'dart:io';

import 'package:shelf/shelf.dart';
import 'package:shelf/shelf_io.dart';

Future<void> main() async {
  final port = int.tryParse(Platform.environment['PORT'] ?? '') ?? 8080;
  final handler = buildHandler(TaskStore.seeded());
  final server = await serve(handler, InternetAddress.loopbackIPv4, port);

  print('Serving at http://${server.address.host}:${server.port}');
}

Handler buildHandler(TaskStore store) {
  return Pipeline()
      .addMiddleware(logRequests())
      .addMiddleware(_jsonErrors())
      .addHandler(_tasksHandler(store));
}

Middleware _jsonErrors() {
  return (innerHandler) {
    return (request) async {
      try {
        return await innerHandler(request);
      } catch (error, stackTrace) {
        stderr.writeln('Unhandled request error: $error\n$stackTrace');
        return jsonResponse(
          {'error': 'internal_error', 'message': 'Unexpected server error'},
          statusCode: 500,
        );
      }
    };
  };
}

Handler _tasksHandler(TaskStore store) {
  return (request) async {
    final segments = request.url.pathSegments;

    if (request.method == 'GET' && _matches(segments, ['tasks'])) {
      return jsonResponse(store.list().map((task) => task.toJson()).toList());
    }

    if (request.method == 'POST' && _matches(segments, ['tasks'])) {
      final payload = await _readJsonObject(request);
      final title = payload['title'];
      if (title is! String || title.trim().isEmpty) {
        return jsonResponse(
          {'error': 'validation_error', 'message': 'title is required'},
          statusCode: 400,
        );
      }

      final task = store.create(title.trim());
      return jsonResponse(task.toJson(), statusCode: 201);
    }

    if (request.method == 'POST' &&
        segments.length == 3 &&
        segments[0] == 'tasks' &&
        segments[2] == 'complete') {
      final id = int.tryParse(segments[1]);
      if (id == null) {
        return jsonResponse({'error': 'invalid_task_id'}, statusCode: 400);
      }

      final task = store.complete(id);
      if (task == null) {
        return jsonResponse({'error': 'task_not_found'}, statusCode: 404);
      }

      return jsonResponse(task.toJson());
    }

    return jsonResponse({'error': 'not_found'}, statusCode: 404);
  };
}

bool _matches(List<String> actual, List<String> expected) {
  if (actual.length != expected.length) {
    return false;
  }

  for (var i = 0; i < expected.length; i++) {
    if (actual[i] != expected[i]) {
      return false;
    }
  }

  return true;
}

Future<Map<String, Object?>> _readJsonObject(Request request) async {
  final text = await request.readAsString();
  if (text.trim().isEmpty) {
    return {};
  }

  final decoded = jsonDecode(text);
  if (decoded is Map<String, Object?>) {
    return decoded;
  }

  return {};
}

Response jsonResponse(Object body, {int statusCode = 200}) {
  return Response(
    statusCode,
    body: jsonEncode(body),
    headers: const {'content-type': 'application/json'},
  );
}

class TaskStore {
  TaskStore(this._tasks);

  factory TaskStore.seeded() {
    return TaskStore([
      Task(id: 1, title: 'Read Dart async model'),
      Task(id: 2, title: 'Map a Shelf pipeline'),
    ]);
  }

  final List<Task> _tasks;

  List<Task> list() => List.unmodifiable(_tasks);

  Task create(String title) {
    final nextId = _tasks.isEmpty ? 1 : _tasks.last.id + 1;
    final task = Task(id: nextId, title: title);
    _tasks.add(task);
    return task;
  }

  Task? complete(int id) {
    final index = _tasks.indexWhere((task) => task.id == id);
    if (index == -1) {
      return null;
    }

    final updated = _tasks[index].copyWith(done: true);
    _tasks[index] = updated;
    return updated;
  }
}

class Task {
  const Task({
    required this.id,
    required this.title,
    this.done = false,
  });

  final int id;
  final String title;
  final bool done;

  Task copyWith({bool? done}) {
    return Task(id: id, title: title, done: done ?? this.done);
  }

  Map<String, Object?> toJson() {
    return {'id': id, 'title': title, 'done': done};
  }
}
