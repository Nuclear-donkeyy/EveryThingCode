use axum::{
    extract::{Path, State},
    http::StatusCode,
    response::IntoResponse,
    routing::{get, post},
    Json, Router,
};
use serde::{Deserialize, Serialize};
use std::{
    collections::BTreeMap,
    net::SocketAddr,
    sync::{
        atomic::{AtomicU64, Ordering},
        Arc, RwLock,
    },
};

type SharedState = Arc<AppState>;

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

fn new_state() -> SharedState {
    Arc::new(AppState {
        notes: RwLock::new(BTreeMap::new()),
        next_id: AtomicU64::new(1),
    })
}

fn build_app(state: SharedState) -> Router {
    Router::new()
        .route("/health", get(health))
        .route("/notes", get(list_notes).post(create_note))
        .route("/notes/{id}", get(get_note))
        .with_state(state)
}

async fn health() -> Json<Health> {
    Json(Health {
        status: "ok",
        framework: "axum",
    })
}

async fn list_notes(State(state): State<SharedState>) -> Json<Vec<Note>> {
    let notes = state.notes.read().expect("notes lock poisoned");
    Json(notes.values().cloned().collect())
}

async fn get_note(Path(id): Path<u64>, State(state): State<SharedState>) -> impl IntoResponse {
    let notes = state.notes.read().expect("notes lock poisoned");

    match notes.get(&id) {
        Some(note) => (StatusCode::OK, Json(note.clone())).into_response(),
        None => (StatusCode::NOT_FOUND, "note not found").into_response(),
    }
}

async fn create_note(
    State(state): State<SharedState>,
    Json(payload): Json<CreateNote>,
) -> impl IntoResponse {
    let id = state.next_id.fetch_add(1, Ordering::Relaxed);
    let note = Note {
        id,
        title: payload.title,
        body: payload.body,
    };

    let mut notes = state.notes.write().expect("notes lock poisoned");
    notes.insert(id, note.clone());

    (StatusCode::CREATED, Json(note))
}

#[tokio::main]
async fn main() {
    let address: SocketAddr = "127.0.0.1:3000".parse().expect("valid socket address");
    let listener = tokio::net::TcpListener::bind(address)
        .await
        .expect("bind listener");

    println!("Axum quickstart listening on http://{address}");
    axum::serve(listener, build_app(new_state()))
        .await
        .expect("run server");
}

#[cfg(test)]
mod tests {
    use super::*;
    use axum::{
        body::{to_bytes, Body},
        http::{header, Request},
    };
    use serde_json::{json, Value};
    use tower::ServiceExt;

    #[tokio::test]
    async fn health_returns_ok() {
        let response = build_app(new_state())
            .oneshot(Request::builder().uri("/health").body(Body::empty()).unwrap())
            .await
            .unwrap();

        assert_eq!(response.status(), StatusCode::OK);
    }

    #[tokio::test]
    async fn create_and_list_note() {
        let app = build_app(new_state());

        let response = app
            .oneshot(
                Request::builder()
                    .method("POST")
                    .uri("/notes")
                    .header(header::CONTENT_TYPE, "application/json")
                    .body(Body::from(
                        json!({
                            "title": "Learn Axum",
                            "body": "Router, extractor, state"
                        })
                        .to_string(),
                    ))
                    .unwrap(),
            )
            .await
            .unwrap();

        assert_eq!(response.status(), StatusCode::CREATED);

        let body = to_bytes(response.into_body(), usize::MAX).await.unwrap();
        let created: Value = serde_json::from_slice(&body).unwrap();
        assert_eq!(created["id"], 1);
        assert_eq!(created["title"], "Learn Axum");
    }
}

