package main

import (
	"context"
	"encoding/json"
	"errors"
	"log"
	"net/http"
	"os"
	"strconv"
	"strings"
	"sync"
	"time"
)

type Task struct {
	ID    int    `json:"id"`
	Title string `json:"title"`
	Done  bool   `json:"done"`
}

type Store struct {
	mu     sync.Mutex
	nextID int
	tasks  map[int]Task
}

func NewStore() *Store {
	store := &Store{
		nextID: 1,
		tasks:  make(map[int]Task),
	}
	_, _ = store.Create(context.Background(), "learn net/http handlers")
	_, _ = store.Create(context.Background(), "write httptest coverage")
	return store
}

func (s *Store) List(ctx context.Context) ([]Task, error) {
	if err := ctx.Err(); err != nil {
		return nil, err
	}

	s.mu.Lock()
	defer s.mu.Unlock()

	tasks := make([]Task, 0, len(s.tasks))
	for id := 1; id < s.nextID; id++ {
		if task, ok := s.tasks[id]; ok {
			tasks = append(tasks, task)
		}
	}
	return tasks, nil
}

func (s *Store) Create(ctx context.Context, title string) (Task, error) {
	if err := ctx.Err(); err != nil {
		return Task{}, err
	}

	title = strings.TrimSpace(title)
	if title == "" {
		return Task{}, errors.New("title is required")
	}

	s.mu.Lock()
	defer s.mu.Unlock()

	task := Task{ID: s.nextID, Title: title}
	s.tasks[task.ID] = task
	s.nextID++
	return task, nil
}

func (s *Store) MarkDone(ctx context.Context, id int) (Task, bool, error) {
	if err := ctx.Err(); err != nil {
		return Task{}, false, err
	}

	s.mu.Lock()
	defer s.mu.Unlock()

	task, ok := s.tasks[id]
	if !ok {
		return Task{}, false, nil
	}
	task.Done = true
	s.tasks[id] = task
	return task, true, nil
}

type app struct {
	store  *Store
	logger *log.Logger
}

func main() {
	logger := log.New(os.Stdout, "net-http: ", log.LstdFlags)
	server := &http.Server{
		Addr:              ":" + port(),
		Handler:           newServer(NewStore(), logger),
		ReadHeaderTimeout: 5 * time.Second,
		ReadTimeout:       10 * time.Second,
		WriteTimeout:      10 * time.Second,
		IdleTimeout:       60 * time.Second,
	}

	logger.Printf("listening on http://localhost%s", server.Addr)
	if err := server.ListenAndServe(); err != nil && !errors.Is(err, http.ErrServerClosed) {
		logger.Fatal(err)
	}
}

func port() string {
	if value := os.Getenv("PORT"); value != "" {
		return value
	}
	return "8080"
}

func newServer(store *Store, logger *log.Logger) http.Handler {
	api := &app{store: store, logger: logger}

	mux := http.NewServeMux()
	mux.HandleFunc("GET /health", api.health)
	mux.HandleFunc("GET /tasks", api.listTasks)
	mux.HandleFunc("POST /tasks", api.createTask)
	mux.HandleFunc("PATCH /tasks/{id}/done", api.markTaskDone)

	var handler http.Handler = mux
	handler = timeoutMiddleware(2 * time.Second)(handler)
	handler = recoverMiddleware(logger)(handler)
	handler = loggingMiddleware(logger)(handler)
	return handler
}

func (a *app) health(w http.ResponseWriter, r *http.Request) {
	writeJSON(w, http.StatusOK, map[string]string{"status": "ok"})
}

func (a *app) listTasks(w http.ResponseWriter, r *http.Request) {
	tasks, err := a.store.List(r.Context())
	if err != nil {
		http.Error(w, err.Error(), http.StatusGatewayTimeout)
		return
	}
	writeJSON(w, http.StatusOK, tasks)
}

func (a *app) createTask(w http.ResponseWriter, r *http.Request) {
	var input struct {
		Title string `json:"title"`
	}
	if err := json.NewDecoder(r.Body).Decode(&input); err != nil {
		http.Error(w, "invalid JSON body", http.StatusBadRequest)
		return
	}

	task, err := a.store.Create(r.Context(), input.Title)
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}
	writeJSON(w, http.StatusCreated, task)
}

func (a *app) markTaskDone(w http.ResponseWriter, r *http.Request) {
	id, err := strconv.Atoi(r.PathValue("id"))
	if err != nil || id < 1 {
		http.Error(w, "invalid task id", http.StatusBadRequest)
		return
	}

	task, ok, err := a.store.MarkDone(r.Context(), id)
	if err != nil {
		http.Error(w, err.Error(), http.StatusGatewayTimeout)
		return
	}
	if !ok {
		http.Error(w, "task not found", http.StatusNotFound)
		return
	}
	writeJSON(w, http.StatusOK, task)
}

func timeoutMiddleware(timeout time.Duration) func(http.Handler) http.Handler {
	return func(next http.Handler) http.Handler {
		return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			ctx, cancel := context.WithTimeout(r.Context(), timeout)
			defer cancel()
			next.ServeHTTP(w, r.WithContext(ctx))
		})
	}
}

func recoverMiddleware(logger *log.Logger) func(http.Handler) http.Handler {
	return func(next http.Handler) http.Handler {
		return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			defer func() {
				if recovered := recover(); recovered != nil {
					logger.Printf("panic recovered: %v", recovered)
					http.Error(w, "internal server error", http.StatusInternalServerError)
				}
			}()
			next.ServeHTTP(w, r)
		})
	}
}

func loggingMiddleware(logger *log.Logger) func(http.Handler) http.Handler {
	return func(next http.Handler) http.Handler {
		return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			start := time.Now()
			next.ServeHTTP(w, r)
			logger.Printf("%s %s %s", r.Method, r.URL.Path, time.Since(start).Round(time.Millisecond))
		})
	}
}

func writeJSON(w http.ResponseWriter, status int, value any) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	_ = json.NewEncoder(w).Encode(value)
}
