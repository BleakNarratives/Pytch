package main

import (
    "fmt"
    "math/rand"
)

type Agent struct {
    ID   int
    Task string
    Healthy bool
}

func (a *Agent) SelfHeal() {
    if !a.Healthy {
        fmt.Printf("Agent %d is healing...\n", a.ID)
        a.Healthy = true
    }
}

func main() {
    agents := []Agent{
        {1, "Education", true},
        {2, "Healthcare", false}, // Simulate a fault
    }

    for i := range agents {
        if !agents[i].Healthy {
            agents[i].SelfHeal()
        }
        fmt.Printf("Agent %d (%s): Healthy=%v\n", agents[i].ID, agents[i].Task, agents[i].Healthy)
    }
}
