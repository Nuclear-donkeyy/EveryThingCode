class TasksController < ActionController::API
  def index
    render json: Task.all
  end

  def show
    task = Task.find(params[:id])
    return render json: { error: "task not found" }, status: :not_found unless task

    render json: task
  end

  def create
    task = Task.create(title: params[:title])
    render json: task, status: :created
  rescue ArgumentError => error
    render json: { error: error.message }, status: :unprocessable_entity
  end
end
