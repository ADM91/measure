__author__ = 'masslab'

from subprocess import call
from config import masscode_path
from utility.queues import input_file_queue


def run_masscode_queue(cls):

    # Run until queue is empty
    while input_file_queue.qsize() > 0:

        input_file = input_file_queue.get(0)
        output_file = input_file[:-3] + "out"

        # Runs the masscode
        call('"' + masscode_path + '"' + " " + '"' + input_file + '"' + " " + '"' + output_file + '"' + "\n")
        input_file_queue.task_done()

        # Removes the input file path from the list
        try:
            cls.inputList.takeItem(0)
        except:
            pass
