enum SignupError: Error, CustomStringConvertible {
    case emptyEmail
    case invalidEmail(String)
    case weakPassword(minimumLength: Int)

    var description: String {
        switch self {
        case .emptyEmail:
            return "email is required"
        case .invalidEmail(let value):
            return "'\(value)' is not a valid email"
        case .weakPassword(let minimumLength):
            return "password must be at least \(minimumLength) characters"
        }
    }
}

struct Account {
    let email: String
}

func validateSignup(email: String, password: String) -> Result<Account, SignupError> {
    let trimmedEmail = email.filter { !$0.isWhitespace }

    guard !trimmedEmail.isEmpty else {
        return .failure(.emptyEmail)
    }

    guard trimmedEmail.contains("@") else {
        return .failure(.invalidEmail(trimmedEmail))
    }

    guard password.count >= 8 else {
        return .failure(.weakPassword(minimumLength: 8))
    }

    return .success(Account(email: trimmedEmail.lowercased()))
}

let attempts = [
    (email: "  USER@example.com  ", password: "correct horse"),
    (email: "", password: "correct horse"),
    (email: "not-an-email", password: "correct horse"),
    (email: "team@example.com", password: "short")
]

for attempt in attempts {
    switch validateSignup(email: attempt.email, password: attempt.password) {
    case .success(let account):
        print("created account:", account.email)
    case .failure(let error):
        print("signup failed:", error.description)
    }
}
