package main

import "fmt"

type Course struct {
    Name    string
    Minutes int
}

func main() {
    courses := []Course{{"interfaces", 20}, {"goroutines", 30}}
    total := 0
    for _, course := range courses {
        total += course.Minutes
    }
    fmt.Printf("total minutes = %d\n", total)
}
