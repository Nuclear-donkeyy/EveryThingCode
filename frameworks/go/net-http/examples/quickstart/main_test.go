package main

import (
	"bytes"
	"encoding/json"
	"io"
	"log"
	"net/http"
	"net/http/httptest"
	"testing"
)

func TestTaskLifecycle(t *testing.T) {
	handler := newServer(NewStore(), log.New(io.Discard, "", 0))

	recorder := httptest.NewRecorder()
	handler.ServeHTTP(recorder, httptest.NewRequest(http.MethodGet, "/health", nil))
	if recorder.Code != http.StatusOK {
		t.Fatalf("health status = %d, want %d", recorder.Code, http.StatusOK)
	}

	body := bytes.NewBufferString(`{"title":"ship a standard library API"}`)
	recorder = httptest.NewRecorder()
	handler.ServeHTTP(recorder, httptest.NewRequest(http.MethodPost, "/tasks", body))
	if recorder.Code != http.StatusCreated {
		t.Fatalf("create status = %d, want %d: %s", recorder.Code, http.StatusCreated, recorder.Body.String())
	}

	var created Task
	if err := json.NewDecoder(recorder.Body).Decode(&created); err != nil {
		t.Fatalf("decode created task: %v", err)
	}
	if created.ID == 0 || created.Done {
		t.Fatalf("created task = %+v, want non-zero id and done=false", created)
	}

	recorder = httptest.NewRecorder()
	handler.ServeHTTP(recorder, httptest.NewRequest(http.MethodPatch, "/tasks/1/done", nil))
	if recorder.Code != http.StatusOK {
		t.Fatalf("mark done status = %d, want %d: %s", recorder.Code, http.StatusOK, recorder.Body.String())
	}

	var done Task
	if err := json.NewDecoder(recorder.Body).Decode(&done); err != nil {
		t.Fatalf("decode done task: %v", err)
	}
	if !done.Done {
		t.Fatalf("done task = %+v, want done=true", done)
	}
}

func TestCreateTaskRequiresTitle(t *testing.T) {
	handler := newServer(NewStore(), log.New(io.Discard, "", 0))

	recorder := httptest.NewRecorder()
	handler.ServeHTTP(recorder, httptest.NewRequest(http.MethodPost, "/tasks", bytes.NewBufferString(`{"title":""}`)))
	if recorder.Code != http.StatusBadRequest {
		t.Fatalf("status = %d, want %d", recorder.Code, http.StatusBadRequest)
	}
}
