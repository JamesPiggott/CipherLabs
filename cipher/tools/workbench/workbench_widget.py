class WorkbenchWidget:
    def __init__(
        self,
        widget_id,
        title,
        template,
        phase,
        description=None,
        recommended=False,
        enabled=True,
        reason=None,
        order=100,
        default_open=None,
    ):
        self.id = widget_id
        self.title = title
        self.template = template
        self.phase = phase
        self.description = description
        self.recommended = recommended
        self.enabled = enabled
        self.reason = reason
        self.order = order

        if default_open is None:
            self.default_open = recommended
        else:
            self.default_open = default_open