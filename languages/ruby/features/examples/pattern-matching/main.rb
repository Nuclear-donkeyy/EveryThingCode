events = [
  { type: :payment, status: :captured, id: "pay_101", amount: 42 },
  { type: :payment, status: :failed, id: "pay_102", reason: "card_declined" },
  { type: :refund, id: "ref_201", payment_id: "pay_101", amount: 12 },
  { type: :audit, message: "daily close" }
]

def ruby_at_least?(major, minor)
  current_major, current_minor = RUBY_VERSION.split(".").map(&:to_i)
  current_major > major || (current_major == major && current_minor >= minor)
end

if ruby_at_least?(2, 7)
  eval <<~'RUBY'
    def describe(event)
      case event
      in { type: :payment, status: :captured, id:, amount: }
        "captured #{id} for $#{amount}"
      in { type: :payment, status: :failed, id:, reason: }
        "failed #{id}: #{reason}"
      in { type: :refund, id:, payment_id:, amount: }
        "refund #{id} returns $#{amount} from #{payment_id}"
      else
        "unhandled event: #{event.inspect}"
      end
    end
  RUBY
  mode = "pattern matching"
else
  def describe(event)
    case [event[:type], event[:status]]
    when [:payment, :captured]
      "captured #{event[:id]} for $#{event[:amount]}"
    when [:payment, :failed]
      "failed #{event[:id]}: #{event[:reason]}"
    else
      if event[:type] == :refund
        "refund #{event[:id]} returns $#{event[:amount]} from #{event[:payment_id]}"
      else
        "unhandled event: #{event.inspect}"
      end
    end
  end
  mode = "hash fallback for Ruby #{RUBY_VERSION}"
end

puts "Event descriptions (#{mode}):"
events.each do |event|
  puts "  #{describe(event)}"
end
