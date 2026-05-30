struct Course {
    let name: String
    let minutes: Int
}

let courses = [Course(name: "actors", minutes: 20), Course(name: "protocols", minutes: 30)]
print("total minutes = \(courses.map(\.minutes).reduce(0, +))")
