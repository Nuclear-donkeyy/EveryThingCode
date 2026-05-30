struct Document<'a> {
    title: &'a str,
    body: &'a str,
}

fn longer<'a>(left: &'a str, right: &'a str) -> &'a str {
    if left.len() >= right.len() {
        left
    } else {
        right
    }
}

fn first_sentence(text: &str) -> &str {
    text.split('.').next().unwrap_or(text).trim()
}

fn describe<'a>(document: &'a Document<'a>, fallback: &'a str) -> &'a str {
    let sentence = first_sentence(document.body);
    if sentence.is_empty() {
        fallback
    } else {
        sentence
    }
}

fn main() {
    let title = String::from("Rust field note");
    let body = String::from("Borrowed data can be read without taking ownership. The owner stays in main.");
    let fallback = "empty document";

    let document = Document {
        title: &title,
        body: &body,
    };

    println!("title: {}", document.title);
    println!("summary: {}", describe(&document, fallback));

    let chosen = longer(document.title, fallback);
    println!("longer label: {chosen}");
}
