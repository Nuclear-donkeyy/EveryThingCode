var exportPath = Path.Combine(Path.GetTempPath(), "csharp-dotnet-feature-report.txt");

using (var writer = new ReportWriter(exportPath))
{
    writer.WriteLine("C# feature report");
    writer.WriteLine("resource boundary: using + IDisposable");
}

Console.WriteLine(File.ReadAllText(exportPath).TrimEnd());
Console.WriteLine($"file exists after dispose: {File.Exists(exportPath)}");

public sealed class ReportWriter : IDisposable
{
    private readonly StreamWriter writer;
    private bool disposed;

    public ReportWriter(string path)
    {
        writer = new StreamWriter(path, append: false);
        Console.WriteLine("opened writer");
    }

    public void WriteLine(string line)
    {
        ObjectDisposedException.ThrowIf(disposed, this);
        writer.WriteLine(line);
    }

    public void Dispose()
    {
        if (disposed)
        {
            return;
        }

        writer.Dispose();
        disposed = true;
        Console.WriteLine("disposed writer");
    }
}
