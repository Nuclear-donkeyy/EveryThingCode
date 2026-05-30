// swift-tools-version: 6.3

import PackageDescription

let package = Package(
    name: "LearningTasksApp",
    platforms: [
        .macOS(.v14)
    ],
    products: [
        .executable(name: "LearningTasksApp", targets: ["LearningTasksApp"])
    ],
    targets: [
        .executableTarget(
            name: "LearningTasksApp"
        )
    ]
)
