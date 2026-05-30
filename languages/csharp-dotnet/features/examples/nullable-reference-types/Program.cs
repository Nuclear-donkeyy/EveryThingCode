var rawRows = new[]
{
    new RawStudent("Ada", "ada@example.com"),
    new RawStudent("Lin", null),
    new RawStudent("", "empty-name@example.com")
};

foreach (var row in rawRows)
{
    if (Student.TryCreate(row, out var student, out var error))
    {
        Console.WriteLine($"accepted: {student.DisplayName} <{student.Email}>");
    }
    else
    {
        Console.WriteLine($"rejected: {error}");
    }
}

public sealed record RawStudent(string? Name, string? Email);

public sealed record Student(string DisplayName, string Email)
{
    public static bool TryCreate(RawStudent row, out Student? student, out string? error)
    {
        if (string.IsNullOrWhiteSpace(row.Name))
        {
            student = null;
            error = "name is required";
            return false;
        }

        if (string.IsNullOrWhiteSpace(row.Email))
        {
            student = null;
            error = $"email is required for {row.Name}";
            return false;
        }

        student = new Student(row.Name.Trim(), row.Email.Trim());
        error = null;
        return true;
    }
}
