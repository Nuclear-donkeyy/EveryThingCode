typedef ScoreRow = ({String name, int correct, int total});

({double ratio, String label}) grade(int correct, int total) {
  final ratio = total == 0 ? 0.0 : correct / total;
  final label = switch (ratio) {
    >= 0.9 => 'excellent',
    >= 0.7 => 'steady',
    _ => 'needs practice',
  };
  return (ratio: ratio, label: label);
}

(int earned, int possible) summarize(Iterable<ScoreRow> rows) {
  var earned = 0;
  var possible = 0;

  for (final (:correct, :total) in rows) {
    earned += correct;
    possible += total;
  }

  return (earned, possible);
}

void main() {
  const rows = <ScoreRow>[
    (name: 'Ada', correct: 9, total: 10),
    (name: 'Grace', correct: 7, total: 10),
    (name: 'Linus', correct: 5, total: 10),
  ];

  for (final (:name, :correct, :total) in rows) {
    final (:ratio, :label) = grade(correct, total);
    final percent = (ratio * 100).toStringAsFixed(0);
    print('$name scored $correct/$total ($percent%): $label');
  }

  final (earned, possible) = summarize(rows);
  print('Class total: $earned/$possible');
}
