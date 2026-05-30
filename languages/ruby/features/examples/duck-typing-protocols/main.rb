require "tmpdir"

class ReportPrinter
  def initialize(writer)
    @writer = writer
  end

  def print(title, rows)
    @writer.write("== #{title} ==")
    rows.each { |name, value| @writer.write("#{name}: #{value}") }
  end
end

class ConsoleWriter
  def write(line)
    puts line
  end
end

class MemoryWriter
  attr_reader :lines

  def initialize
    @lines = []
  end

  def write(line)
    @lines << line
  end
end

class FileWriter
  def initialize(path)
    @file = File.open(path, "w")
  end

  def write(line)
    @file.puts(line)
  end

  def close
    @file.close
  ensure
    @file = nil
  end
end

rows = [["paid orders", 2], ["pending orders", 1]]

puts "Console writer:"
ReportPrinter.new(ConsoleWriter.new).print("Daily summary", rows)

memory = MemoryWriter.new
ReportPrinter.new(memory).print("Buffered summary", rows)
puts "\nMemory writer captured:"
puts memory.lines.map { |line| "  #{line}" }

path = File.join(Dir.tmpdir, "ruby-feature-report-#{Process.pid}.txt")
file_writer = FileWriter.new(path)
begin
  ReportPrinter.new(file_writer).print("File summary", rows)
ensure
  file_writer.close
end

puts "\nFile writer saved #{path}:"
puts File.read(path).lines.map { |line| "  #{line}" }
File.delete(path) if File.exist?(path)
