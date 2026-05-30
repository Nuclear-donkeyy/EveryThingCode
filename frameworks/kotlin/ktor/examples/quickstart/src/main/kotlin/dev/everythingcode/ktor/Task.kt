package dev.everythingcode.ktor

import kotlinx.serialization.Serializable

@Serializable
data class Task(
    val id: Int,
    val title: String,
    val done: Boolean = false,
)

@Serializable
data class CreateTaskRequest(
    val title: String,
)

@Serializable
data class ErrorResponse(
    val error: String,
)

@Serializable
data class HealthResponse(
    val status: String,
)
