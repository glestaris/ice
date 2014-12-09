"""Wrapper class for API-related shell commands."""
import argparse

from . import ShellExt
from ice import api


class APIShell(ShellExt):
    """Wrapper class for API-related shell commands."""

    def __init__(self, shell):
        """
        :param ice.shell.Shell shell: The shell.
        """
        super(APIShell, self).__init__(shell)

        # Register self
        shell.add_magic_function('inst_ls', self.ls_inst)
        shell.add_magic_function_v2(
            'inst_wait', self.run_wait, self.get_wait_parser()
        )
        shell.add_magic_function(
            'inst_del', self.del_inst,
            usage='<Instance id> [<Instance id> ...]'
        )
        shell.add_magic_function(
            'inst_show', self.show_inst,
            usage='<Instance id> [<Instance id> ...]'
        )

    #
    # Commands
    #

    def ls_inst(self, magis, args_raw):
        """Lists instances."""
        # Get instances
        inst_list = api.instances.get_list()
        if inst_list is None:
            self.logger.error('Failed to find instances!')
            return

        self.logger.info('Found %d instances' % len(inst_list))
        print '-' * 129
        print '| {0:23s} | {1:20s} | {2:43s} | {3:30s} |'.format(
            'Id',
            'Public IP address',
            'Cloud Id',
            'Created on'
        )
        print '-' * 129
        for inst in inst_list:
            print '| {0.id:23s} | {0.public_ip_addr:20s}'.format(inst) \
                  + ' | {0.cloud_id:43s} | {0.created:30s} |'.format(inst)
        print '-' * 129

    def get_wait_parser(self):
        parser = argparse.ArgumentParser(prog='inst_wait', add_help=False)
        parser.add_argument(
            '-n', metavar='<Amount of instances>', dest='amt', type=int,
            default=1
        )
        parser.add_argument(
            '-t', metavar='<Timeout (sec.)>', dest='timeout', default=120
        )
        return parser

    def run_wait(self, magics, args_raw):
        """Waits for instances to appear."""
        args = self.get_wait_parser().parse_args(args_raw.split())
        res = api.instances.wait(args.amt, args.timeout)
        if res:
            self.logger.info('Instances are ready!')
        else:
            self.logger.error('Timeout!')

    def show_inst(self, magics, args_raw):
        """Shows information for a specific instance."""
        inst_ids = args_raw.split()

        # Check arguments
        if len(inst_ids) == 0:
            self.logger.error('Please specify instance id!')
            return

        # Get instance
        for inst_id in inst_ids:
            inst = api.instances.get(inst_id)
            if inst is None:
                self.logger.error('Failed to find instance `%s`!' % inst_id)
                return

            # Printout information
            for key, value in inst.__dict__.items():
                print '{0:30s}: {1}'.format(key, value)

    def del_inst(self, magics, args_raw):
        """Deletes a specific instance."""
        inst_ids = args_raw.split()

        # Check arguments
        if len(inst_ids) == 0:
            inst_ids = None

        # Fire action
        res = api.instances.destroy(inst_ids)
        if not res:
            self.logger.error('Failed to delete one or more instances!')
        else:
            self.logger.info('All instances successfully deleted.')
