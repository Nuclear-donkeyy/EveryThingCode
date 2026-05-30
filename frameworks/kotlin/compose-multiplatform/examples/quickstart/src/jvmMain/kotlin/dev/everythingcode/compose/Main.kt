package dev.everythingcode.compose

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.material.Button
import androidx.compose.material.MaterialTheme
import androidx.compose.material.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.compose.ui.window.Window
import androidx.compose.ui.window.application

fun main() = application {
    Window(
        onCloseRequest = ::exitApplication,
        title = "Compose Quickstart",
    ) {
        App()
    }
}

@Composable
fun App(counter: CounterState = CounterState()) {
    var count by remember { mutableStateOf(counter.count) }

    MaterialTheme {
        CounterPanel(
            count = count,
            onIncrement = { count = counter.increment() },
            onReset = { count = counter.reset() },
        )
    }
}

@Composable
fun CounterPanel(
    count: Int,
    onIncrement: () -> Unit,
    onReset: () -> Unit,
) {
    Column(
        modifier = Modifier.fillMaxSize().padding(32.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center,
    ) {
        Text("Compose Multiplatform counter")
        Spacer(Modifier.height(12.dp))
        Text("Count: $count")
        Spacer(Modifier.height(16.dp))
        Row(horizontalArrangement = Arrangement.spacedBy(12.dp)) {
            Button(onClick = onIncrement) {
                Text("Add")
            }
            Button(onClick = onReset) {
                Text("Reset")
            }
        }
    }
}
