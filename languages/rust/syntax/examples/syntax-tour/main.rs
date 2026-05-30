use std::collections::HashMap;

const PASSING_SCORE: u32 = 60;

mod formatter {
    pub fn title(text: &str) -> String {
        format!("== {text} ==")
    }
}

#[derive(Debug)]
struct Student {
    name: String,
    course: String,
    score: u32,
    status: Enrollment,
}

#[derive(Debug)]
enum Enrollment {
    Active,
    Completed { certificate: bool },
    Dropped(String),
}

impl Student {
    fn new(name: &str, course: &str, score: u32, status: Enrollment) -> Self {
        Self {
            name: name.to_string(),
            course: course.to_string(),
            score,
            status,
        }
    }

    fn passed(&self) -> bool {
        self.score >= PASSING_SCORE
    }

    fn improve(&mut self, points: u32) {
        self.score = (self.score + points).min(100);
    }
}

fn status_label(status: &Enrollment) -> String {
    match status {
        Enrollment::Active => "active".to_string(),
        Enrollment::Completed { certificate } => {
            let label = if *certificate {
                "completed with certificate"
            } else {
                "completed"
            };
            label.to_string()
        }
        Enrollment::Dropped(reason) => format!("dropped: {reason}"),
    }
}

fn find_student<'a>(students: &'a [Student], name: &str) -> Option<&'a Student> {
    students.iter().find(|student| student.name == name)
}

fn parse_score(text: &str) -> Result<u32, String> {
    let score = text
        .trim()
        .parse::<u32>()
        .map_err(|err| format!("not a whole number: {err}"))?;

    if score <= 100 {
        Ok(score)
    } else {
        Err(format!("score {score} is above 100"))
    }
}

fn main() {
    let language: &str = "Rust";
    let mut students = vec![
        Student::new("Ada", language, 91, Enrollment::Completed { certificate: true }),
        Student::new("Lin", language, 56, Enrollment::Active),
        Student::new(
            "Mira",
            "Systems",
            72,
            Enrollment::Dropped("schedule conflict".to_string()),
        ),
    ];

    students[1].improve(8);

    let summary = {
        let count = students.len();
        format!("{count} students tracked")
    };

    println!("{}", formatter::title("syntax tour"));
    println!("{summary}");

    let mut course_counts: HashMap<String, u32> = HashMap::new();
    for student in students.iter() {
        *course_counts.entry(student.course.clone()).or_insert(0) += 1;
    }

    println!("course counts: {course_counts:?}");

    for student in students.iter() {
        let outcome = if student.passed() { "pass" } else { "retry" };
        println!(
            "{} -> {} ({}, score {})",
            student.name,
            outcome,
            status_label(&student.status),
            student.score
        );
    }

    match find_student(&students, "Ada") {
        Some(student) => println!("found {} in {}", student.name, student.course),
        None => println!("student not found"),
    }

    for raw in ["88", "oops", "120"] {
        match parse_score(raw) {
            Ok(score) => println!("parsed {raw:?} as {score}"),
            Err(error) => println!("could not parse {raw:?}: {error}"),
        }
    }
}
