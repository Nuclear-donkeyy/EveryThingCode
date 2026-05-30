use actix_web::{get, web, App, HttpResponse, HttpServer, Responder};
use serde::{Deserialize, Serialize};
use std::{
    collections::BTreeMap,
    sync::{
        atomic::{AtomicU64, Ordering},
        RwLock,
    },
};

struct AppState {
    notes: RwLock<BTreeMap<u64, Note>>,
    next_id: AtomicU64,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
struct Note {
    id: u64,
    title: String,
    body: String,
}

#[derive(Debug, Deserialize)]
struct CreateNote {
    title: String,
    body: String,
}

#[derive(Debug, Serialize)]
struct Health {
    status: &'static str,
    framework: &'static str,
}

fn new_state() -> web::Data<AppState> {
    web::Data::new(AppState {
        notes: RwLock::new(BTreeMap::new()),
        next_id: AtomicU64::new(1),
    })
}

fn configure_routes(config: &mut web::ServiceConfig) {
    config.service(health).service(
        web::scope("/api")
            .service(
                web::resource("/notes")
                    .route(web::get().to(list_notes))
                    .route(web::post().to(create_note)),
            )
            .service(web::resource("/notes/{id}").route(web::get().to(get_note))),
    );
}

#[get("/health")]
async fn health() -> impl Responder {
    web::Json(Health {
        status: "ok",
        framework: "actix-web",
    })
}

async fn list_notes(state: web::Data<AppState>) -> impl Responder {
    let notes = state.notes.read().expect("notes lock poisoned");
    let response: Vec<Note> = notes.values().cloned().collect();
    web::Json(response)
}

async fn get_note(path: web::Path<u64>, state: web::Data<AppState>) -> impl Responder {
    let id = path.into_inner();
    let notes = state.notes.read().expect("notes lock poisoned");

    match notes.get(&id) {
        Some(note) => HttpResponse::Ok().json(note),
        None => HttpResponse::NotFound().body("note not found"),
    }
}

async fn create_note(
    state: web::Data<AppState>,
    payload: web::Json<CreateNote>,
) -> impl Responder {
    let id = state.next_id.fetch_add(1, Ordering::Relaxed);
    let note = Note {
        id,
        title: payload.title.clone(),
        body: payload.body.clone(),
    };

    let mut notes = state.notes.write().expect("notes lock poisoned");
    notes.insert(id, note.clone());

    HttpResponse::Created().json(note)
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    let state = new_state();
    let address = "127.0.0.1:8080";

    println!("Actix Web quickstart listening on http://{address}");
    HttpServer::new(move || {
        App::new()
            .app_data(state.clone())
            .configure(configure_routes)
    })
    .bind(address)?
    .run()
    .await
}

#[cfg(test)]
mod tests {
    use super::*;
    use actix_web::{http::StatusCode, test};
    use serde_json::json;

    #[actix_web::test]
    async fn health_returns_ok() {
        let app = test::init_service(
            App::new()
                .app_data(new_state())
                .configure(configure_routes),
        )
        .await;

        let request = test::TestRequest::get().uri("/health").to_request();
        let response = test::call_service(&app, request).await;

        assert_eq!(response.status(), StatusCode::OK);
    }

    #[actix_web::test]
    async fn create_note_returns_created_json() {
        let app = test::init_service(
            App::new()
                .app_data(new_state())
                .configure(configure_routes),
        )
        .await;

        let request = test::TestRequest::post()
            .uri("/api/notes")
            .set_json(json!({
                "title": "Learn Actix Web",
                "body": "App, Scope, Handler, Data"
            }))
            .to_request();

        let note: Note = test::call_and_read_body_json(&app, request).await;

        assert_eq!(note.id, 1);
        assert_eq!(note.title, "Learn Actix Web");
    }
}
