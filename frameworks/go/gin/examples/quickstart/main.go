package main

import (
	"context"
	"errors"
	"net/http"
	"os"
	"strconv"
	"strings"
	"sync"
	"time"

	"github.com/gin-gonic/gin"
)

type Task struct {
	ID    int    `json:"id"`
	Title string `json:"title"`
	Done  bool   `json:"done"`
}

type CreateTaskInput struct {
	Title string `json:"title" binding:"required,min=3"`
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
	_, _ = store.Create(context.Background(), "learn Gin routes")
	_, _ = store.Create(context.Background(), "test binding errors")
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

func main() {
	gin.SetMode(gin.ReleaseMode)
	router := setupRouter(NewStore())

	server := &http.Server{
		Addr:              ":" + port(),
		Handler:           router,
		ReadHeaderTimeout: 5 * time.Second,
		ReadTimeout:       10 * time.Second,
		WriteTimeout:      10 * time.Second,
		IdleTimeout:       60 * time.Second,
	}

	if err := server.ListenAndServe(); err != nil && !errors.Is(err, http.ErrServerClosed) {
		panic(err)
	}
}

func port() string {
	if value := os.Getenv("PORT"); value != "" {
		return value
	}
	return "8080"
}

func setupRouter(store *Store) *gin.Engine {
	router := gin.New()
	router.Use(requestIDMiddleware())
	router.Use(gin.Logger())
	router.Use(gin.Recovery())

	api := router.Group("/api")
	api.GET("/health", health)
	api.GET("/tasks", listTasks(store))
	api.POST("/tasks", createTask(store))
	api.PATCH("/tasks/:id/done", markTaskDone(store))

	return router
}

func requestIDMiddleware() gin.HandlerFunc {
	return func(c *gin.Context) {
		requestID := c.GetHeader("X-Request-ID")
		if requestID == "" {
			requestID = strconv.FormatInt(time.Now().UnixNano(), 36)
		}

		c.Set("request_id", requestID)
		c.Header("X-Request-ID", requestID)
		c.Next()
	}
}

func health(c *gin.Context) {
	c.JSON(http.StatusOK, gin.H{"status": "ok"})
}

func listTasks(store *Store) gin.HandlerFunc {
	return func(c *gin.Context) {
		tasks, err := store.List(c.Request.Context())
		if err != nil {
			c.JSON(http.StatusGatewayTimeout, gin.H{"error": err.Error()})
			return
		}
		c.JSON(http.StatusOK, tasks)
	}
}

func createTask(store *Store) gin.HandlerFunc {
	return func(c *gin.Context) {
		var input CreateTaskInput
		if err := c.ShouldBindJSON(&input); err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
			return
		}

		task, err := store.Create(c.Request.Context(), input.Title)
		if err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
			return
		}
		c.JSON(http.StatusCreated, task)
	}
}

func markTaskDone(store *Store) gin.HandlerFunc {
	return func(c *gin.Context) {
		id, err := strconv.Atoi(c.Param("id"))
		if err != nil || id < 1 {
			c.JSON(http.StatusBadRequest, gin.H{"error": "invalid task id"})
			return
		}

		task, ok, err := store.MarkDone(c.Request.Context(), id)
		if err != nil {
			c.JSON(http.StatusGatewayTimeout, gin.H{"error": err.Error()})
			return
		}
		if !ok {
			c.JSON(http.StatusNotFound, gin.H{"error": "task not found"})
			return
		}
		c.JSON(http.StatusOK, task)
	}
}
