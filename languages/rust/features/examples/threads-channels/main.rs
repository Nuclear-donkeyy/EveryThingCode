use std::sync::mpsc;
use std::thread;
use std::time::Duration;

#[derive(Debug)]
struct Reading {
    sensor: &'static str,
    value: i32,
}

fn spawn_sensor(sensor: &'static str, values: Vec<i32>, tx: mpsc::Sender<Reading>) {
    thread::spawn(move || {
        for value in values {
            thread::sleep(Duration::from_millis(10));
            tx.send(Reading { sensor, value }).expect("receiver should be alive");
        }
    });
}

fn main() {
    let (tx, rx) = mpsc::channel();

    spawn_sensor("temperature", vec![21, 22, 24], tx.clone());
    spawn_sensor("humidity", vec![45, 48], tx.clone());
    drop(tx);

    let mut count = 0;
    let mut total = 0;

    for reading in rx {
        println!("{} => {}", reading.sensor, reading.value);
        count += 1;
        total += reading.value;
    }

    println!("received {count} readings");
    println!("average {}", total as f32 / count as f32);
}
