require "tmpdir"

def read_with_manual_ensure(path)
  file = File.open(path, "r")
  yield file
ensure
  file&.close
  puts "  manual ensure closed file? #{file&.closed?}"
end

def read_with_block_api(path)
  opened_file = nil
  File.open(path, "r") do |file|
    opened_file = file
    yield file
    puts "  inside block closed? #{file.closed?}"
  end
  puts "  block API closed file? #{opened_file.closed?}"
end

path = File.join(Dir.tmpdir, "ruby-feature-cleanup-#{Process.pid}.txt")
File.write(path, "first line\nsecond line\n")

puts "Manual ensure:"
begin
  read_with_manual_ensure(path) do |file|
    puts "  read: #{file.readline.strip}"
    raise "simulated processing error"
  end
rescue RuntimeError => error
  puts "  caller handled: #{error.message}"
end

puts "\nBlock API:"
read_with_block_api(path) do |file|
  puts "  read: #{file.readline.strip}"
end

File.delete(path) if File.exist?(path)
puts "\nTemporary file removed: #{!File.exist?(path)}"
