package main

import (
	"errors"
	"fmt"
)

var ErrMissingRecipient = errors.New("missing recipient")

type Message struct {
	To   string
	Body string
}

type Notifier interface {
	Notify(Message) error
}

type AuditLogger interface {
	Log(string)
}

type Service struct {
	notifier Notifier
	logger   AuditLogger
}

func (s Service) Send(message Message) error {
	s.logger.Log("prepare notification")

	if err := s.notifier.Notify(message); err != nil {
		return fmt.Errorf("send notification to %q: %w", message.To, err)
	}

	s.logger.Log("notification sent")
	return nil
}

type EmailNotifier struct{}

func (EmailNotifier) Notify(message Message) error {
	if message.To == "" {
		return ErrMissingRecipient
	}
	fmt.Printf("email to %s: %s\n", message.To, message.Body)
	return nil
}

type StdoutLogger struct{}

func (StdoutLogger) Log(line string) {
	fmt.Println("audit:", line)
}

func main() {
	service := Service{
		notifier: EmailNotifier{},
		logger:   StdoutLogger{},
	}

	if err := service.Send(Message{To: "team@example.com", Body: "deploy finished"}); err != nil {
		fmt.Println("unexpected:", err)
	}

	if err := service.Send(Message{Body: "no recipient"}); err != nil {
		fmt.Println("handled:", err)
		fmt.Println("is missing recipient:", errors.Is(err, ErrMissingRecipient))
	}
}
