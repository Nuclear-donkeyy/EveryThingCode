module Auditable
  def record_event(message)
    audit_events << "#{Time.now.strftime("%H:%M:%S")} #{message}"
  end

  def audit_trail
    audit_events.dup
  end

  private

  def audit_events
    @audit_events ||= []
  end
end

class Order
  include Auditable

  def initialize(id)
    @id = id
  end

  def pay(amount)
    record_event("order #{@id} paid $#{amount}")
  end
end

class Deployment
  include Auditable

  def initialize(service)
    @service = service
  end

  def promote(version)
    record_event("#{@service} promoted to #{version}")
  end
end

order = Order.new("R-2001")
order.pay(128)

deployment = Deployment.new("billing-api")
deployment.promote("v2.4.0")

puts "Method lookup:"
puts "  Order ancestors include Auditable? #{Order.ancestors.include?(Auditable)}"
puts "  Deployment ancestors include Auditable? #{Deployment.ancestors.include?(Auditable)}"

puts "\nAudit trails:"
puts "  order: #{order.audit_trail.join(", ")}"
puts "  deployment: #{deployment.audit_trail.join(", ")}"
