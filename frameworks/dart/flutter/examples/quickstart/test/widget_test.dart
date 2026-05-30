import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

import 'package:everythingcode_flutter_quickstart/main.dart';

void main() {
  testWidgets('completes the next learning task', (tester) async {
    await tester.pumpWidget(const StudyApp());

    expect(find.text('已完成 0 / 3'), findsOneWidget);
    expect(find.text('Dart syntax'), findsOneWidget);

    await tester.tap(find.byIcon(Icons.check_circle_outline));
    await tester.pump();

    expect(find.text('已完成 1 / 3'), findsOneWidget);
    expect(find.byIcon(Icons.check_circle), findsOneWidget);
  });
}
