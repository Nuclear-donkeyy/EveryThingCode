#include <QCoreApplication>
#include <QObject>
#include <QString>
#include <QStringList>
#include <QTimer>

#include <iostream>

class TaskBoard final : public QObject {
    Q_OBJECT

public:
    using QObject::QObject;

    void addTask(const QString& title) {
        tasks_.append(title);
        emit taskAdded(tasks_.size(), title);
    }

    qsizetype count() const {
        return tasks_.size();
    }

signals:
    void taskAdded(qsizetype index, const QString& title);

private:
    QStringList tasks_;
};

int main(int argc, char* argv[]) {
    QCoreApplication app(argc, argv);
    TaskBoard board;

    QObject::connect(
        &board,
        &TaskBoard::taskAdded,
        [](qsizetype index, const QString& title) {
            std::cout << "added task #" << index << ": "
                      << title.toStdString() << '\n';
        }
    );

    std::cout << "Qt event loop demo\n";

    QTimer::singleShot(0, &app, [&]() {
        board.addTask("connect signal to slot");
        board.addTask("let event loop deliver work");
        std::cout << "total tasks: " << board.count() << '\n';
        app.quit();
    });

    return app.exec();
}

#include "main.moc"
