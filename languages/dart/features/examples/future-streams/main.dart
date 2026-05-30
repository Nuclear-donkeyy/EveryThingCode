import 'dart:async';

Future<String> fetchUserSummary(int id) async {
  await Future<void>.delayed(Duration(milliseconds: 120 + id * 30));
  return 'user-$id: active';
}

Stream<String> buildReportProgress(String reportName) async* {
  final steps = ['read cache', 'fetch remote delta', 'merge records'];

  for (final (index, step) in steps.indexed) {
    await Future<void>.delayed(const Duration(milliseconds: 90));
    yield '$reportName step ${index + 1}/${steps.length}: $step';
  }
}

Future<void> main() async {
  print('Loading user summaries with Future.wait...');
  final summaries = await Future.wait([
    fetchUserSummary(1),
    fetchUserSummary(2),
    fetchUserSummary(3),
  ]);

  for (final summary in summaries) {
    print('  $summary');
  }

  print('');
  print('Watching report progress with Stream...');
  await for (final event in buildReportProgress('daily-report')) {
    print('  $event');
  }

  print('Report stream is done.');
}
