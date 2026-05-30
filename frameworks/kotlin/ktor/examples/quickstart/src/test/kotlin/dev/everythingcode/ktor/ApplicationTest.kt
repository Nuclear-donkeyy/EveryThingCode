package dev.everythingcode.ktor

import io.ktor.client.call.body
import io.ktor.client.plugins.contentnegotiation.ContentNegotiation
import io.ktor.client.request.get
import io.ktor.client.request.patch
import io.ktor.client.request.post
import io.ktor.client.request.setBody
import io.ktor.http.ContentType
import io.ktor.http.HttpStatusCode
import io.ktor.http.contentType
import io.ktor.serialization.kotlinx.json.json
import io.ktor.server.testing.testApplication
import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertTrue

class ApplicationTest {
    @Test
    fun `creates and completes tasks`() = testApplication {
        application {
            taskModule(TaskStore(emptyList()))
        }

        val client = createClient {
            install(ContentNegotiation) {
                json()
            }
        }

        val created = client.post("/api/tasks") {
            contentType(ContentType.Application.Json)
            setBody(CreateTaskRequest("  write Ktor test  "))
        }

        assertEquals(HttpStatusCode.Created, created.status)
        assertEquals("write Ktor test", created.body<Task>().title)

        val completed = client.patch("/api/tasks/1/done")
        assertEquals(HttpStatusCode.OK, completed.status)
        assertTrue(completed.body<Task>().done)
    }

    @Test
    fun `rejects blank task titles`() = testApplication {
        application {
            taskModule(TaskStore(emptyList()))
        }

        val response = client.post("/api/tasks") {
            contentType(ContentType.Application.Json)
            setBody("""{"title":"   "}""")
        }

        assertEquals(HttpStatusCode.BadRequest, response.status)
    }

    @Test
    fun `returns health response`() = testApplication {
        application {
            taskModule()
        }

        val response = client.get("/api/health")

        assertEquals(HttpStatusCode.OK, response.status)
        assertEquals("""{"status":"ok"}""", response.body<String>())
    }
}
