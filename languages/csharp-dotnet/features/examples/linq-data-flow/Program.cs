var enrollments = new[]
{
    new Enrollment("Ada", "C# fundamentals", 90, completed: true),
    new Enrollment("Lin", "C# fundamentals", 90, completed: false),
    new Enrollment("Mia", "LINQ data flow", 45, completed: true),
    new Enrollment("Noor", "LINQ data flow", 45, completed: true),
    new Enrollment("Sam", "Async services", 60, completed: true)
};

var inspectedRows = 0;

var activeCourseSummaries =
    enrollments
        .Where(enrollment =>
        {
            inspectedRows++;
            return enrollment.Completed;
        })
        .GroupBy(enrollment => enrollment.Course)
        .Select(group => new CourseSummary(
            Course: group.Key,
            CompletedStudents: group.Select(enrollment => enrollment.Student).Order().ToArray(),
            TotalMinutes: group.Sum(enrollment => enrollment.Minutes)))
        .OrderByDescending(summary => summary.CompletedStudents.Length)
        .ThenBy(summary => summary.Course);

Console.WriteLine($"before ToList: inspected rows = {inspectedRows}");

var summaries = activeCourseSummaries.ToList();

Console.WriteLine($"after ToList: inspected rows = {inspectedRows}");

foreach (var summary in summaries)
{
    Console.WriteLine($"{summary.Course}: {summary.CompletedStudents.Length} completed, {summary.TotalMinutes} minutes");
}

public sealed record Enrollment(string Student, string Course, int Minutes, bool Completed);

public sealed record CourseSummary(string Course, IReadOnlyList<string> CompletedStudents, int TotalMinutes);
