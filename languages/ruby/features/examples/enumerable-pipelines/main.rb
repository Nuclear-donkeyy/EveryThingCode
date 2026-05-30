events = [
  { user: "Ada", kind: :started, seconds: 0 },
  { user: "Ada", kind: :finished, seconds: 42 },
  { user: "Lin", kind: :finished, seconds: 18 },
  { user: "Matz", kind: :started, seconds: 0 },
  { user: "Ada", kind: :finished, seconds: 35 },
  { user: "Matz", kind: :finished, seconds: 51 }
]

completed = events
  .select { |event| event[:kind] == :finished }
  .map { |event| { user: event[:user], seconds: event[:seconds] } }

seconds_by_user = completed
  .group_by { |event| event[:user] }
  .transform_values { |items| items.sum { |event| event[:seconds] } }

ranked = seconds_by_user.sort_by { |_user, seconds| -seconds }

puts "Completed work by user:"
ranked.each do |user, seconds|
  puts "  #{user}: #{seconds}s"
end

puts "\nOriginal events still available: #{events.size}"
