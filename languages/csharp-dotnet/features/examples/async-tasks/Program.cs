using var timeout = new CancellationTokenSource(TimeSpan.FromSeconds(2));

var cardTasks = new[]
{
    LoadCardAsync("cs-101", timeout.Token),
    LoadCardAsync("linq-201", timeout.Token),
    LoadCardAsync("async-301", timeout.Token)
};

Console.WriteLine("requests started");

var cards = await Task.WhenAll(cardTasks);

foreach (var card in cards.OrderBy(card => card.Id))
{
    var mentor = card.MentorName ?? "mentor pending";
    Console.WriteLine($"{card.Id}: {card.Title} ({mentor})");
}

static async Task<CourseCard> LoadCardAsync(string id, CancellationToken cancellationToken)
{
    await Task.Delay(delay: TimeSpan.FromMilliseconds(120), cancellationToken);

    return id switch
    {
        "cs-101" => new CourseCard(id, "C# fundamentals", "Ada"),
        "linq-201" => new CourseCard(id, "LINQ data flow", "Lin"),
        _ => new CourseCard(id, "Async services", MentorName: null)
    };
}

public sealed record CourseCard(string Id, string Title, string? MentorName);
