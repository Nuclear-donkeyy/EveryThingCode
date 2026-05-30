trait Scored {
    fn name(&self) -> &str;
    fn score(&self) -> u32;

    fn summary(&self) -> String {
        format!("{} scored {}", self.name(), self.score())
    }
}

struct Task {
    name: String,
    impact: u32,
    effort: u32,
}

impl Scored for Task {
    fn name(&self) -> &str {
        &self.name
    }

    fn score(&self) -> u32 {
        self.impact * 2 + (10 - self.effort)
    }
}

fn best_item<T: Scored>(items: &[T]) -> Option<&T> {
    items.iter().max_by_key(|item| item.score())
}

fn main() {
    let tasks = vec![
        Task {
            name: String::from("write tests"),
            impact: 7,
            effort: 3,
        },
        Task {
            name: String::from("trim allocations"),
            impact: 5,
            effort: 4,
        },
        Task {
            name: String::from("document API"),
            impact: 4,
            effort: 2,
        },
    ];

    let visible: Vec<String> = tasks
        .iter()
        .filter(|task| task.score() >= 12)
        .map(|task| task.summary())
        .collect();

    for line in visible {
        println!("{line}");
    }

    if let Some(best) = best_item(&tasks) {
        println!("best: {}", best.summary());
    }
}
