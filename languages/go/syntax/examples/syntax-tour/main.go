package main

import (
	"errors"
	"fmt"
	"sort"
	"strings"
)

const defaultStatus = "todo"

var errEmptyTitle = errors.New("task title is empty")

type Task struct {
	Title    string
	Priority int
	Status   string
}

func (t Task) String() string {
	return fmt.Sprintf("%s [%s, p%d]", t.Title, t.Status, t.Priority)
}

func parseTask(line string) (Task, error) {
	parts := strings.Split(line, "|")
	if len(parts) != 3 {
		return Task{}, fmt.Errorf("expected title|priority|status, got %q", line)
	}

	title := strings.TrimSpace(parts[0])
	if title == "" {
		return Task{}, errEmptyTitle
	}

	var priority int
	if _, err := fmt.Sscanf(strings.TrimSpace(parts[1]), "%d", &priority); err != nil {
		return Task{}, fmt.Errorf("parse priority for %q: %w", title, err)
	}
	if priority < 1 || priority > 5 {
		return Task{}, fmt.Errorf("priority for %q must be 1..5", title)
	}

	status := strings.TrimSpace(parts[2])
	if status == "" {
		status = defaultStatus
	}

	return Task{Title: title, Priority: priority, Status: status}, nil
}

func summarize(tasks []Task) map[string]int {
	counts := make(map[string]int)
	for _, task := range tasks {
		counts[task.Status]++
	}
	return counts
}

func statusLabel(status string) string {
	switch status {
	case "done":
		return "finished"
	case "doing":
		return "in progress"
	case "todo":
		return "not started"
	default:
		return "custom"
	}
}

func main() {
	defer fmt.Println("tour finished: deferred cleanup runs before main returns")

	const appName = "Go syntax tour"
	var rawTasks = []string{
		"learn package main|2|done",
		"practice slices and maps|1|doing",
		"handle errors explicitly|1|todo",
		"   |3|todo",
	}

	fmt.Println(appName)
	fmt.Println(`input format: "title|priority|status"`)

	tasks := make([]Task, 0, len(rawTasks))
	for index, line := range rawTasks {
		task, err := parseTask(line)
		if err != nil {
			if errors.Is(err, errEmptyTitle) {
				fmt.Printf("skip row %d: missing title\n", index)
				continue
			}
			fmt.Printf("skip row %d: %v\n", index, err)
			continue
		}
		tasks = append(tasks, task)
	}

	fmt.Println("\nvalid tasks:")
	for i := 0; i < len(tasks); i++ {
		var printable fmt.Stringer = tasks[i]
		fmt.Printf("- %s => %s\n", printable, statusLabel(tasks[i].Status))
	}

	counts := summarize(tasks)
	statuses := make([]string, 0, len(counts))
	for status := range counts {
		statuses = append(statuses, status)
	}
	sort.Strings(statuses)

	fmt.Println("\nsummary:")
	for _, status := range statuses {
		fmt.Printf("- %s: %d\n", status, counts[status])
	}
}
