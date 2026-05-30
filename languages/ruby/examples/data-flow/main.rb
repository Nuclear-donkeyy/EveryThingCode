Course = Data.define(:name, :minutes)

courses = [Course.new("blocks", 20), Course.new("fibers", 30)]
puts "total minutes = #{courses.sum(&:minutes)}"
