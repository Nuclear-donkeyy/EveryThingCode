enum ConfigError: Error {
    case missing
}

func loadName(_ ok: Bool) throws -> String {
    if !ok { throw ConfigError.missing }
    return "learner"
}

do {
    print(try loadName(false))
} catch {
    print("recover: \(error)")
}
