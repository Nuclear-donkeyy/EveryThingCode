require "json"
require "sinatra/base"

class TaskRepository
  def initialize
    @tasks = [
      { id: 1, title: "Read Sinatra README", done: false },
      { id: 2, title: "Trace a Rack request", done: false }
    ]
    @next_id = 3
  end

  def all
    @tasks
  end

  def create(title:)
    task = { id: @next_id, title: title, done: false }
    @next_id += 1
    @tasks << task
    task
  end
end

class TaskService
  def initialize(repository)
    @repository = repository
  end

  def create_task(title)
    normalized = title.to_s.strip
    raise ArgumentError, "title is required" if normalized.empty?

    @repository.create(title: normalized)
  end
end

class TaskApi < Sinatra::Base
  repository = TaskRepository.new
  service = TaskService.new(repository)

  configure do
    set :show_exceptions, false
  end

  before do
    content_type :json
  end

  helpers do
    def json(payload)
      JSON.generate(payload)
    end
  end

  get "/health" do
    json(status: "ok")
  end

  get "/tasks" do
    json(repository.all)
  end

  post "/tasks" do
    payload = JSON.parse(request.body.read)
    task = service.create_task(payload["title"])
    status 201
    json(task)
  rescue JSON::ParserError
    status 400
    json(error: "request body must be valid JSON")
  rescue ArgumentError => error
    status 400
    json(error: error.message)
  end
end
