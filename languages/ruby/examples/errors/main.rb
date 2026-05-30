def load_name(ok)
  raise "config missing" unless ok
  "learner"
end

begin
  puts load_name(false)
rescue StandardError => error
  puts "recover: #{error.message}"
end
