class SearchQuery {
    var keyword: String = "kotlin"
    var pageSize: Int = 10
    var includeArchived: Boolean = false

    override fun toString(): String =
        "SearchQuery(keyword='$keyword', pageSize=$pageSize, includeArchived=$includeArchived)"
}

data class RequestParams(
    val keyword: String?,
    val pageSize: Int?,
    val includeArchived: Boolean?,
)

fun normalizeKeyword(raw: String?): String? =
    raw
        ?.trim()
        ?.takeIf { it.isNotEmpty() }
        ?.let { it.lowercase() }

fun buildQuery(params: RequestParams): SearchQuery =
    SearchQuery()
        .apply {
            keyword = normalizeKeyword(params.keyword) ?: "kotlin"
            pageSize = params.pageSize?.coerceIn(1, 50) ?: 10
            includeArchived = params.includeArchived ?: false
        }
        .also {
            println("调试: 已构建查询 $it")
        }

val requests = listOf(
    RequestParams("  Coroutines  ", 25, null),
    RequestParams("   ", 200, true),
)

for (params in requests) {
    val query = buildQuery(params)
    val summary = query.run {
        "搜索 '$keyword'，每页 $pageSize 条，包含归档=$includeArchived"
    }
    println(summary)
}
