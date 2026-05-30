<?php
declare(strict_types=1);

$root = sys_get_temp_dir() . '/php-autoload-demo-' . getmypid();
$classFile = $root . '/Domain/OrderId.php';
mkdir(dirname($classFile), 0777, true);

file_put_contents($classFile, <<<'PHP'
<?php
declare(strict_types=1);

namespace App\Domain;

final class OrderId
{
    public function __construct(private string $value)
    {
        if (!preg_match('/^ORD-\d{4}$/', $value)) {
            throw new \InvalidArgumentException('Order id must look like ORD-1001.');
        }
    }

    public function __toString(): string
    {
        return $this->value;
    }
}
PHP);

spl_autoload_register(function (string $class) use ($root): void {
    $prefix = 'App\\';
    if (!str_starts_with($class, $prefix)) {
        return;
    }

    $relativeClass = substr($class, strlen($prefix));
    $path = $root . '/' . str_replace('\\', '/', $relativeClass) . '.php';
    if (is_file($path)) {
        require $path;
    }
});

use App\Domain\OrderId;

echo 'loaded order: ' . new OrderId('ORD-1001') . PHP_EOL;

array_map('unlink', glob($root . '/Domain/*.php') ?: []);
@rmdir($root . '/Domain');
@rmdir($root);
