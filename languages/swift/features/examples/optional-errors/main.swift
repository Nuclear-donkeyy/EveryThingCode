enum ConfigError: Error, CustomStringConvertible {
    case missingKey(String)
    case invalidNumber(key: String, value: String)
    case outOfRange(key: String, value: Int, range: ClosedRange<Int>)

    var description: String {
        switch self {
        case .missingKey(let key):
            return "Missing required setting '\(key)'"
        case .invalidNumber(let key, let value):
            return "Setting '\(key)' must be a number, got '\(value)'"
        case .outOfRange(let key, let value, let range):
            return "Setting '\(key)' must be in \(range), got \(value)"
        }
    }
}

func loadPort(from settings: [String: String]) throws -> Int {
    let key = "port"

    guard let rawPort = settings[key] else {
        throw ConfigError.missingKey(key)
    }

    guard let port = Int(rawPort) else {
        throw ConfigError.invalidNumber(key: key, value: rawPort)
    }

    let validRange = 1...65535
    guard validRange.contains(port) else {
        throw ConfigError.outOfRange(key: key, value: port, range: validRange)
    }

    return port
}

let samples = [
    "good": ["port": "8080"],
    "missing": [:],
    "text": ["port": "eighty"],
    "tooLarge": ["port": "70000"]
]

for name in ["good", "missing", "text", "tooLarge"] {
    do {
        let port = try loadPort(from: samples[name] ?? [:])
        print("\(name): starting server on port \(port)")
    } catch let error as ConfigError {
        print("\(name): \(error.description)")
    } catch {
        print("\(name): unexpected error \(error)")
    }
}
