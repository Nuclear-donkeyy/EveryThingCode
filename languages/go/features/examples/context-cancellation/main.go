package main

import (
	"context"
	"errors"
	"fmt"
	"time"
)

func runReport(ctx context.Context, steps int) error {
	for step := 1; step <= steps; step++ {
		select {
		case <-time.After(70 * time.Millisecond):
			fmt.Println("finished step", step)
		case <-ctx.Done():
			return fmt.Errorf("report stopped at step %d: %w", step, ctx.Err())
		}
	}
	return nil
}

func main() {
	ctx, cancel := context.WithTimeout(context.Background(), 180*time.Millisecond)
	defer cancel()

	if err := runReport(ctx, 5); err != nil {
		fmt.Println("handled:", err)
		fmt.Println("deadline exceeded:", errors.Is(err, context.DeadlineExceeded))
		return
	}

	fmt.Println("report completed")
}
