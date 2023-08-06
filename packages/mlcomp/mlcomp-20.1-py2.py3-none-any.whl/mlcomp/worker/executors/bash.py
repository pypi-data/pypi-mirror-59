import subprocess

from mlcomp.contrib.search.grid import grid_cells
from mlcomp.utils.config import Config

from mlcomp.worker.executors import Executor


@Executor.register
class Bash(Executor):
    def __init__(self, command: str, **kwargs):
        super().__init__(**kwargs)

        self.command = command

    def work(self):
        self.info('Opening Process')
        sub_commands = self.command.split('&&')
        for sub in sub_commands:
            self.info('executing '+sub)

            process = subprocess.Popen('exec ' + sub,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE,
                                       shell=True
                                       )
            try:
                self.add_child_process(process.pid)
                self.info('Opening Process. Finished')

                while True:
                    line = process.stdout.readline()
                    if not line:
                        break
                    self.info(line.decode().strip())

                error = []
                while True:
                    line = process.stderr.readline()
                    if not line:
                        break
                    line = line.decode().strip()
                    error.append(line)

                process.communicate()

                if process.returncode != 0:
                    raise Exception('\n'.join(error))
            finally:
                process.kill()

    @classmethod
    def _from_config(
            cls, executor: dict, config: Config, additional_info: dict
    ):
        grid_cell = additional_info.get('grid_cell')
        grid_config = {}
        if grid_cell is not None:
            grid_config = grid_cells(executor['grid'])[grid_cell][0]
        for k, v in grid_config.items():
            executor['command'] = executor['command'].replace(f'${k}', str(v))
        return cls(**executor)


__all__ = ['Bash']
