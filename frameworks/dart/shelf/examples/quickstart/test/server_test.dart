import 'dart:convert';

import 'package:shelf/shelf.dart';
import 'package:test/test.dart';

import '../bin/server.dart';

void main() {
  late Handler handler;

  setUp(() {
    handler = buildHandler(TaskStore.seeded());
  });

  test('lists seeded tasks', () async {
    final response = await handler(
      Request('GET', Uri.parse('http://localhost/tasks')),
    );

    final body = jsonDecode(await response.readAsString()) as List<Object?>;

    expect(response.statusCode, 200);
    expect(body, hasLength(2));
  });

  test('creates a task from JSON body', () async {
    final response = await handler(
      Request(
        'POST',
        Uri.parse('http://localhost/tasks'),
        body: jsonEncode({'title': 'Write a Shelf test'}),
        headers: {'content-type': 'application/json'},
      ),
    );

    final body = jsonDecode(await response.readAsString()) as Map<String, Object?>;

    expect(response.statusCode, 201);
    expect(body['id'], 3);
    expect(body['title'], 'Write a Shelf test');
    expect(body['done'], false);
  });

  test('returns not found for unknown routes', () async {
    final response = await handler(
      Request('GET', Uri.parse('http://localhost/missing')),
    );

    expect(response.statusCode, 404);
  });
}
