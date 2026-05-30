import 'package:flutter/material.dart';

void main() {
  runApp(const StudyApp());
}

class StudyApp extends StatelessWidget {
  const StudyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'EverythingCode Flutter',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.teal),
        useMaterial3: true,
      ),
      home: const LearningBoard(),
    );
  }
}

class LearningTask {
  const LearningTask({
    required this.title,
    required this.note,
    this.done = false,
  });

  final String title;
  final String note;
  final bool done;

  LearningTask copyWith({bool? done}) {
    return LearningTask(
      title: title,
      note: note,
      done: done ?? this.done,
    );
  }
}

class LearningBoard extends StatefulWidget {
  const LearningBoard({super.key});

  @override
  State<LearningBoard> createState() => _LearningBoardState();
}

class _LearningBoardState extends State<LearningBoard> {
  List<LearningTask> _tasks = const [
    LearningTask(title: 'Dart syntax', note: 'Types, null safety, Future'),
    LearningTask(title: 'Flutter widgets', note: 'Build a declarative UI tree'),
    LearningTask(title: 'Shelf handlers', note: 'Compose HTTP middleware'),
  ];

  int get _completedCount => _tasks.where((task) => task.done).length;

  void _completeNext() {
    final index = _tasks.indexWhere((task) => !task.done);
    if (index == -1) {
      return;
    }

    setState(() {
      _tasks = [
        for (var i = 0; i < _tasks.length; i++)
          if (i == index) _tasks[i].copyWith(done: true) else _tasks[i],
      ];
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Dart learning board'),
        actions: [
          IconButton(
            tooltip: 'Complete next task',
            onPressed: _completeNext,
            icon: const Icon(Icons.check_circle_outline),
          ),
        ],
      ),
      body: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              '已完成 $_completedCount / ${_tasks.length}',
              style: Theme.of(context).textTheme.headlineSmall,
            ),
            const SizedBox(height: 12),
            Text(
              'Tap the check button to update state and rebuild the widget tree.',
              style: Theme.of(context).textTheme.bodyMedium,
            ),
            const SizedBox(height: 20),
            Expanded(
              child: ListView.separated(
                itemCount: _tasks.length,
                separatorBuilder: (_, __) => const Divider(),
                itemBuilder: (context, index) => TaskTile(task: _tasks[index]),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class TaskTile extends StatelessWidget {
  const TaskTile({required this.task, super.key});

  final LearningTask task;

  @override
  Widget build(BuildContext context) {
    return ListTile(
      contentPadding: EdgeInsets.zero,
      leading: Icon(
        task.done ? Icons.check_circle : Icons.radio_button_unchecked,
        color: task.done ? Colors.teal : Colors.grey,
      ),
      title: Text(
        task.title,
        style: TextStyle(
          decoration: task.done ? TextDecoration.lineThrough : null,
        ),
      ),
      subtitle: Text(task.note),
    );
  }
}
