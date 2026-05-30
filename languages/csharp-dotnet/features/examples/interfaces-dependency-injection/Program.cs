IClock clock = new FixedClock(new DateTimeOffset(2026, 5, 30, 9, 0, 0, TimeSpan.Zero));
INotifier notifier = new ConsoleNotifier();

var scheduler = new LessonScheduler(clock, notifier);
scheduler.Schedule(new LessonRequest("C# patterns", "Ada", TimeSpan.FromHours(3)));
scheduler.Schedule(new LessonRequest("LINQ review", "Lin", TimeSpan.FromMinutes(30)));

public interface IClock
{
    DateTimeOffset Now { get; }
}

public interface INotifier
{
    void Send(string message);
}

public sealed class FixedClock(DateTimeOffset now) : IClock
{
    public DateTimeOffset Now => now;
}

public sealed class ConsoleNotifier : INotifier
{
    public void Send(string message) => Console.WriteLine(message);
}

public sealed class LessonScheduler(IClock clock, INotifier notifier)
{
    public void Schedule(LessonRequest request)
    {
        var startsAt = clock.Now.Add(request.Delay);
        var message = $"{request.Student} scheduled {request.Topic} at {startsAt:HH:mm}";

        notifier.Send(message);
    }
}

public sealed record LessonRequest(string Topic, string Student, TimeSpan Delay);
