var catalog = new InMemoryCatalog<CoursePlan>();

var fundamentals = new CoursePlan(
    Id: "cs-101",
    Title: "C# fundamentals",
    Minutes: 90,
    Tags: ["oop", "generics"]);

catalog.Add(fundamentals);
catalog.Add(fundamentals with
{
    Id = "cs-201",
    Title = "Records and patterns",
    Minutes = 45,
    Tags = ["records", "patterns"]
});

foreach (var plan in catalog.All())
{
    Console.WriteLine($"{plan.Id}: {Describe(plan)}");
}

static string Describe(CoursePlan plan) => plan switch
{
    { Minutes: >= 60, Tags.Count: >= 2 } => $"{plan.Title} is a deep workshop",
    { Tags: var tags } when tags.Contains("records") => $"{plan.Title} focuses on data modeling",
    _ => $"{plan.Title} is a short lesson"
};

public interface IEntity
{
    string Id { get; }
}

public sealed class InMemoryCatalog<T> where T : IEntity
{
    private readonly Dictionary<string, T> items = new();

    public void Add(T item) => items[item.Id] = item;

    public IEnumerable<T> All() => items.Values.OrderBy(item => item.Id);
}

public sealed record CoursePlan(
    string Id,
    string Title,
    int Minutes,
    IReadOnlyList<string> Tags) : IEntity;
