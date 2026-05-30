package main

import (
	"bytes"
	"encoding/json"
	"io"
	"net/http"
	"net/http/httptest"
	"testing"

	"github.com/gin-gonic/gin"
)

func TestTaskLifecycle(t *testing.T) {
	gin.SetMode(gin.TestMode)
	gin.DefaultWriter = io.Discard
	router := setupRouter(NewStore())

	recorder := performRequest(router, http.MethodGet, "/api/health", "")
	if recorder.Code != http.StatusOK {
		t.Fatalf("health status = %d, want %d", recorder.Code, http.StatusOK)
	}

	recorder = performRequest(router, http.MethodPost, "/api/tasks", `{"title":"ship a Gin API"}`)
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

	recorder = performRequest(router, http.MethodPatch, "/api/tasks/1/done", "")
	if recorder.Code != http.StatusOK {
		t.Fatalf("mark done status = %d, want %d: %s", recorder.Code, http.StatusOK, recorder.Body.String())
	}
}

func TestCreateTaskValidation(t *testing.T) {
	gin.SetMode(gin.TestMode)
	gin.DefaultWriter = io.Discard
	router := setupRouter(NewStore())

	recorder := performRequest(router, http.MethodPost, "/api/tasks", `{"title":""}`)
	if recorder.Code != http.StatusBadRequest {
		t.Fatalf("status = %d, want %d", recorder.Code, http.StatusBadRequest)
	}
}

func performRequest(handler http.Handler, method string, path string, body string) *httptest.ResponseRecorder {
	request := httptest.NewRequest(method, path, bytes.NewBufferString(body))
	if body != "" {
		request.Header.Set("Content-Type", "application/json")
	}

	recorder := httptest.NewRecorder()
	handler.ServeHTTP(recorder, request)
	return recorder
}
