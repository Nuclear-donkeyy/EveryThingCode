require "json"
require "tempfile"

DEFAULT_OWNER = "learning-team".freeze

class InvalidTask < StandardError; end

module Taggable
  def tags
    base_tags = [owner, status]
    priority >= 3 ? base_tags + ["high-priority"] : base_tags
  end
end

class Task
  include Taggable

  attr_reader :title, :priority, :owner

  def initialize(title, priority:, done: false, owner: DEFAULT_OWNER)
    raise InvalidTask, "title must not be empty" if title.nil? || title.strip.empty?
    raise InvalidTask, "priority must be positive" if priority < 1

    @title = title
    @priority = priority
    @done = done
    @owner = owner
  end

  def done?
    @done
  end

  def status
    if done?
      "done"
    elsif priority >= 3
      "urgent"
    else
      "open"
    end
  end
end

def parse_priority(raw_value, default: 1)
  Integer(raw_value)
rescue ArgumentError
  puts "Invalid priority #{raw_value.inspect}; using default #{default}."
  default
end

def priority_label(priority)
  case priority
  when 1
    "low"
  when 2..3
    "normal"
  else
    "high"
  end
end

def with_section(title)
  puts
  puts "== #{title} =="
  result = yield
  puts "-- end #{title} --"
  result
end

def build_tasks
  [
    Task.new("Read syntax guide", priority: 1, done: true),
    Task.new("Run the syntax tour", priority: 2),
    Task.new("Explain block and yield", priority: parse_priority("high")),
    Task.new("Refactor repeated imports", priority: 3, owner: "platform")
  ]
end

def summarize(tasks)
  status_counts = { "done" => 0, "urgent" => 0, "open" => 0 }

  tasks.each do |task|
    next if task.title.include?("Draft")

    status_counts[task.status] += 1
  end

  done_count = tasks.select(&:done?).size
  total_priority = tasks.sum(&:priority)
  all_tags = tasks.flat_map(&:tags).map(&:downcase).uniq.sort

  {
    status_counts: status_counts,
    done_count: done_count,
    total_priority: total_priority,
    tags: all_tags
  }
end

def report_rows(tasks)
  tasks.map.with_index(1) do |task, index|
    {
      index: index,
      title: task.title,
      owner: task.owner,
      status: task.status,
      priority: priority_label(task.priority)
    }
  end
end

def write_json_report(tasks)
  file = Tempfile.new(["ruby-syntax-tour", ".json"])
  file.write(JSON.pretty_generate(report_rows(tasks)))
  file.close

  File.read(file.path)
ensure
  file&.unlink
end

def main
  tasks = build_tasks

  with_section("tasks") do
    tasks.each do |task|
      puts "#{task.title}: #{task.status} / #{priority_label(task.priority)}"
    end
  end

  summary = with_section("summary") do
    summarize(tasks)
  end

  puts "Status counts: #{summary.fetch(:status_counts)}"
  puts "Done: #{summary.fetch(:done_count)}"
  puts "Total priority: #{summary.fetch(:total_priority)}"
  puts "Tags: #{summary.fetch(:tags).join(', ')}"

  with_section("json report") do
    puts write_json_report(tasks)
  end
rescue InvalidTask => error
  warn "Cannot build task list: #{error.message}"
end

if __FILE__ == $PROGRAM_NAME
  main
end
