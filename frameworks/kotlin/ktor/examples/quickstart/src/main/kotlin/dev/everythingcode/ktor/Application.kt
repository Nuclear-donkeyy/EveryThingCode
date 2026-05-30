package dev.everythingcode.ktor

import io.ktor.http.HttpStatusCode
import io.ktor.serialization.kotlinx.json.json
import io.ktor.server.application.Application
import io.ktor.server.application.call
import io.ktor.server.engine.embeddedServer
import io.ktor.server.netty.Netty
import io.ktor.server.plugins.contentnegotiation.ContentNegotiation
import io.ktor.server.request.receive
import io.ktor.server.response.respond
import io.ktor.server.routing.get
import io.ktor.server.routing.patch
import io.ktor.server.routing.post
import io.ktor.server.routing.route
import io.ktor.server.routing.routing
import kotlinx.serialization.json.Json

fun main() {
    val port = System.getenv("PORT")?.toIntOrNull() ?: 8080
    embeddedServer(Netty, port = port, host = "0.0.0.0") {
        taskModule()
    }.start(wait = true)
}

fun Application.taskModule(store: TaskStore = TaskStore()) {
    install(ContentNegotiation) {
        json(Json {
            ignoreUnknownKeys = true
        })
    }

    routing {
        route("/api") {
            get("/health") {
                call.respond(HealthResponse(status = "ok"))
            }

            route("/tasks") {
                get {
                    call.respond(store.list())
                }

                post {
                    val request = call.receive<CreateTaskRequest>()
                    val title = request.title.trim()
                    if (title.isEmpty()) {
                        call.respond(HttpStatusCode.BadRequest, ErrorResponse("title must not be blank"))
                        return@post
                    }

                    val task = store.create(title)
                    call.respond(HttpStatusCode.Created, task)
                }

                patch("/{id}/done") {
                    val id = call.parameters["id"]?.toIntOrNull()
                    if (id == null) {
                        call.respond(HttpStatusCode.BadRequest, ErrorResponse("id must be an integer"))
                        return@patch
                    }

                    val updated = store.markDone(id)
                    if (updated == null) {
                        call.respond(HttpStatusCode.NotFound, ErrorResponse("task not found"))
                    } else {
                        call.respond(updated)
                    }
                }
            }
        }
    }
}
