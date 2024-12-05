class Pipeline:
    def __init__(self, input_handler, command_parser):
        self.image = input_handler.load_image()
        self.commands = command_parser.parse()

    def run(self):
        for command in self.commands:
            module = command["module"]
            params = command["params"]
            self.image = module.execute(self.image, **params)
