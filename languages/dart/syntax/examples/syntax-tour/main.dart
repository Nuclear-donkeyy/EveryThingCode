import 'dart:async';

const appName = 'Dart syntax tour';

void logSection(String title) {
  print('\n== $title ==');
}

String describePriority(int priority) => switch (priority) {
      >= 8 => 'urgent',
      >= 5 => 'normal',
      _ => 'low',
    };

enum TaskStatus { todo, doing, done }

mixin HasLogLabel {
  String get logLabel;
}

class Task with HasLogLabel {
  Task({
    required this.title,
    required this.priority,
    this.status = TaskStatus.todo,
    this.owner,
  });

  final String title;
  final int priority;
  final TaskStatus status;
  final String? owner;

  bool get isHighPriority => priority >= 8;

  @override
  String get logLabel => '$title:${status.name}';

  @override
  String toString() {
    final ownerText = owner == null ? 'unassigned' : 'owner=$owner';
    return '$title [$ownerText, ${describePriority(priority)}]';
  }
}

sealed class ParseResult {}

class ParseSuccess extends ParseResult {
  ParseSuccess(this.task);

  final Task task;
}

class ParseFailure extends ParseResult {
  ParseFailure(this.message);

  final String message;
}

extension TitleCase on String {
  String toTaskTitle() {
    final trimmed = trim();
    if (trimmed.isEmpty) {
      return trimmed;
    }
    return '${trimmed[0].toUpperCase()}${trimmed.substring(1)}';
  }
}

ParseResult parseTask(String line, {TaskStatus defaultStatus = TaskStatus.todo}) {
  final parts = line.split('|');
  if (parts.length < 2) {
    return ParseFailure('missing "|" separator: $line');
  }

  final title = parts[0].toTaskTitle();
  if (title.isEmpty) {
    return ParseFailure('title must not be empty');
  }

  final priority = int.parse(parts[1]);
  final owner = parts.length >= 3 && parts[2].trim().isNotEmpty
      ? parts[2].trim()
      : null;

  return ParseSuccess(
    Task(
      title: title,
      priority: priority,
      status: defaultStatus,
      owner: owner,
    ),
  );
}

Map<String, int> summarizeByStatus(List<Task> tasks) {
  final counts = <String, int>{};
  for (final task in tasks) {
    counts.update(task.status.name, (value) => value + 1, ifAbsent: () => 1);
  }
  return counts;
}

({String title, int priority}) mostUrgent(List<Task> tasks) {
  if (tasks.isEmpty) {
    return (title: 'none', priority: 0);
  }

  var winner = tasks.first;
  for (var index = 1; index < tasks.length; index++) {
    final candidate = tasks[index];
    if (candidate.priority > winner.priority) {
      winner = candidate;
    }
  }
  return (title: winner.title, priority: winner.priority);
}

Future<int> fetchRemoteCount({required bool shouldFail}) async {
  await Future<void>.delayed(const Duration(milliseconds: 20));
  if (shouldFail) {
    throw StateError('remote counter unavailable');
  }
  return 42;
}

Stream<String> statusEvents() async* {
  yield 'queued';
  yield 'running';
  throw TimeoutException('stream timed out');
}

Future<void> main() async {
  logSection(appName);

  const maxItems = 5;
  final rawTasks = <String>[
    'write syntax guide|9|Jia',
    'review examples|6|',
    '|3|No title',
    'ship docs|not-a-number|Min',
  ];

  var accepted = 0;
  final tasks = <Task>[
    for (final line in rawTasks.take(maxItems))
      if (line.trim().isNotEmpty) ..._parseOne(line),
  ];

  accepted = tasks.length;
  print('accepted $accepted of ${rawTasks.length} rows');

  logSection('tasks');
  for (final task in tasks) {
    final marker = task.isHighPriority ? '!' : '-';
    print('$marker ${task.logLabel} -> $task');
  }

  logSection('summary');
  final counts = summarizeByStatus(tasks);
  for (final entry in counts.entries) {
    print('${entry.key}: ${entry.value}');
  }

  final urgent = mostUrgent(tasks);
  print('most urgent: ${urgent.title} (${urgent.priority})');

  logSection('future errors');
  try {
    final remoteCount = await fetchRemoteCount(shouldFail: false);
    print('remote count: $remoteCount');
    await fetchRemoteCount(shouldFail: true);
  } on StateError catch (error) {
    print('recovered future error: ${error.message}');
  } finally {
    print('future cleanup done');
  }

  logSection('stream errors');
  try {
    await for (final event in statusEvents()) {
      switch (event) {
        case 'queued':
          print('stream: waiting');
        case 'running':
          print('stream: active');
        default:
          print('stream: $event');
      }
    }
  } on TimeoutException catch (error) {
    print('recovered stream error: ${error.message}');
  }
}

List<Task> _parseOne(String line) {
  try {
    final result = parseTask(line);
    return switch (result) {
      ParseSuccess(task: final task) => [task],
      ParseFailure(message: final message) => _skip(line, message),
    };
  } on FormatException catch (error) {
    return _skip(line, 'invalid number: ${error.source}');
  }
}

List<Task> _skip(String line, String reason) {
  print('skip "$line" ($reason)');
  return const [];
}
