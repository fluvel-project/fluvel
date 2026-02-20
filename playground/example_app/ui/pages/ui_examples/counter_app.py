import fluvel as fl

class Counter(fl.Model):
    count: int

    def increment(self):
        self.count += 1

    def decrement(self):
        self.count -= 1

cm = Counter(ref="cm").sync()

@fl.route("/counter-page")
class CounterPage(fl.Page):
    def build(self):
        with self.Horizontal(style="bg-slate-100") as  h:
            h.Button(text="-", on_click=cm.decrement)
            h.Label(bind="@cm.count % 'Counter: %v'")
            h.Button(text="+", on_click=cm.increment)