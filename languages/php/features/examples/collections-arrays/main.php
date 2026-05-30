<?php
declare(strict_types=1);

final class CartLine
{
    public function __construct(
        public readonly string $sku,
        public readonly int $quantity,
        public readonly int $unitCents,
    ) {
        if ($sku === '') {
            throw new InvalidArgumentException('SKU cannot be empty.');
        }

        if ($quantity <= 0 || $unitCents < 0) {
            throw new InvalidArgumentException('Quantity and price must be valid.');
        }
    }

    public function subtotalCents(): int
    {
        return $this->quantity * $this->unitCents;
    }
}

$requestLines = [
    ['sku' => 'BOOK-1', 'quantity' => 2, 'unit_cents' => 1599],
    ['sku' => 'MUG-2', 'quantity' => 1, 'unit_cents' => 899],
    ['sku' => '', 'quantity' => 3, 'unit_cents' => 500],
    ['sku' => 'STICKER-3', 'quantity' => 0, 'unit_cents' => 199],
];

$validRows = array_values(array_filter(
    $requestLines,
    fn (array $row): bool => $row['sku'] !== '' && $row['quantity'] > 0 && $row['unit_cents'] >= 0,
));

$lines = array_map(
    fn (array $row): CartLine => new CartLine($row['sku'], $row['quantity'], $row['unit_cents']),
    $validRows,
);

$totalCents = array_reduce(
    $lines,
    fn (int $sum, CartLine $line): int => $sum + $line->subtotalCents(),
    0,
);

echo 'accepted lines:' . PHP_EOL;
foreach ($lines as $line) {
    echo "- {$line->sku} x {$line->quantity} = " . number_format($line->subtotalCents() / 100, 2) . PHP_EOL;
}

echo 'total = ' . number_format($totalCents / 100, 2) . PHP_EOL;
