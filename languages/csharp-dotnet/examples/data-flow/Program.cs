var courses = new[] {
    new Course("nullable", 20),
    new Course("async", 30),
};

Console.WriteLine($"total minutes = {courses.Sum(course => course.Minutes)}");

public record Course(string Name, int Minutes);
