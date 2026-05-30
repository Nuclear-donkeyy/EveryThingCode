<?php

declare(strict_types=1);

namespace SyntaxTour;

use InvalidArgumentException;

const TAX_RATE = 0.0825;

readonly class LineItem
{
    public function __construct(
        public string $sku,
        public string $name,
        public string $category,
        public int $quantity,
        public float $unitPrice,
    ) {
        if ($this->sku === '' || $this->name === '' || $this->category === '') {
            throw new InvalidArgumentException('sku, name, and category are required');
        }

        if ($this->quantity <= 0) {
            throw new InvalidArgumentException('quantity must be positive');
        }

        if ($this->unitPrice < 0) {
            throw new InvalidArgumentException('unit price cannot be negative');
        }
    }

    public function subtotal(): float
    {
        return $this->quantity * $this->unitPrice;
    }
}

function parseQuantity(string $rawQuantity): int
{
    if (!ctype_digit($rawQuantity)) {
        throw new InvalidArgumentException("quantity must be digits, got $rawQuantity");
    }

    $quantity = (int) $rawQuantity;
    if ($quantity <= 0) {
        throw new InvalidArgumentException('quantity must be greater than zero');
    }

    return $quantity;
}

function statusLabel(string $status): string
{
    switch ($status) {
        case 'draft':
            return 'Draft order';
        case 'paid':
            return 'Paid and ready to ship';
        case 'cancelled':
            return 'Cancelled';
        default:
            return 'Unknown status';
    }
}

/**
 * @param list<LineItem> $items
 */
function orderSubtotal(array $items): float
{
    $total = 0.0;

    foreach ($items as $item) {
        $total += $item->subtotal();
    }

    return $total;
}

/**
 * @param list<LineItem> $items
 * @return array<string, float>
 */
function totalsByCategory(array $items): array
{
    $totals = [];

    foreach ($items as $item) {
        if (!array_key_exists($item->category, $totals)) {
            $totals[$item->category] = 0.0;
        }

        $totals[$item->category] += $item->subtotal();
    }

    return $totals;
}

function discountLabel(float $subtotal): string
{
    if ($subtotal >= 100) {
        return 'priority discount';
    } elseif ($subtotal >= 50) {
        return 'standard discount';
    }

    return 'no discount';
}

$customerName = 'Ada';
$status = 'paid';
$hasGiftWrap = true;
$note = null;

$lineItems = [
    new LineItem('BOOK-1', 'PHP Field Guide', 'books', 2, 24.50),
    new LineItem('MUG-7', 'Syntax Mug', 'gear', 1, 14.00),
    new LineItem('STK-3', 'Namespace Stickers', 'gear', 3, 2.50),
];

try {
    $giftQuantity = parseQuantity('two');
} catch (InvalidArgumentException $error) {
    echo "Recovered from invalid quantity: {$error->getMessage()}\n";
    $giftQuantity = 1;
}

$lineItems[] = new LineItem('GIFT-0', 'Fallback Gift Card', 'promo', $giftQuantity, 0.00);

$subtotal = orderSubtotal($lineItems);
$tax = $subtotal * TAX_RATE;
$grandTotal = $subtotal + $tax;

echo "Customer: $customerName\n";
echo 'Status: ' . statusLabel($status) . "\n";
echo 'Gift wrap: ' . ($hasGiftWrap ? 'yes' : 'no') . "\n";
echo 'Note: ' . ($note ?? 'none') . "\n";
echo sprintf("Tax rate: %.2f%%\n", TAX_RATE * 100);
echo 'Discount tier: ' . discountLabel($subtotal) . "\n\n";

foreach ($lineItems as $index => $item) {
    $lineNumber = $index + 1;
    echo sprintf(
        "%d. %s x%d = %.2f\n",
        $lineNumber,
        $item->name,
        $item->quantity,
        $item->subtotal(),
    );
}

echo "\nTotals by category:\n";
foreach (totalsByCategory($lineItems) as $category => $categorySubtotal) {
    echo sprintf("- %s: %.2f\n", $category, $categorySubtotal);
}

echo sprintf("\nSubtotal: %.2f\n", $subtotal);
echo sprintf("Tax: %.2f\n", $tax);
echo sprintf("Grand total: %.2f\n", $grandTotal);
