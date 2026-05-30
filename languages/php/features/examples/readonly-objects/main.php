<?php
declare(strict_types=1);

final class ReportOptions
{
    public function __construct(
        public readonly string $from,
        public readonly string $to,
        public readonly string $format,
    ) {
        if ($from > $to) {
            throw new InvalidArgumentException('from must be before to.');
        }

        if (!in_array($format, ['csv', 'json'], true)) {
            throw new InvalidArgumentException('format must be csv or json.');
        }
    }
}

function describeReport(ReportOptions $options): string
{
    return sprintf('report %s..%s as %s', $options->from, $options->to, $options->format);
}

$options = new ReportOptions('2026-05-01', '2026-05-30', 'json');
echo describeReport($options) . PHP_EOL;

try {
    $options->format = 'csv';
} catch (Error $error) {
    echo 'readonly caught: ' . $error->getMessage() . PHP_EOL;
}
