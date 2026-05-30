enum Readiness {
    Ready { load: u32 },
    Waiting(&'static str),
    Blocked { code: u16, reason: &'static str },
}

fn parse_load(raw: &str) -> Result<u32, String> {
    raw.parse::<u32>()
        .map_err(|_| format!("'{raw}' is not a number"))
}

fn classify(raw: &str) -> Option<Readiness> {
    if raw.trim().is_empty() {
        return None;
    }

    match parse_load(raw) {
        Ok(0) => Some(Readiness::Waiting("no work assigned")),
        Ok(load) if load <= 80 => Some(Readiness::Ready { load }),
        Ok(_) => Some(Readiness::Blocked {
            code: 429,
            reason: "too much load",
        }),
        Err(_) => Some(Readiness::Blocked {
            code: 400,
            reason: "invalid input",
        }),
    }
}

fn describe(state: Readiness) -> String {
    match state {
        Readiness::Ready { load } => format!("ready with load {load}"),
        Readiness::Waiting(reason) => format!("waiting: {reason}"),
        Readiness::Blocked { code, reason } => format!("blocked {code}: {reason}"),
    }
}

fn main() {
    for raw in ["42", "0", "120", "abc", ""] {
        match classify(raw) {
            Some(state) => println!("{raw:?} => {}", describe(state)),
            None => println!("{raw:?} => no value"),
        }
    }
}
