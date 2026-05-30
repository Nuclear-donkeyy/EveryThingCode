class Course {
  const Course(this.name, this.minutes);

  final String name;
  final int minutes;
}

void main() {
  const courses = [Course('null safety', 20), Course('streams', 30)];
  final total = courses.map((course) => course.minutes).reduce((a, b) => a + b);
  print('total minutes = $total');
}
