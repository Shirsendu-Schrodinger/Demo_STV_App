from textual.app import App, ComposeResult, RenderResult
from textual.containers import VerticalScroll, Vertical, Horizontal
from textual.widgets import Footer, Static, Label
from textual.widget import Widget
from textual.message import Message
# from textual.css.query import NoMatches, WrongType
from dataclasses import dataclass
from typing import List
from textual.reactive import reactive
from textual import events
from datetime import datetime


@dataclass
class TaskInfo:
    id: int
    name: str
    start_time: datetime
    status: str
    logs: List[str]
    description: str


class Task(Widget):

    class Selected(Message):
        def __init__(self, task_info: TaskInfo):
            self.task_info = task_info
            super().__init__()

    def __init__(self, task_info: TaskInfo, id, classes):
        super().__init__(id=id, classes=classes)
        self.can_focus = True
        # self.task_name = task_info.name
        # self.task_id = task_info.id
        self.task_data = task_info

    def render(self) -> RenderResult:
        return f"[b]Task_id:[/b] {self.task_data.id} | \
            [b]{self.task_data.name}[/b]"

    def on_click(self, event: events.Click) -> None:
        print("Clicked")
        self.post_message(self.Selected(self.task_data))


class TaskList(Widget):
    def __init__(self, id):
        super().__init__(id=id)
        self.task_data: List[TaskInfo] = []
        # selected_task: reactive[]
        self.can_focus = True

    def compose(self) -> ComposeResult:
        self.task_data = self.load_data()
        with VerticalScroll():
            for task in self.task_data:
                yield Task(task, id=f"task-{task.id}",
                           classes=f"{task.status.lower()}")

    def load_data(self):
        return [
            TaskInfo(id=102, name="Task1", start_time=datetime.strptime("29-05-25 14:07:20.46",'%d-%m-%y %H:%M:%S.%f'), status="Running", logs=["Some Process\n"], description="Created by User A"),
            TaskInfo(id=106, name="Task2", status="Failed", start_time=datetime.strptime("12-03-24 09:15:32.74",'%d-%m-%y %H:%M:%S.%f'), logs=["Some Process\n", "Failed process\n"], description="Created by User X"),
            TaskInfo(id=204, name="Task3", status="Success", start_time=datetime.strptime("28-11-22 22:41:08.19",'%d-%m-%y %H:%M:%S.%f'), logs=["Some Process\n", "Process completed\n"], description="Created by User B"),
            TaskInfo(id=105, name="Task4", status="Failed", start_time=datetime.strptime("07-07-25 13:58:45.03",'%d-%m-%y %H:%M:%S.%f'), logs=["Some Process\n", "Failed process\n"], description="Created by User Y"),
            TaskInfo(id=202, name="Task5", status="Waiting", start_time=datetime.strptime("16-01-23 04:27:11.89",'%d-%m-%y %H:%M:%S.%f'), logs=["Waiting in Queue\n"], description="Created by User A"),
            TaskInfo(id=109, name="Task6", status="Running", start_time=datetime.strptime("03-06-24 17:36:55.62",'%d-%m-%y %H:%M:%S.%f'), logs=["Some Process\n"], description="Created by User L"),
            TaskInfo(id=201, name="Task7", status="Failed", start_time=datetime.strptime("25-10-21 20:09:03.47",'%d-%m-%y %H:%M:%S.%f'), logs=["Some Process\n", "Failed process\n"], description="Created by User P"),
            TaskInfo(id=100, name="Task8", status="Success", start_time=datetime.strptime("19-02-25 06:12:29.90",'%d-%m-%y %H:%M:%S.%f'), logs=["Some Process\n", "Process completed\n"], description="Created by User C")
        ]


class TaskDetails(Static):
    task_selected: reactive[TaskInfo | None] = reactive(None)

    def __init__(self, id):
        super().__init__(id=id)

    def compose(self) -> ComposeResult:
        self.label = Label("Select a task to view details", id="details-label")
        with VerticalScroll():
            yield self.label

    def update_task(self, task_info: TaskInfo) -> None:
        self.label.update(f"[b]Task ID:[/b] {task_info.id}\n"
                          f"[b]Name:[/b] {task_info.name}\n"
                          f"[b]Status:[/b] {task_info.status}\n"
                          f"[b]Creation Time:[/b] {task_info.start_time}\n"
                          f"[b]Description:[/b] {task_info.description}\n\n"
                          f"{'-'*10 + ' [b]Logs[/b] ' + '-'*10}\n"
                          f"{''.join([line for line in task_info.logs])}")


class TaskViewerApp(App):
    CSS_PATH = "taskviewer.tcss"

    def on_mount(self):
        obj = self.query_one("#left-pane")
        obj.border_title = "Tasks"
        obj = self.query_one("#right-pane")
        obj.border_title = "Info"

    def compose(self) -> ComposeResult:
        yield Footer()
        with Horizontal():
            with Vertical(id="left-pane"):
                yield TaskList(id="task-list")
            with Vertical(id="right-pane"):
                yield TaskDetails(id="view-pane")

    def on_task_selected(self, message: Task.Selected) -> None:
        # print("Message Received!")
        view_pane = self.query_one("#view-pane", TaskDetails)
        view_pane.update_task(message.task_info)
        self.query_one("#right-pane").border_subtitle = f"task-{message.task_info.id}"


if __name__ == '__main__':
    app = TaskViewerApp()
    app.run()
