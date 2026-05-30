<?php
declare(strict_types=1);

$courses = [
    ["name" => "types", "minutes" => 20],
    ["name" => "fibers", "minutes" => 30],
];

echo "total minutes = " . array_sum(array_column($courses, "minutes")) . PHP_EOL;
