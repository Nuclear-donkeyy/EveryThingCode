struct Inventory {
    items: Vec<String>,
}

fn consume_report(report: String) {
    println!("archived report: {report}");
}

fn list_items(inventory: &Inventory) {
    for item in &inventory.items {
        println!("item: {item}");
    }
}

fn add_item(inventory: &mut Inventory, item: &str) {
    inventory.items.push(item.to_string());
}

fn first_word(text: &str) -> &str {
    text.split_whitespace().next().unwrap_or("")
}

fn main() {
    let report = String::from("field report");
    consume_report(report);

    let mut inventory = Inventory {
        items: vec![String::from("sensor"), String::from("battery")],
    };

    list_items(&inventory);
    add_item(&mut inventory, "radio");

    let note = String::from("battery checked");
    let word = first_word(&note);

    println!("first word: {word}");
    println!("inventory size: {}", inventory.items.len());
}
