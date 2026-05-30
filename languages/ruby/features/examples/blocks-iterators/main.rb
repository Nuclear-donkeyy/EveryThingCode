Order = Struct.new(:id, :customer, :total, :status, keyword_init: true)

orders = [
  Order.new(id: "R-1001", customer: "Ada", total: 120, status: :paid),
  Order.new(id: "R-1002", customer: "Lin", total: 80, status: :pending),
  Order.new(id: "R-1003", customer: "Matz", total: 220, status: :paid)
]

puts "Warm up:"
3.times { |index| puts "  pass #{index + 1}" }

paid_summaries = orders
  .select { |order| order.status == :paid }
  .map do |order|
    discount = order.total >= 200 ? 0.9 : 1.0
    [order.customer, order.total * discount]
  end

revenue = paid_summaries.reduce(0) { |sum, (_, amount)| sum + amount }

puts "\nPaid orders:"
paid_summaries.each do |customer, amount|
  puts "  #{customer}: $#{amount.round(2)}"
end

puts "\nRevenue after discount: $#{revenue.round(2)}"
