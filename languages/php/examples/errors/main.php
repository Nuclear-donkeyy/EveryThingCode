<?php
declare(strict_types=1);

function loadName(bool $ok): string {
    if (!$ok) {
        throw new RuntimeException("config missing");
    }
    return "learner";
}

try {
    echo loadName(false) . PHP_EOL;
} catch (Throwable $error) {
    echo "recover: {$error->getMessage()}" . PHP_EOL;
}
