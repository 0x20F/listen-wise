from typing import Callable, List, Any, Optional, Dict
from datetime import datetime


class PipelineUsable():
    def __init__(self) -> None:
        self.logger: Callable[[str], None] = lambda message: print(message)

    def setup(self) -> None:
        raise Exception("Setup method not implemented for module")

    def with_logger(self, logger: Callable[[str], None]):
        self.logger = logger


class PipelineStep():
    def __init__(
        self, name: str, box: PipelineUsable,
        needs: Optional[List[str]],
        method: str
    ) -> None:
        self.name = name
        self.box = box
        self.method = method
        self.needs = needs
        self.result = None

        # This will raise if not found
        self.runnable = getattr(self.box, self.method)

        # If we haven't exploded, setup the module
        # Logger is customised for each pipeline step
        def logger(message: str):
            now = datetime.now()
            formatted = now.strftime('%H:%M:%S')
            print('\033[0;90m{}\033[00m [{}] {}'.format(formatted, name, message))

        self.box.with_logger(logger)
        self.box.setup()
        

    def execute(self, args):
        is_tuple = type(args) is tuple

        if is_tuple:
            self.result = self.runnable(*args)
        else:
            self.result = self.runnable(args)


class Pipeline():
    def __init__(
        self, 
        *steps: PipelineStep
    ) -> None:
        self.steps: Dict[str, PipelineStep] = dict()

        for step in steps:
            self.steps[step.name] = step

    def run(self, data: Any):
        prev_step = ''

        try:
            for index, key in enumerate(self.steps):
                step = self.steps[key]
                args = None

                step.box.logger('Running')

                # Always pass the previous steps output to the next thing 
                # (unless they specifically need something else)
                
                if step.needs is not None:
                    # Find the result of the needed step
                    arg_list = [ self.steps[key].result for key in step.needs ]
                    # Turn them into a tuple since the executor will spread the arguments
                    args = tuple(arg_list)
                else:
                    if index > 0:
                        args = tuple(self.steps[prev_step].result or [])
                    else:
                        args = data

                step.execute(args)
                prev_step = key

                step.box.logger('Finished')
        except Exception as e:
            print('[-] Stopped pipeline execution. Something failed:')
            print(e)


def pipeline(*steps: PipelineStep) -> Pipeline:
    line = Pipeline(*steps)
    return line


def use(
    name: str, 
    box: PipelineUsable, 
    **kwargs
) -> PipelineStep:
    step = PipelineStep(
        name=name,
        box=box,
        needs=kwargs.get('needs', None),
        method=kwargs.get('method', None)
    )

    return step