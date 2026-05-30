using Microsoft.Extensions.Options;

var builder = WebApplication.CreateBuilder(args);

builder.Services
    .AddOptions<TodoOptions>()
    .Bind(builder.Configuration.GetSection("Todo"))
    .Validate(options => !string.IsNullOrWhiteSpace(options.ApiName), "Todo:ApiName is required.")
    .Validate(options => options.MaxPageSize is >= 1 and <= 200, "Todo:MaxPageSize must be between 1 and 200.")
    .ValidateOnStart();

builder.Services.AddSingleton<InMemoryTodoRepository>();
builder.Services.AddSingleton<TodoService>();

var app = builder.Build();

app.Use(async (context, next) =>
{
    var startedAt = DateTimeOffset.UtcNow;
    await next();
    var elapsed = DateTimeOffset.UtcNow - startedAt;
    app.Logger.LogInformation(
        "{Method} {Path} -> {StatusCode} in {ElapsedMilliseconds}ms",
        context.Request.Method,
        context.Request.Path,
        context.Response.StatusCode,
        elapsed.TotalMilliseconds);
});

app.MapGet("/", (IOptions<TodoOptions> options) =>
{
    var value = options.Value;
    return Results.Ok(new
    {
        name = value.ApiName,
        version = "v1",
        endpoints = new[] { "/todos", "/todos/{id}", "/todos/{id}/complete" }
    });
});

var todos = app.MapGroup("/todos").WithTags("Todos");

todos.MapGet("/", (int? take, TodoService service, IOptions<TodoOptions> options) =>
{
    var limit = Math.Clamp(take ?? 10, 1, options.Value.MaxPageSize);
    return Results.Ok(service.List(limit));
});

todos.MapGet("/{id:int}", (int id, TodoService service) =>
{
    var todo = service.Find(id);
    return todo is null ? Results.NotFound(new { message = $"Todo {id} was not found." }) : Results.Ok(todo);
});

todos.MapPost("/", (CreateTodoRequest request, TodoService service) =>
{
    var created = service.Create(request);
    return Results.Created($"/todos/{created.Id}", created);
});

todos.MapPatch("/{id:int}/complete", (int id, TodoService service) =>
{
    var completed = service.Complete(id);
    return completed is null ? Results.NotFound(new { message = $"Todo {id} was not found." }) : Results.Ok(completed);
});

app.Run();

public sealed record TodoOptions
{
    public string ApiName { get; init; } = "Todo API";

    public int MaxPageSize { get; init; } = 50;
}

public sealed record CreateTodoRequest(string Title);

public sealed record TodoItem(int Id, string Title, bool Completed, DateTimeOffset CreatedAt);

public sealed class TodoService
{
    private readonly InMemoryTodoRepository repository;

    public TodoService(InMemoryTodoRepository repository)
    {
        this.repository = repository;
    }

    public IReadOnlyList<TodoItem> List(int take)
    {
        return repository.List(take);
    }

    public TodoItem? Find(int id)
    {
        return repository.Find(id);
    }

    public TodoItem Create(CreateTodoRequest request)
    {
        var title = request.Title.Trim();
        if (title.Length == 0)
        {
            throw new BadHttpRequestException("Todo title cannot be empty.");
        }

        return repository.Add(title);
    }

    public TodoItem? Complete(int id)
    {
        return repository.Complete(id);
    }
}

public sealed class InMemoryTodoRepository
{
    private readonly object gate = new();
    private readonly List<TodoItem> items = new();
    private int nextId = 1;

    public IReadOnlyList<TodoItem> List(int take)
    {
        lock (gate)
        {
            return items
                .OrderBy(item => item.Id)
                .Take(take)
                .ToArray();
        }
    }

    public TodoItem? Find(int id)
    {
        lock (gate)
        {
            return items.SingleOrDefault(item => item.Id == id);
        }
    }

    public TodoItem Add(string title)
    {
        lock (gate)
        {
            var item = new TodoItem(nextId++, title, Completed: false, DateTimeOffset.UtcNow);
            items.Add(item);
            return item;
        }
    }

    public TodoItem? Complete(int id)
    {
        lock (gate)
        {
            var index = items.FindIndex(item => item.Id == id);
            if (index < 0)
            {
                return null;
            }

            var completed = items[index] with { Completed = true };
            items[index] = completed;
            return completed;
        }
    }
}
