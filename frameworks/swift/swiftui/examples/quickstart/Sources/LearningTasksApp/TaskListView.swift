import SwiftUI

struct TaskListView: View {
    @State private var store = TaskStore()
    @State private var draftTitle = ""
    @Environment(\.colorScheme) private var colorScheme

    var body: some View {
        VStack(alignment: .leading, spacing: 16) {
            header
            composer

            List($store.tasks) { $task in
                TaskRow(task: $task)
            }

            footer
        }
        .padding()
    }

    private var header: some View {
        VStack(alignment: .leading, spacing: 4) {
            Text("Learning Tasks")
                .font(.largeTitle.bold())
            Text("\(store.remainingCount) remaining · \(colorScheme == .dark ? "Dark" : "Light") mode")
                .foregroundStyle(.secondary)
        }
    }

    private var composer: some View {
        HStack {
            TextField("Add a learning task", text: $draftTitle)
                .textFieldStyle(.roundedBorder)

            Button("Add") {
                store.add(title: draftTitle)
                draftTitle = ""
            }
            .keyboardShortcut(.return, modifiers: [])
        }
    }

    private var footer: some View {
        HStack {
            Spacer()
            Button("Clear Completed") {
                store.clearCompleted()
            }
            .disabled(!store.tasks.contains { $0.isDone })
        }
    }
}

struct TaskRow: View {
    @Binding var task: LearningTask

    var body: some View {
        Toggle(isOn: $task.isDone) {
            Text(task.title)
                .strikethrough(task.isDone)
                .foregroundStyle(task.isDone ? .secondary : .primary)
        }
        .toggleStyle(.checkbox)
    }
}

#Preview {
    TaskListView()
}
