package dev.everythingcode.compose

import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertFailsWith

class CounterStateTest {
    @Test
    fun `increments and resets count`() {
        val counter = CounterState()

        assertEquals(1, counter.increment())
        assertEquals(6, counter.increment(step = 5))
        assertEquals(0, counter.reset())
    }

    @Test
    fun `rejects non positive steps`() {
        val counter = CounterState()

        assertFailsWith<IllegalArgumentException> {
            counter.increment(step = 0)
        }
    }
}
