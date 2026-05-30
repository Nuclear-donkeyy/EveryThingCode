package dev.everythingcode.springboot;

import java.util.Comparator;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicLong;

import org.springframework.stereotype.Repository;

@Repository
public class TaskRepository {
    private final AtomicLong nextId = new AtomicLong();
    private final Map<Long, Task> tasks = new ConcurrentHashMap<>();

    public TaskRepository() {
        create("Read Spring Boot guide", false);
        create("Run quickstart tests", true);
    }

    public List<Task> findAll() {
        return tasks.values().stream()
                .sorted(Comparator.comparingLong(Task::id))
                .toList();
    }

    public Optional<Task> findById(long id) {
        return Optional.ofNullable(tasks.get(id));
    }

    public Task create(String title, boolean done) {
        long id = nextId.incrementAndGet();
        Task task = new Task(id, title, done);
        tasks.put(id, task);
        return task;
    }
}

