package main

import (
	"fmt"
	"sync"
	"time"
)

type Job struct {
	ID    int
	Input int
}

type Result struct {
	WorkerID int
	JobID    int
	Value    int
}

func worker(id int, jobs <-chan Job, results chan<- Result, wg *sync.WaitGroup) {
	defer wg.Done()

	for job := range jobs {
		time.Sleep(time.Duration(40+job.ID*10) * time.Millisecond)
		results <- Result{
			WorkerID: id,
			JobID:    job.ID,
			Value:    job.Input * job.Input,
		}
	}
}

func main() {
	jobs := make(chan Job)
	results := make(chan Result)

	var wg sync.WaitGroup
	for id := 1; id <= 2; id++ {
		wg.Add(1)
		go worker(id, jobs, results, &wg)
	}

	go func() {
		for id, input := range []int{2, 3, 4, 5} {
			jobs <- Job{ID: id + 1, Input: input}
		}
		close(jobs)
	}()

	go func() {
		wg.Wait()
		close(results)
	}()

	for result := range results {
		fmt.Printf("worker %d finished job %d: %d\n", result.WorkerID, result.JobID, result.Value)
	}
}
