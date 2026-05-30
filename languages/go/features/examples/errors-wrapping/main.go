package main

import (
	"errors"
	"fmt"
)

var ErrUserNotFound = errors.New("user not found")

type OperationError struct {
	Operation string
	Key       string
	Err       error
}

func (e *OperationError) Error() string {
	return fmt.Sprintf("%s %q: %v", e.Operation, e.Key, e.Err)
}

func (e *OperationError) Unwrap() error {
	return e.Err
}

func lookupEmail(users map[string]string, userID string) (string, error) {
	email, ok := users[userID]
	if !ok {
		return "", &OperationError{
			Operation: "lookup email",
			Key:       userID,
			Err:       ErrUserNotFound,
		}
	}
	return email, nil
}

func deliverReceipt(users map[string]string, userID string) error {
	email, err := lookupEmail(users, userID)
	if err != nil {
		return fmt.Errorf("deliver receipt for user %s: %w", userID, err)
	}

	fmt.Println("receipt sent to", email)
	return nil
}

func main() {
	users := map[string]string{
		"u-100": "team@example.com",
	}

	if err := deliverReceipt(users, "u-100"); err != nil {
		fmt.Println("unexpected:", err)
	}

	if err := deliverReceipt(users, "u-404"); err != nil {
		fmt.Println("handled:", err)
		fmt.Println("is user not found:", errors.Is(err, ErrUserNotFound))

		var opErr *OperationError
		if errors.As(err, &opErr) {
			fmt.Printf("operation=%s key=%s\n", opErr.Operation, opErr.Key)
		}
	}
}
