mixin ScoredTask {
  int get earnedPoints;
  int get totalPoints;

  double get completionRatio {
    if (totalPoints == 0) {
      return 0;
    }
    return earnedPoints / totalPoints;
  }

  String get gradeLabel {
    final ratio = completionRatio;
    if (ratio >= 0.9) {
      return 'excellent';
    }
    if (ratio >= 0.7) {
      return 'steady';
    }
    return 'needs practice';
  }
}

class LessonTask with ScoredTask {
  const LessonTask({
    required this.title,
    required this.earnedPoints,
    required this.totalPoints,
  });

  final String title;

  @override
  final int earnedPoints;

  @override
  final int totalPoints;

  String summary() {
    return '$title: $earnedPoints/$totalPoints ($gradeLabel)';
  }
}

extension LessonTaskList on Iterable<LessonTask> {
  int get earnedTotal {
    return fold(0, (sum, task) => sum + task.earnedPoints);
  }

  int get possibleTotal {
    return fold(0, (sum, task) => sum + task.totalPoints);
  }

  LessonTask? get firstNeedsPractice {
    for (final task in this) {
      if (task.gradeLabel == 'needs practice') {
        return task;
      }
    }
    return null;
  }
}

void main() {
  const tasks = [
    LessonTask(title: 'Null safety quiz', earnedPoints: 9, totalPoints: 10),
    LessonTask(title: 'Future lab', earnedPoints: 7, totalPoints: 10),
    LessonTask(title: 'Mixin refactor', earnedPoints: 5, totalPoints: 10),
  ];

  for (final task in tasks) {
    print(task.summary());
  }

  print('Total: ${tasks.earnedTotal}/${tasks.possibleTotal}');
  final review = tasks.firstNeedsPractice;
  if (review != null) {
    print('Review next: ${review.title}');
  }
}
