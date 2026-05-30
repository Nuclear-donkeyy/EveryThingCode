package dev.everythingcode.compose

class CounterState(initialValue: Int = 0) {
    var count: Int = initialValue
        private set

    fun increment(step: Int = 1): Int {
        require(step > 0) { "step must be positive" }
        count += step
        return count
    }

    fun reset(): Int {
        count = 0
        return count
    }
}
