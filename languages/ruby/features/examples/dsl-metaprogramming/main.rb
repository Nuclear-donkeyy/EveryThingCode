class ConfigSchema
  def self.rules
    @rules ||= {}
  end

  def self.required(name)
    rules[name] = ->(value) { value.nil? || value.to_s.strip.empty? ? "is required" : nil }
    define_method(name) { @values[name] }
  end

  def self.number(name)
    rules[name] = ->(value) { value.is_a?(Numeric) ? nil : "must be a number" }
    define_method(name) { @values[name] }
  end

  def self.build(&block)
    Class.new(self).tap { |schema| schema.instance_eval(&block) }
  end

  def initialize(values)
    @values = values
  end

  def errors
    self.class.rules.each_with_object([]) do |(name, validator), messages|
      message = validator.call(@values[name])
      messages << "#{name} #{message}" if message
    end
  end
end

ServerConfig = ConfigSchema.build do
  required :host
  number :port
end

valid = ServerConfig.new(host: "localhost", port: 4567)
invalid = ServerConfig.new(host: "  ", port: "fast")

puts "Valid config:"
puts "  #{valid.host}:#{valid.port}"
puts "  errors: #{valid.errors.inspect}"

puts "\nInvalid config:"
puts "  errors: #{invalid.errors.inspect}"
