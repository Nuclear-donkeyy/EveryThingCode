String loadName(bool ok) {
  if (!ok) {
    throw StateError('config missing');
  }
  return 'learner';
}

void main() {
  try {
    print(loadName(false));
  } on StateError catch (error) {
    print('recover: ${error.message}');
  }
}
