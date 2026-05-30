using System.Globalization;
using Storefront.SyntaxTour;

const decimal TaxRate = 0.08m;

var products = new List<Product>
{
    new("BK-001", "C# Field Guide", 39.90m, 4),
    new("KB-204", "Mechanical Keyboard", 129.00m, 2),
    new("HD-404", "Noise-canceling Headphones", 89.50m, 0)
};

var productBySku = products.ToDictionary(product => product.Sku);
string? maybeCoupon = args.FirstOrDefault();

using var ledger = new InventoryLedger("syntax-tour");

Console.WriteLine($"Run started at {DateTimeOffset.Now:yyyy-MM-dd HH:mm:ss zzz}");
Console.WriteLine($"Coupon: {DescribeCoupon(maybeCoupon)}");

var availableProducts = products
    .Where(product => product.Stock > 0)
    .Select(product => product with { Name = product.Name.Trim() })
    .ToList();

foreach (var product in products)
{
    var stockLabel = product.Stock switch
    {
        0 => "sold out",
        <= 2 => "low stock",
        _ => "available"
    };

    Console.WriteLine($"{product.Sku}: {product.Name} is {stockLabel}");
}

try
{
    var selectedSku = "BK-001";
    var selected = FindProduct(productBySku, selectedSku);
    var subtotal = CalculateSubtotal(availableProducts);
    var couponDiscount = maybeCoupon is "VIP" ? 0.15m : 0m;
    var total = ApplyTax(subtotal * (1 - couponDiscount), TaxRate);

    ledger.RecordSale(selected, total);

    Console.WriteLine(selected.Describe());
    Console.WriteLine($"Subtotal: {FormatMoney(subtotal)}");
    Console.WriteLine($"Total with tax: {FormatMoney(total)}");

    _ = FindProduct(productBySku, "MISSING");
}
catch (KeyNotFoundException ex)
{
    Console.WriteLine($"Lookup failed: {ex.Message}");
}

static Product FindProduct(Dictionary<string, Product> productsBySku, string sku)
{
    if (productsBySku.TryGetValue(sku, out var product))
    {
        return product;
    }

    throw new KeyNotFoundException($"No product exists for SKU '{sku}'.");
}

static decimal CalculateSubtotal(IEnumerable<Product> products)
{
    return products.Sum(product => product.Price);
}

static decimal ApplyTax(decimal amount, decimal taxRate) => amount * (1 + taxRate);

static string FormatMoney(decimal amount)
{
    return amount.ToString("C", CultureInfo.GetCultureInfo("en-US"));
}

static string DescribeCoupon(string? coupon)
{
    return string.IsNullOrWhiteSpace(coupon)
        ? "none"
        : coupon.ToUpperInvariant();
}

namespace Storefront.SyntaxTour
{
    public interface IDescribable
    {
        string Describe();
    }

    public sealed record Product(string Sku, string Name, decimal Price, int Stock) : IDescribable
    {
        public string Describe() => $"{Name} ({Sku}) costs {Price:C} and has {Stock} in stock.";
    }

    public sealed class InventoryLedger : IDisposable
    {
        private readonly string _source;
        private readonly List<string> _events = new();
        private bool _disposed;

        public InventoryLedger(string source)
        {
            _source = source;
            Console.WriteLine($"Ledger '{_source}' opened.");
        }

        public void RecordSale(Product product, decimal amount)
        {
            ThrowIfDisposed();
            _events.Add($"{product.Sku}:{amount:F2}");
            Console.WriteLine($"Recorded sale #{_events.Count} for {product.Sku}.");
        }

        public void Dispose()
        {
            if (_disposed)
            {
                return;
            }

            _disposed = true;
            Console.WriteLine($"Ledger '{_source}' closed with {_events.Count} event(s).");
        }

        private void ThrowIfDisposed()
        {
            if (_disposed)
            {
                throw new ObjectDisposedException(nameof(InventoryLedger));
            }
        }
    }
}
