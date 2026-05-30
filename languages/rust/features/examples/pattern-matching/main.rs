enum Command {
    Move { x: i32, y: i32 },
    Write(String),
    ChangeColor(u8, u8, u8),
    Quit,
}

fn parse_command(input: &str) -> Command {
    let parts: Vec<&str> = input.split_whitespace().collect();
    match parts.as_slice() {
        ["move", x, y] => Command::Move {
            x: x.parse().unwrap_or(0),
            y: y.parse().unwrap_or(0),
        },
        ["write", rest @ ..] => Command::Write(rest.join(" ")),
        ["color", r, g, b] => Command::ChangeColor(
            r.parse().unwrap_or(0),
            g.parse().unwrap_or(0),
            b.parse().unwrap_or(0),
        ),
        ["quit"] => Command::Quit,
        _ => Command::Write(String::from("unknown command")),
    }
}

fn handle(command: Command) -> String {
    match command {
        Command::Move { x: 0, y: 0 } => String::from("stay at origin"),
        Command::Move { x, y } if x.abs() + y.abs() > 10 => {
            format!("move far to ({x}, {y})")
        }
        Command::Move { x, y } => format!("move to ({x}, {y})"),
        Command::Write(text) if text.is_empty() => String::from("write nothing"),
        Command::Write(text) => format!("write: {text}"),
        Command::ChangeColor(255, 0, 0) => String::from("switch to red"),
        Command::ChangeColor(r, g, b) => format!("switch to rgb({r}, {g}, {b})"),
        Command::Quit => String::from("quit"),
    }
}

fn main() {
    for raw in [
        "move 0 0",
        "move 8 7",
        "write hello rust",
        "color 255 0 0",
        "color 10 20 30",
        "quit",
    ] {
        let command = parse_command(raw);
        println!("{raw:?} => {}", handle(command));
    }
}
