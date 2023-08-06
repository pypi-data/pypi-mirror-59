#
#  Copyright (C) 2018-2019 Bloomberg Finance LP
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 2 of the License, or (at your option) any later version.
#
#  This library is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	 See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library. If not, see <http://www.gnu.org/licenses/>.

import os
import signal
import subprocess
import sys

import psutil

from .. import utils, _signals
from . import SandboxFlags
from .._exceptions import SandboxError
from .._protos.build.bazel.remote.execution.v2 import remote_execution_pb2
from ._sandboxreapi import SandboxREAPI


# SandboxBuildBoxRun()
#
# BuildBox-based sandbox implementation.
#
class SandboxBuildBoxRun(SandboxREAPI):
    def __init__(self, context, project, directory, **kwargs):
        kwargs["allow_real_directory"] = False
        super().__init__(context, project, directory, **kwargs)

    @classmethod
    def check_available(cls):
        try:
            utils.get_host_tool("buildbox-run")
        except utils.ProgramNotFoundError as Error:
            cls._dummy_reasons += ["buildbox-run not found"]
            raise SandboxError(" and ".join(cls._dummy_reasons), reason="unavailable-local-sandbox") from Error

    @classmethod
    def check_sandbox_config(cls, platform, config):
        # Report error for elements requiring non-0 UID/GID
        if config.build_uid != 0 or config.build_gid != 0:
            return False

        # Check host os and architecture match
        if config.build_os != platform.get_host_os():
            raise SandboxError("Configured and host OS don't match.")
        if config.build_arch != platform.get_host_arch():
            raise SandboxError("Configured and host architecture don't match.")

        return True

    def _execute_action(self, action, flags):
        stdout, stderr = self._get_output()

        context = self._get_context()
        cascache = context.get_cascache()
        casd_process_manager = cascache.get_casd_process_manager()

        with utils._tempnamedfile() as action_file, utils._tempnamedfile() as result_file:
            action_file.write(action.SerializeToString())
            action_file.flush()

            buildbox_command = [
                utils.get_host_tool("buildbox-run"),
                "--use-localcas",
                "--remote={}".format(casd_process_manager._connection_string),
                "--action={}".format(action_file.name),
                "--action-result={}".format(result_file.name),
            ]

            # If we're interactive, we want to inherit our stdin,
            # otherwise redirect to /dev/null, ensuring process
            # disconnected from terminal.
            if flags & SandboxFlags.INTERACTIVE:
                stdin = sys.stdin
            else:
                stdin = subprocess.DEVNULL

            self._run_buildbox(
                buildbox_command, stdin, stdout, stderr, interactive=(flags & SandboxFlags.INTERACTIVE),
            )

            return remote_execution_pb2.ActionResult().FromString(result_file.read())

    def _run_buildbox(self, argv, stdin, stdout, stderr, *, interactive):
        def kill_proc():
            if process:
                # First attempt to gracefully terminate
                proc = psutil.Process(process.pid)
                proc.terminate()

                try:
                    proc.wait(20)
                except psutil.TimeoutExpired:
                    utils._kill_process_tree(process.pid)

        def suspend_proc():
            group_id = os.getpgid(process.pid)
            os.killpg(group_id, signal.SIGSTOP)

        def resume_proc():
            group_id = os.getpgid(process.pid)
            os.killpg(group_id, signal.SIGCONT)

        with _signals.suspendable(suspend_proc, resume_proc), _signals.terminator(kill_proc):
            process = subprocess.Popen(
                argv, close_fds=True, stdin=stdin, stdout=stdout, stderr=stderr, start_new_session=interactive,
            )

            # Wait for the child process to finish, ensuring that
            # a SIGINT has exactly the effect the user probably
            # expects (i.e. let the child process handle it).
            try:
                while True:
                    try:
                        returncode = process.wait()
                        # If the process exits due to a signal, we
                        # brutally murder it to avoid zombies
                        if returncode < 0:
                            utils._kill_process_tree(process.pid)

                    # Unlike in the bwrap case, here only the main
                    # process seems to receive the SIGINT. We pass
                    # on the signal to the child and then continue
                    # to wait.
                    except KeyboardInterrupt:
                        process.send_signal(signal.SIGINT)
                        continue

                    break
            # If we can't find the process, it has already died of
            # its own accord, and therefore we don't need to check
            # or kill anything.
            except psutil.NoSuchProcess:
                pass

            if returncode != 0:
                raise SandboxError("buildbox-run failed with returncode {}".format(returncode))
