<?php
declare(strict_types=1);

function readEvents(): Generator
{
    yield ['level' => 'info', 'message' => 'request started'];
    yield ['level' => 'warning', 'message' => 'cache miss'];
    yield ['level' => 'error', 'message' => 'payment timeout'];
    yield ['level' => 'info', 'message' => 'request finished'];
}

function importantEvents(iterable $events): Generator
{
    foreach ($events as $event) {
        if (in_array($event['level'], ['warning', 'error'], true)) {
            yield strtoupper($event['level']) . ': ' . $event['message'];
        }
    }
}

foreach (importantEvents(readEvents()) as $line) {
    echo $line . PHP_EOL;
}
