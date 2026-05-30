<?php
declare(strict_types=1);

final class Response
{
    public function __construct(
        public readonly int $status,
        public readonly string $body,
    ) {
    }
}

function reserveSeat(array $request): Response
{
    $name = trim($request['name'] ?? '');
    $seats = $request['seats'] ?? 0;

    if ($name === '') {
        throw new DomainException('Name is required.');
    }

    if (!is_int($seats)) {
        throw new TypeError('Seats must be an integer.');
    }

    if ($seats < 1 || $seats > 4) {
        throw new DomainException('You can reserve between 1 and 4 seats.');
    }

    return new Response(200, "Reserved {$seats} seat(s) for {$name}.");
}

function handleRequest(array $request): Response
{
    echo 'open request resources' . PHP_EOL;

    try {
        return reserveSeat($request);
    } catch (DomainException $error) {
        return new Response(422, 'Cannot process request: ' . $error->getMessage());
    } catch (Throwable $error) {
        error_log('unexpected failure: ' . get_class($error) . ' ' . $error->getMessage());
        return new Response(500, 'Internal server error.');
    } finally {
        echo 'close request resources' . PHP_EOL;
    }
}

$requests = [
    ['name' => 'Ada', 'seats' => 2],
    ['name' => '', 'seats' => 1],
    ['name' => 'Grace', 'seats' => 'two'],
];

foreach ($requests as $index => $request) {
    echo "request #" . ($index + 1) . PHP_EOL;
    $response = handleRequest($request);
    echo "HTTP {$response->status}: {$response->body}" . PHP_EOL . PHP_EOL;
}
