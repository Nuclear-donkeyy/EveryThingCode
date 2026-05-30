data class RawUser(
    val id: Int,
    val nickname: String?,
    val email: String?,
)

fun displayName(user: RawUser): String =
    user.nickname
        ?.trim()
        ?.takeIf { it.isNotEmpty() }
        ?: "匿名用户#${user.id}"

fun emailDomain(user: RawUser): String? =
    user.email
        ?.substringAfter("@", missingDelimiterValue = "")
        ?.takeIf { it.isNotBlank() }
        ?.lowercase()

val users = listOf(
    RawUser(1, "  Lin  ", "lin@example.com"),
    RawUser(2, null, "no-domain"),
    RawUser(3, "   ", null),
)

for (user in users) {
    val domainText = emailDomain(user)?.let { "邮箱域名: $it" } ?: "邮箱域名: 未提供"
    println("${displayName(user)} | $domainText")
}
