fn load_name(ok: bool) -> Result<&'static str, &'static str> {
    if ok { Ok("learner") } else { Err("config missing") }
}

fn main() {
    match load_name(false) {
        Ok(name) => println!("{name}"),
        Err(error) => println!("recover: {error}"),
    }
}
