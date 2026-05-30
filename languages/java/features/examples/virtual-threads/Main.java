import java.time.Duration;
import java.time.Instant;
import java.util.List;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;

public class Main {
    public static void main(String[] args) throws InterruptedException, ExecutionException {
        Instant started = Instant.now();

        try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
            List<Future<Inventory>> futures = List.of(
                    executor.submit(() -> fetchInventory("store-a", 650)),
                    executor.submit(() -> fetchInventory("store-b", 400)),
                    executor.submit(() -> fetchInventory("store-c", 550))
            );

            for (Future<Inventory> future : futures) {
                System.out.println(future.get());
            }
        }

        long elapsedMillis = Duration.between(started, Instant.now()).toMillis();
        System.out.println("elapsed millis: " + elapsedMillis);
    }

    static Inventory fetchInventory(String store, int latencyMillis) throws InterruptedException {
        Thread.sleep(latencyMillis);
        return new Inventory(store, latencyMillis / 50);
    }
}

record Inventory(String store, int available) {
}
