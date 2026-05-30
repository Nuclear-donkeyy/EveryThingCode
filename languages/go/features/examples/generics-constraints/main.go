package main

import "fmt"

type Number interface {
	~int | ~int64 | ~float64
}

type Score int

type Order struct {
	ID     string
	Region string
	Amount int
}

func Sum[T Number](values []T) T {
	var total T
	for _, value := range values {
		total += value
	}
	return total
}

func GroupBy[T any, K comparable](values []T, key func(T) K) map[K][]T {
	groups := make(map[K][]T)
	for _, value := range values {
		groupKey := key(value)
		groups[groupKey] = append(groups[groupKey], value)
	}
	return groups
}

func main() {
	scores := []Score{8, 13, 21}
	fmt.Println("score total:", Sum(scores))

	orders := []Order{
		{ID: "o-1", Region: "east", Amount: 120},
		{ID: "o-2", Region: "west", Amount: 75},
		{ID: "o-3", Region: "east", Amount: 90},
	}

	byRegion := GroupBy(orders, func(order Order) string {
		return order.Region
	})

	for region, group := range byRegion {
		fmt.Printf("%s: %d orders\n", region, len(group))
	}
}
