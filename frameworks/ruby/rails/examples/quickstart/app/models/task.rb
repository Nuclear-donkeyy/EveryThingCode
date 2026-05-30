class Task
  @records = [
    { id: 1, title: "Read Rails guides", done: false },
    { id: 2, title: "Map routes to controllers", done: false }
  ]
  @next_id = 3

  class << self
    def all
      @records
    end

    def find(id)
      @records.find { |task| task[:id] == id.to_i }
    end

    def create(title:)
      normalized = title.to_s.strip
      raise ArgumentError, "title is required" if normalized.empty?

      task = { id: @next_id, title: normalized, done: false }
      @next_id += 1
      @records << task
      task
    end
  end
end
