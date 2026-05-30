struct Course {
    name: &'static str,
    minutes: u32,
}

fn main() {
    let courses = [Course { name: "ownership", minutes: 25 }, Course { name: "traits", minutes: 35 }];
    let total: u32 = courses.iter().map(|course| course.minutes).sum();
    println!("total minutes = {total}");
}
