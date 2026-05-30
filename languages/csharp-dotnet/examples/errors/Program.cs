static string LoadName(bool ok)
{
    if (!ok) throw new InvalidOperationException("config missing");
    return "learner";
}

try
{
    Console.WriteLine(LoadName(false));
}
catch (InvalidOperationException ex)
{
    Console.WriteLine($"recover: {ex.Message}");
}
