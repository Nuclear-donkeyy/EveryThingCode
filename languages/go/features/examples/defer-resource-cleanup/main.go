package main

import (
	"fmt"
	"io"
	"os"
	"path/filepath"
)

func buildReport() (err error) {
	file, err := os.CreateTemp("", "go-feature-report-*.txt")
	if err != nil {
		return fmt.Errorf("create temp file: %w", err)
	}

	name := file.Name()
	fmt.Println("created", filepath.Base(name))

	defer func() {
		fmt.Println("remove temp file")
		if removeErr := os.Remove(name); err == nil && removeErr != nil {
			err = fmt.Errorf("remove temp file: %w", removeErr)
		}
	}()

	defer func() {
		fmt.Println("close file")
		if closeErr := file.Close(); err == nil && closeErr != nil {
			err = fmt.Errorf("close temp file: %w", closeErr)
		}
	}()

	if _, err = file.WriteString("status=ok\nitems=3\n"); err != nil {
		return fmt.Errorf("write report: %w", err)
	}
	fmt.Println("report written")

	if _, err = file.Seek(0, 0); err != nil {
		return fmt.Errorf("rewind report: %w", err)
	}

	content, err := io.ReadAll(file)
	if err != nil {
		return fmt.Errorf("read report: %w", err)
	}

	fmt.Printf("content:\n%s", content)
	return nil
}

func main() {
	if err := buildReport(); err != nil {
		fmt.Println("handled:", err)
	}
}
