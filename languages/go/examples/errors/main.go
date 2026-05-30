package main

import (
    "errors"
    "fmt"
)

func loadName(ok bool) (string, error) {
    if !ok {
        return "", errors.New("config missing")
    }
    return "learner", nil
}

func main() {
    name, err := loadName(false)
    if err != nil {
        fmt.Println("recover:", err)
        return
    }
    fmt.Println(name)
}
