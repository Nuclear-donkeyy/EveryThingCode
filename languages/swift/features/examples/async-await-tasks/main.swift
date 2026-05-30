func fetchScore(for name: String, delayNanoseconds: UInt64) async -> Int {
    try? await Task.sleep(nanoseconds: delayNanoseconds)
    print("finished:", name)
    return name.count * 10
}

print("starting requests")

async let profileScore = fetchScore(for: "profile", delayNanoseconds: 120_000_000)
async let historyScore = fetchScore(for: "history", delayNanoseconds: 60_000_000)

let total = await profileScore + historyScore
print("combined score:", total)

let task = Task {
    await fetchScore(for: "background-check", delayNanoseconds: 40_000_000)
}

let backgroundScore = await task.value
print("task score:", backgroundScore)
