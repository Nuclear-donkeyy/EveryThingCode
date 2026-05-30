import SwiftUI

@main
struct LearningTasksApp: App {
    var body: some Scene {
        WindowGroup("SwiftUI Tasks") {
            TaskListView()
                .frame(minWidth: 480, minHeight: 360)
        }
    }
}
