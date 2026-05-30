<?php
declare(strict_types=1);

final class Money
{
    public function __construct(
        public readonly int $cents,
        public readonly string $currency,
    ) {
        if ($cents < 0) {
            throw new InvalidArgumentException('Money cannot be negative.');
        }

        if (!preg_match('/^[A-Z]{3}$/', $currency)) {
            throw new InvalidArgumentException('Currency must be a three-letter code.');
        }
    }

    public function multiply(int $quantity): self
    {
        if ($quantity <= 0) {
            throw new InvalidArgumentException('Quantity must be positive.');
        }

        return new self($this->cents * $quantity, $this->currency);
    }

    public function format(): string
    {
        return sprintf('%s %.2f', $this->currency, $this->cents / 100);
    }
}

function lineSubtotal(Money $unitPrice, int $quantity): Money
{
    return $unitPrice->multiply($quantity);
}

echo 'subtotal: ' . lineSubtotal(new Money(1250, 'USD'), 4)->format() . PHP_EOL;

try {
    lineSubtotal(new Money(1250, 'USD'), '2');
} catch (TypeError $error) {
    echo 'strict_types caught: ' . $error->getMessage() . PHP_EOL;
}

try {
    new Money(-100, 'USD');
} catch (InvalidArgumentException $error) {
    echo 'value object caught: ' . $error->getMessage() . PHP_EOL;
}
