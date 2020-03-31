import kronos

from clients.utils.client_helper import store_hackers_data, simulate_exchanges


@kronos.register('* * * * *')
def import_hackers_data():
    store_hackers_data()


@kronos.register('* * * * *')
def simulate_members_clients_exchanges():
    simulate_exchanges(times=5)
