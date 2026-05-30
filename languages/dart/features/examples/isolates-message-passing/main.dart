import 'dart:isolate';

({int count, int sum}) countPrimes(int max) {
  var count = 0;
  var sum = 0;

  for (var value = 2; value <= max; value += 1) {
    if (isPrime(value)) {
      count += 1;
      sum += value;
    }
  }

  return (count: count, sum: sum);
}

bool isPrime(int value) {
  if (value < 2) {
    return false;
  }
  for (var factor = 2; factor * factor <= value; factor += 1) {
    if (value % factor == 0) {
      return false;
    }
  }
  return true;
}

Future<void> main() async {
  const max = 20000;

  print('Main isolate stays free to prepare UI or handle input.');
  final resultFuture = Isolate.run(() => countPrimes(max));

  print('Prime counting moved to a worker isolate.');
  final (:count, :sum) = await resultFuture;

  print('Found $count primes up to $max.');
  print('Their sum is $sum.');
}
