fun loadName(ok: Boolean): String {
    require(ok) { "config missing" }
    return "learner"
}

runCatching { loadName(false) }
    .onSuccess(::println)
    .onFailure { println("recover: ${it.message}") }
