import asyncio
import time
from queue import Empty, Full
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from autoclass import autoclass
from pangeamt_tea.project.workflow.stage.base_stage import BaseStage


async def make_non_blocking(fn, executor, *args, loop=None):
    if loop is None:
        loop = asyncio.get_event_loop()
    await loop.run_in_executor(executor, fn, *args)


def fill_input_queue_worker(input_queue, input_ended_queue, data_generator, max_workers):
    input_len = 0
    for item in data_generator:
        input_queue.put(item)
        input_len += 1

    # Broadcast end signal to all workers
    for _ in range(max_workers):
        input_queue.put(None)

    # Send end signal to the output handler
    input_ended_queue.put(input_len)
    print("End filler")


def handle_output_queue(output_queue, input_ended_queue, progress_queue):
    i = 0
    data_generator_len = None

    while True:
        try:
            # The data generator length is sent by the filler
            data_generator_len = input_ended_queue.get(block=False)
        except Empty:
            try:
                result = output_queue.get(block=True, timeout=0.1)
                # TODO save to disk
            except Empty:
                continue

            i += 1
            try:
                progress_queue.put(i, block=False)
            except Full:
                pass
            if i == data_generator_len:
                progress_queue.put(data_generator_len, block=True)
                print("The end")
                break


def process_queue_worker(input_queue, output_queue, pipeline):
    while True:
        data = input_queue.get()
        if data is None:
            break
        time.sleep(0.03)
        output_queue.put(data)


@autoclass
class MultiprocessingCleaner:
    def __init__(self,
                 data_generator,
                 data_generator_len,
                 max_workers,
                 input_queue,
                 output_queue,
                 input_ended_queue,
                 progress_queue):
        pass

    @staticmethod
    def new(
            data_generator,
            data_generator_len,
            max_workers,
            multiprocessing_manager,

    ):
        input_queue = multiprocessing_manager.Queue(maxsize=max_workers * 10)
        output_queue = multiprocessing_manager.Queue()
        input_ended_queue = multiprocessing_manager.Queue()
        progress_queue = multiprocessing_manager.Queue(maxsize=1)
        return MultiprocessingCleaner(
            data_generator,
            data_generator_len,
            max_workers,
            input_queue,
            output_queue,
            input_ended_queue,
            progress_queue
        )

    async def clean(self):
        # Start input queue filler
        task1 = asyncio.create_task(
            make_non_blocking(
                fill_input_queue_worker,
                ThreadPoolExecutor(max_workers=1),
                self.input_queue,
                self.input_ended_queue,
                self.data_generator,
                self.max_workers
            ))

        # Start output queue handler
        task2 = asyncio.create_task(
            make_non_blocking(
                handle_output_queue,
                ThreadPoolExecutor(max_workers=1),
                self.output_queue,
                self.input_ended_queue,
                self.progress_queue
            ))

        # Create workers
        task3 = asyncio.create_task(make_non_blocking(
            process_queue_worker,
            ProcessPoolExecutor(max_workers=self.max_workers),
            self.input_queue,
            self.output_queue
        ))

        dones = 0
        while True:
            await asyncio.sleep(0.1)
            try:
                dones = self.progress_queue.get(block=False)
            except Empty:
                pass
            if dones != self.data_generator_len:
                yield dones
            else:
                break

        await asyncio.wait_for(task1, None)
        await asyncio.wait_for(task2, None)
        await asyncio.wait_for(task3, None)


class CleanStage(BaseStage):
    NAME = 'clean'

    def __init__(self, workflow):
        super().__init__(workflow, self.NAME)

    async def run(self, multiprocessing_manager, max_workers):
        # TODO
        # Read the project config.processor and instantiate a pangeanlp processor pipeline

        return {

        }
